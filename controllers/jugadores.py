import utils.corefiles as cf
import utils.validaData as vd
import controllers.equipos as eq
from datetime import datetime

ARCHIVO_JUGADORES = "data/jugadores.json"

POSICIONES = {
    1: "Portero",
    2: "Defensa Central",
    3: "Lateral Derecho",
    4: "Lateral Izquierdo",
    5: "Mediocentro Defensivo",
    6: "Mediocentro",
    7: "Mediocentro Ofensivo",
    8: "Extremo Derecho",
    9: "Extremo Izquierdo",
    10: "Delantero Centro"
}

def mostrar_posiciones():
    """Muestra las posiciones disponibles"""
    print("\n⚽ POSICIONES DISPONIBLES:")
    for num, posicion in POSICIONES.items():
        print(f"{num}. {posicion}")

def registrar_jugador():
    """Registra un nuevo jugador en el sistema"""
    print("👤 REGISTRO DE JUGADOR")
    print("-" * 30)
    
    # Verificar que hay equipos disponibles
    equipos = eq.obtener_todos_equipos()
    if not equipos:
        print("❌ No hay equipos registrados. Registre un equipo primero.")
        return
    
    # Mostrar equipos disponibles
    print("\n📋 EQUIPOS DISPONIBLES:")
    for id_eq, datos in equipos.items():
        print(f"{id_eq} - {datos['nombre']} ({datos['pais']})")
    
    # Solicitar ID del equipo
    id_equipo = input("\nID del equipo: ").strip()
    if not eq.obtener_equipo_por_id(id_equipo):
        print("❌ Equipo no válido")
        return
    
    # Generar ID único del jugador
    id_jugador = cf.obtener_siguiente_id(ARCHIVO_JUGADORES, "JG")
    
    # Solicitar datos del jugador
    nombre = vd.validatetext("Nombre completo del jugador: ")
    
    # Validar número de dorsal único en el equipo
    dorsal = validar_dorsal_unico(id_equipo)
    
    # Seleccionar posición
    mostrar_posiciones()
    pos_num = vd.validateInt("Seleccione posición (1-10): ")
    while pos_num not in POSICIONES:
        print("❌ Posición inválida")
        pos_num = vd.validateInt("Seleccione posición (1-10): ")
    
    posicion = POSICIONES[pos_num]
    
    # Datos adicionales
    print("\nFecha de nacimiento:")
    dia = vd.validateInt("Día (1-31): ")
    mes = vd.validateInt("Mes (1-12): ")
    año = vd.validateInt("Año: ")
    
    try:
        fecha_nacimiento = datetime(año, mes, dia).strftime("%d/%m/%Y")
        edad = datetime.now().year - año
    except ValueError:
        print("❌ Fecha inválida. Se usará edad manual.")
        fecha_nacimiento = "No especificada"
        edad = vd.validateInt("Edad: ")
    
    nacionalidad = vd.validatetext("Nacionalidad: ")
    
    # Crear diccionario del jugador
    jugador = {
        id_jugador: {
            "nombre": nombre,
            "dorsal": dorsal,
            "posicion": posicion,
            "equipo_id": id_equipo,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "nacionalidad": nacionalidad,
            "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "activo": True,
            "historial_equipos": [id_equipo]
        }
    }
    
    # Guardar en archivo JSON
    if cf.updateJson(ARCHIVO_JUGADORES, jugador):
        print(f"\n✅ Jugador '{nombre}' registrado exitosamente con ID: {id_jugador}")
        print(f"   Dorsal: #{dorsal} - Posición: {posicion}")
    else:
        print("❌ Error al registrar el jugador")

def validar_dorsal_unico(id_equipo: str) -> int:
    """Valida que el dorsal sea único en el equipo"""
    jugadores = cf.readJson(ARCHIVO_JUGADORES)
    dorsales_usados = []
    
    for jugador in jugadores.values():
        if jugador.get("equipo_id") == id_equipo and jugador.get("activo", True):
            dorsales_usados.append(jugador.get("dorsal"))
    
    while True:
        dorsal = vd.validateInt("Número de dorsal (1-99): ")
        if 1 <= dorsal <= 99:
            if dorsal not in dorsales_usados:
                return dorsal
            else:
                print(f"❌ El dorsal #{dorsal} ya está en uso en este equipo")
        else:
            print("❌ El dorsal debe estar entre 1 y 99")

def listar_jugadores():
    """Lista todos los jugadores registrados"""
    print("👥 LISTA DE JUGADORES REGISTRADOS")
    print("-" * 60)
    
    jugadores = cf.readJson(ARCHIVO_JUGADORES)
    equipos = eq.obtener_todos_equipos()
    
    if not jugadores:
        print("⚠️ No hay jugadores registrados")
        return
    
    # Opción de filtrar por equipo
    print("Opciones de listado:")
    print("1. Todos los jugadores")
    print("2. Por equipo específico")
    
    opcion = vd.validateInt("Seleccione opción: ")
    
    if opcion == 2:
        if not equipos:
            print("❌ No hay equipos registrados")
            return
        
        print("\n📋 EQUIPOS DISPONIBLES:")
        for id_eq, datos in equipos.items():
            print(f"{id_eq} - {datos['nombre']}")
        
        id_equipo_filtro = input("\nID del equipo: ").strip()
        if id_equipo_filtro not in equipos:
            print("❌ Equipo no válido")
            return
    else:
        id_equipo_filtro = None
    
    print(f"\n{'ID':<8} {'NOMBRE':<20} {'DORSAL':<8} {'POSICIÓN':<20} {'EQUIPO':<15}")
    print("-" * 71)
    
    contador = 0
    for id_jugador, datos in jugadores.items():
        if not datos.get("activo", True):
            continue
        
        if id_equipo_filtro and datos.get("equipo_id") != id_equipo_filtro:
            continue
        
        equipo_nombre = equipos.get(datos.get("equipo_id", ""), {}).get("nombre", "Sin equipo")
        
        print(f"{id_jugador:<8} {datos['nombre']:<20} #{datos['dorsal']:<7} {datos['posicion']:<20} {equipo_nombre:<15}")
        contador += 1
    
    print(f"\nTotal de jugadores mostrados: {contador}")

def obtener_jugador_por_id(id_jugador: str):
    """Obtiene un jugador específico por su ID"""
    jugador = cf.buscar_por_id(ARCHIVO_JUGADORES, id_jugador)
    return jugador if jugador and jugador.get("activo", True) else None

def obtener_jugadores_por_equipo(id_equipo: str):
    """Obtiene todos los jugadores de un equipo específico"""
    jugadores = cf.readJson(ARCHIVO_JUGADORES)
    return {k: v for k, v in jugadores.items() 
            if v.get("equipo_id") == id_equipo and v.get("activo", True)}

def cambiar_equipo_jugador(id_jugador: str, nuevo_equipo_id: str):
    """Cambia el equipo de un jugador (usado en transferencias)"""
    jugadores = cf.readJson(ARCHIVO_JUGADORES)
    
    if id_jugador in jugadores:
        # Actualizar equipo actual
        jugadores[id_jugador]["equipo_id"] = nuevo_equipo_id
        
        # Agregar al historial
        historial = jugadores[id_jugador].get("historial_equipos", [])
        if nuevo_equipo_id not in historial:
            historial.append(nuevo_equipo_id)
            jugadores[id_jugador]["historial_equipos"] = historial
        
        # Actualizar fecha de última modificación
        jugadores[id_jugador]["ultima_actualizacion"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        cf.writeJson(ARCHIVO_JUGADORES, jugadores)
        return True
    return False

def mostrar_detalle_jugador(id_jugador: str):
    """Muestra información detallada de un jugador"""
    jugador = obtener_jugador_por_id(id_jugador)
    
    if not jugador:
        print("❌ Jugador no encontrado")
        return
    
    equipo = eq.obtener_equipo_por_id(jugador.get("equipo_id", ""))
    equipo_nombre = equipo["nombre"] if equipo else "Sin equipo"
    
    print(f"👤 DETALLES DEL JUGADOR - {jugador['nombre']}")
    print("-" * 50)
    print(f"ID: {id_jugador}")
    print(f"Nombre: {jugador['nombre']}")
    print(f"Dorsal: #{jugador['dorsal']}")
    print(f"Posición: {jugador['posicion']}")
    print(f"Equipo actual: {equipo_nombre}")
    print(f"Edad: {jugador['edad']} años")
    print(f"Nacionalidad: {jugador['nacionalidad']}")
    print(f"Fecha de nacimiento: {jugador['fecha_nacimiento']}")
    print(f"Registrado: {jugador['fecha_registro']}")
    
    if len(jugador.get("historial_equipos", [])) > 1:
        print(f"Historial de equipos: {len(jugador['historial_equipos'])} equipos")