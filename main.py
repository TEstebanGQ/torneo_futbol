import utils.screenControllers as sc
import utils.validaData as vd
import controllers.equipos as eq
import controllers.jugadores as jg
import controllers.transferencias as tr
import controllers.estadisticas as est
import utils.corefiles as cf

def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("=" * 40)
    print("    🏆 GESTOR DE TORNEOS DE FÚTBOL    ")
    print("=" * 40)
    print("1. 📘 Registrar equipo")
    print("2. 📋 Listar equipos")
    print("3. 👤 Registrar jugador")
    print("4. 👥 Listar jugadores")
    print("5. 🔄 Transferencia de jugador")
    print("6. 📊 Ver estadísticas")
    print("7. 🏟️  Gestionar dirigentes")
    print("8. 🏆 Gestionar torneos")
    print("0. ❌ Salir")
    print("=" * 40)

def inicializar_sistema():
    """Inicializa la estructura de archivos JSON"""
    estructura_inicial = {
        "equipos": {},
        "jugadores": {},
        "dirigentes": {},
        "ligas": {},
        "torneos": {},
        "partidos": {},
        "transferencias": {}
    }
    
    # Inicializar archivos individuales
    archivos = [
        ("data/equipos.json", {}),
        ("data/jugadores.json", {}),
        ("data/dirigentes.json", {}),
        ("data/ligas.json", {}),
        ("data/torneos.json", {}),
        ("data/partidos.json", {}),
        ("data/transferencias.json", {})
    ]
    
    for archivo, estructura in archivos:
        cf.initializeJson(archivo, estructura)  # Corregido: manteniendo la I mayúscula

def main():
    """Función principal del programa"""
    inicializar_sistema()
    
    while True:
        sc.limpiar_pantalla()
        mostrar_menu()
        
        opcion = vd.validateInt("Seleccione una opción: ")
        
        if opcion == 1:
            sc.limpiar_pantalla()
            eq.registrar_equipo()
            sc.pausar_pantalla()
            
        elif opcion == 2:
            sc.limpiar_pantalla()
            eq.listar_equipos()
            sc.pausar_pantalla()
            
        elif opcion == 3:
            sc.limpiar_pantalla()
            jg.registrar_jugador()
            sc.pausar_pantalla()
            
        elif opcion == 4:
            sc.limpiar_pantalla()
            jg.listar_jugadores()
            sc.pausar_pantalla()
            
        elif opcion == 5:
            sc.limpiar_pantalla()
            tr.realizar_transferencia()
            sc.pausar_pantalla()
            
        elif opcion == 6:
            sc.limpiar_pantalla()
            est.mostrar_estadisticas()
            sc.pausar_pantalla()
            
        elif opcion == 7:
            sc.limpiar_pantalla()
            print("🏟️ Gestión de dirigentes - En desarrollo")
            sc.pausar_pantalla()
            
        elif opcion == 8:
            sc.limpiar_pantalla()
            print("🏆 Gestión de torneos - En desarrollo")
            sc.pausar_pantalla()
            
        elif opcion == 0:
            sc.limpiar_pantalla()
            print("¡Gracias por usar el Gestor de Torneos! ⚽")
            break
            
        else:
            print("❌ Opción inválida. Por favor seleccione una opción válida.")
            sc.pausar_pantalla()

if __name__ == "__main__":
    main()