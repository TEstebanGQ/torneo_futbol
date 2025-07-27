import os
import sys
import controllers.equipos as equiposs
import controllers.jugadores as jugadoress
import controllers.transferencias as transferenciass
from utils.screenControllers import limpiar_pantalla
import controllers.ligas as ligass

class AnsiColors:
    RESET = '\033[0m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'

def _get_key_windows():
    import msvcrt
    key = msvcrt.getch()
    if key in b'\x00\xe0':
        key = msvcrt.getch()
        if key == b'H': return 'up'
        if key == b'P': return 'down'
    elif key == b'\r':
        return 'enter'
    return None

def _get_key_unix():
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(sys.stdin.fileno())
        char = sys.stdin.read(1)
        if char == '\x1b':
            sequence = sys.stdin.read(2)
            if sequence == '[A': return 'up'
            if sequence == '[B': return 'down'
        elif char in ('\n', '\r'):
            return 'enter'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def interactive_menu_colored(options):
    current_option = 0
    get_key = _get_key_windows if os.name == 'nt' else _get_key_unix

    if os.name == 'nt':
        os.system('')

    while True:
        limpiar_pantalla()
        print("Menú torneo de fútbol")
        print("Seleccione una opción (use las flechas y Enter):")
        print("──────────────────────────────────────────────")

        for i, option in enumerate(options):
            if i == current_option:
                print(f"{AnsiColors.YELLOW}{option}{AnsiColors.RESET}")
            else:
                print(option)
        
        print("──────────────────────────────────────────────")

        key = get_key()

        if key == 'up':
            current_option = (current_option - 1) % len(options)
        elif key == 'down':
            current_option = (current_option + 1) % len(options)
        elif key == 'enter':
            return current_option

if __name__ == '__main__':
    menu_items = [
        '- Gestionar Equipos', 
        '- Gestionar Jugadores',
        '- Transferencias de Jugadores',
        '- Ver Estadisticas',
        '- Gestionar Ligas',
        '- Gestionar Torneos',
        '- Gestionar Dirigentes',
        '- Gestionar Partidos',
        '- Salir'
    ]
    
    while True:
        selected_index = interactive_menu_colored(menu_items)
        limpiar_pantalla()
        selected_text = menu_items[selected_index]
        print(f"Ha seleccionado: {AnsiColors.GREEN}{selected_text}{AnsiColors.RESET}")

        match selected_index:
            case 0:
                equiposs.subMenuEquipos()
            case 1:
                jugadoress.subMenuJugadores()
            case 2:
                transferenciass.subMenuTransferencias()
            case 3:
                pass
            case 4:
                ligass.subMenuLigas()
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
            case 8:
                print("¡Hasta luego!")
                break
            case _:
                print("Opción no válida.")
