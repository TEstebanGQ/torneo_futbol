import os
import sys
import time

def pausar_pantalla():
    """Pausa la ejecución esperando entrada del usuario"""
    try:
        if sys.platform == "linux" or sys.platform == "darwin":
            input('\n🔄 Presione Enter para continuar...')
        else:
            os.system('pause')
    except KeyboardInterrupt:
        print("\n❌ Operación interrumpida")

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    try:
        if sys.platform == "linux" or sys.platform == "darwin":
            os.system('clear')
        else:
            os.system('cls')
    except:
        # Fallback para sistemas que no soporten clear/cls
        print('\n' * 50)

def mostrar_titulo(titulo: str, ancho: int = 60):
    """Muestra un título decorado"""
    print("=" * ancho)
    print(f"{titulo.center(ancho)}")
    print("=" * ancho)

def mostrar_subtitulo(subtitulo: str, ancho: int = 40):
    """Muestra un subtítulo decorado"""
    print("-" * ancho)
    print(f"{subtitulo.center(ancho)}")
    print("-" * ancho)

def mostrar_separador(caracter: str = "-", longitud: int = 50):
    """Muestra una línea separadora"""
    print(caracter * longitud)

def mostrar_mensaje_exito(mensaje: str):
    """Muestra un mensaje de éxito"""
    print(f"✅ {mensaje}")

def mostrar_mensaje_error(mensaje: str):
    """Muestra un mensaje de error"""
    print(f"❌ {mensaje}")

def mostrar_mensaje_advertencia(mensaje: str):
    """Muestra un mensaje de advertencia"""
    print(f"⚠️  {mensaje}")

def mostrar_mensaje_info(mensaje: str):
    """Muestra un mensaje informativo"""
    print(f"ℹ️  {mensaje}")

def mostrar_cargando(mensaje: str = "Cargando", duracion: float = 2.0):
    """Muestra una animación de carga"""
    print(f"{mensaje}", end="")
    for i in range(int(duracion * 4)):
        print(".", end="", flush=True)
        time.sleep(0.25)
    print(" ✓")

def mostrar_progress_bar(progreso: int, total: int, longitud: int = 30):
    """Muestra una barra de progreso"""
    porcentaje = (progreso / total) * 100
    bloques = int((progreso / total) * longitud)
    barra = "█" * bloques + "-" * (longitud - bloques)
    print(f"[{barra}] {porcentaje:.2f}% ({progreso}/{total})", end="\r")