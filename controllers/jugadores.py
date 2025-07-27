<<<<<<< HEAD
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
=======
import os 
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import json 

RUTA_JUGADORES_JSON = os.path.join("data", "jugadores.json")
RUTA_EQUIPOS_JSON = os.path.join("data", "equipos.json")

POSICIONES_VALIDAS = [
    "Portero",
    "Defensa Central Derecho",
    "Defensa Central Izquierdo",
    "Defensa Central",
    "Lateral Derecho",
    "Lateral Izquierdo",
    "Líbero",
    "Centrocampista Defensivo",
    "Centrocampista Central",
    "Centrocampista Ofensivo",
    "Centrocampista Derecho",
    "Centrocampista Izquierdo",
    "Extremo Derecho",
    "Extremo Izquierdo",
    "Delantero Centro"
]

def cargar_datos_jugadores():
    os.makedirs("data", exist_ok=True)
    try:
        with open(RUTA_JUGADORES_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos_jugadores(datos):
    with open(RUTA_JUGADORES_JSON, 'w') as f:
        json.dump(datos, f, indent=4)

def cargar_datos_equipos():
    try:
        with open(RUTA_EQUIPOS_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

lista_de_jugadores = cargar_datos_jugadores()

def obtener_id_validado():
    while True:
        try:
            id_str = input("Ingrese el ID del jugador: ").strip()
            id_ingresado = int(id_str)
            
            ids_existentes = [jugador.get("id") for jugador in lista_de_jugadores]
            if id_ingresado in ids_existentes:
                print("Error: El ID ingresado ya existe. Por favor, intente con otro.")
                continue
            
            return id_ingresado
        except ValueError:
            print("Error: Debe ingresar un número entero válido para el ID.")

def obtener_nombre_validado():
    while True:
        nombre = input("Ingrese el nombre del jugador: ").strip()
        if nombre and all(c.isalpha() or c.isspace() for c in nombre):
            return nombre
        else:
            print("Error: El nombre solo puede contener letras y espacios.")

def obtener_dorsal_validado():
    while True:
        dorsal_str = input("Ingrese el número de dorsal (1-99): ").strip()
        try:
            dorsal = int(dorsal_str)
            if 1 <= dorsal <= 99:
                return dorsal
            else:
                print("Error: El dorsal debe ser un número entre 1 y 99.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def obtener_posicion_validada():
    while True:
        posicion = input(f"Ingrese la posición: ").strip().title()
        if posicion in POSICIONES_VALIDAS:
            return posicion
        else:
            print("\nError: Posición no válida.")
            print("Las posiciones aceptadas son:", ", ".join(POSICIONES_VALIDAS))
            pausar_pantalla()
            limpiar_pantalla()
            print("--- Registro de Nuevos Jugadores (continuación) ---")

def subMenuJugadores():
    while True:
        limpiar_pantalla() 
        print("--- Submenú de Gestión de Jugadores ---")
        print("1. Registrar un nuevo jugador")
        print("2. Listar todos los jugadores")
        print("3. Volver al menú principal")
        print("-------------------------------------")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crearJugador()
        elif opcion == '2':
            listarJugadores()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar_pantalla()

def crearJugador():
    limpiar_pantalla()
    print("--- Registro de Nuevos Jugadores ---")
    
    equipos = cargar_datos_equipos()
    if not equipos:
        print("Error: No hay equipos registrados. No se puede añadir un jugador.")
        pausar_pantalla()
        return

    while True:
        nuevo_id = obtener_id_validado()
        nombre = obtener_nombre_validado()
        posicion = obtener_posicion_validada()
        dorsal = obtener_dorsal_validado()

        equipo_id_seleccionado = None
        while True:
            limpiar_pantalla()
            print("--- Equipos Disponibles ---")
            for equipo in equipos:
                print(f"ID: {equipo['id']} - Nombre: {equipo['nombre']}")
            print("---------------------------")
            
            try:
                id_ingresado = int(input("Ingrese el ID del equipo al que pertenece el jugador: "))
                ids_validos = [equipo['id'] for equipo in equipos]
                if id_ingresado in ids_validos:
                    equipo_id_seleccionado = id_ingresado
                    break
                else:
                    print("Error: El ID del equipo no existe. Intente de nuevo.")
                    pausar_pantalla()
            except ValueError:
                print("Error: Debe ingresar un número para el ID. Intente de nuevo.")
                pausar_pantalla()

        nuevo_jugador = {
            "id": nuevo_id,
            "nombre": nombre,
            "dorsal": dorsal,
            "posicion": posicion,
            "equipo_id": equipo_id_seleccionado
        }
        
        lista_de_jugadores.append(nuevo_jugador)
        guardar_datos_jugadores(lista_de_jugadores)
        
        print(f"\n¡Jugador '{nombre}' (ID: {nuevo_id}) registrado exitosamente!")
        
        while True:
            seguir = input("\n¿Desea registrar otro jugador? (Si/No): ").lower()
            if seguir in ['si', 'no']:
                break
            else:
                print("Respuesta no válida. Por favor, ingrese 'Si' o 'No'.")
        
        if seguir == 'no':
            break
        
        limpiar_pantalla()
        print("--- Registro de Nuevos Jugadores ---")

def listarJugadores():
    limpiar_pantalla()
    print("--- Lista de Jugadores Registrados ---")
    
    equipos = cargar_datos_equipos()
    mapa_nombres_equipos = {equipo['id']: equipo['nombre'] for equipo in equipos}

    if not lista_de_jugadores:
        print("No hay jugadores registrados.")
    else:
        for jugador in lista_de_jugadores:
            nombre_equipo = mapa_nombres_equipos.get(jugador['equipo_id'], "Equipo no encontrado")
            
            print(f"  ID: {jugador['id']}")
            print(f"  Nombre: {jugador['nombre']}")
            print(f"  Dorsal: {jugador['dorsal']} | Posición: {jugador['posicion']}")
            print(f"  Equipo: {nombre_equipo} (ID: {jugador['equipo_id']})")
            print("-" * 30)
    print("\nPresione Enter para continuar...")    
    pausar_pantalla()
>>>>>>> 5c19e46 (primer)
