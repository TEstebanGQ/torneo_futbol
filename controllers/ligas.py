import os
import json
import datetime
from utils.screenControllers import limpiar_pantalla, pausar_pantalla

RUTA_LIGAS_JSON = os.path.join("data", "ligas.json")
RUTA_EQUIPOS_JSON = os.path.join("data", "equipos.json")

def cargar_datos(ruta_archivo):
    os.makedirs("data", exist_ok=True)
    try:
        with open(ruta_archivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(datos, ruta_archivo):
    with open(ruta_archivo, 'w') as f:
        json.dump(datos, f, indent=4)

def obtener_nombre_liga_validado(lista_ligas):
    while True:
        nombre = input("Ingrese el nombre de la liga: ").strip()
        if not nombre:
            print("Error: El nombre de la liga no puede estar vacío.")
            continue
        
        if nombre.lower() in [liga['nombre'].lower() for liga in lista_ligas]:
            print(f"Error: La liga '{nombre}' ya se encuentra registrada.")
            continue
            
        return nombre

def obtener_pais_validado():
    while True:
        pais = input("Ingrese el país de la liga: ").strip()
        if not pais:
            print("Error: El país no puede estar vacío.")
            continue

        if all(c.isalpha() or c.isspace() for c in pais):
            return pais
        else:
            print("Error: El país solo puede contener letras y espacios.")

def obtener_fecha_valida(prompt, fecha_referencia=None):
    while True:
        fecha_str = input(prompt).strip()
        try:
            fecha_obj = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            if fecha_referencia and fecha_obj <= fecha_referencia:
                print(f"Error: La fecha final debe ser posterior a la fecha inicial ({fecha_referencia.strftime('%Y-%m-%d')}).")
                continue
            return fecha_str, fecha_obj
        except ValueError:
            print("Error: Formato de fecha no válido. Por favor, use YYYY-MM-DD.")

def agregar_equipos_a_liga(nueva_liga_id, pais_de_la_liga):
    equipos_seleccionados_ids = []
    
    while True:
        limpiar_pantalla()
        equipos_todos = cargar_datos(RUTA_EQUIPOS_JSON)
        
        equipos_disponibles = [
            e for e in equipos_todos 
            if not e.get("liga_id") and e.get("pais", "").lower() == pais_de_la_liga.lower()
        ]

        print(f"--- Agregar Equipos de '{pais_de_la_liga}' a la Liga ---")
        if not equipos_disponibles:
            print("No hay equipos disponibles de este país para agregar.")
            pausar_pantalla()
            break

        print("Equipos Disponibles:")
        for equipo in equipos_disponibles:
            print(f"ID: {equipo['id']} - Nombre: {equipo['nombre']}")
        print("-------------------------------")

        try:
            equipo_id_str = input("Ingrese el ID del equipo a agregar (o 'fin' para terminar): ").strip()
            if equipo_id_str.lower() == 'fin':
                break
            
            equipo_id = int(equipo_id_str)
            equipo_a_agregar = next((e for e in equipos_disponibles if e['id'] == equipo_id), None)

            if equipo_a_agregar:
                # Verificar si el equipo ya está asignado a otra liga
                if equipo_a_agregar.get("liga_id"):
                    print("Error: Este equipo ya está asignado a otra liga.")
                    pausar_pantalla()
                    continue

                # Asignar el equipo a la nueva liga
                for equipo_en_lista in equipos_todos:
                    if equipo_en_lista['id'] == equipo_id:
                        equipo_en_lista['liga_id'] = nueva_liga_id
                        break
                guardar_datos(equipos_todos, RUTA_EQUIPOS_JSON)

                equipos_seleccionados_ids.append(equipo_id)
                print(f"¡Equipo '{equipo_a_agregar['nombre']}' agregado a la liga!")
            else:
                print("Error: ID de equipo no válido o ya asignado.")
                pausar_pantalla()

        except ValueError:
            print("Error: Entrada no válida.")
            pausar_pantalla()

    return equipos_seleccionados_ids


    return equipos_seleccionados_ids

def subMenuLigas():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Gestión de Ligas ---")
        print("1. Crear una nueva Liga")
        print("2. Listar todas las Ligas")
        print("3. Volver al Menú Principal")
        print("-----------------------------------")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            crearLiga()
        elif opcion == "2":
            listarLigas()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar_pantalla()

def crearLiga():
    limpiar_pantalla()
    print("--- Crear Nueva Liga ---")
    
    lista_de_ligas = cargar_datos(RUTA_LIGAS_JSON)
    
    if not lista_de_ligas:
        nuevo_id = 1
    else:
        nuevo_id = max(liga.get("id", 0) for liga in lista_de_ligas) + 1

    nombre = obtener_nombre_liga_validado(lista_de_ligas)
    pais = obtener_pais_validado()
    fecha_inicial_str, fecha_inicial_obj = obtener_fecha_valida("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fecha_final_str, _ = obtener_fecha_valida("Ingrese la fecha de finalización (YYYY-MM-DD): ", fecha_referencia=fecha_inicial_obj)

    ids_equipos_en_liga = agregar_equipos_a_liga(nuevo_id, pais)

    nueva_liga = {
        "id": nuevo_id,
        "nombre": nombre,
        "pais": pais,
        "fecha_inicial": fecha_inicial_str,
        "fecha_final": fecha_final_str,
        "equipos_ids": ids_equipos_en_liga
    }
    
    lista_de_ligas.append(nueva_liga)
    guardar_datos(lista_de_ligas, RUTA_LIGAS_JSON)
    
    print(f"\n¡Liga '{nombre}' creada exitosamente!")
    pausar_pantalla()

def listarLigas():
    limpiar_pantalla()
    print("--- Listado de Ligas Registradas ---")
    
    lista_de_ligas = cargar_datos(RUTA_LIGAS_JSON)
    equipos_todos = cargar_datos(RUTA_EQUIPOS_JSON)
    mapa_equipos = {e['id']: e['nombre'] for e in equipos_todos}

    if not lista_de_ligas:
        print("No hay ligas registradas.")
    else:
        for liga in lista_de_ligas:
            print(f"\nID: {liga['id']} | Nombre: {liga['nombre']} | País: {liga['pais']}")
            print(f"  Duración: {liga['fecha_inicial']} a {liga['fecha_final']}")
            print("  Equipos Participantes:")
            if not liga.get('equipos_ids'):
                print("    - Ningún equipo asignado.")
            else:
                for equipo_id in liga['equipos_ids']:
                    nombre_equipo = mapa_equipos.get(equipo_id, "Equipo Desconocido")
                    print(f"    - {nombre_equipo} (ID: {equipo_id})")
            print("-" * 40)
    print("Presione Enter para continuar...")
    pausar_pantalla()