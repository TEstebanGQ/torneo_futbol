<<<<<<< HEAD
import utils.corefiles as cf
import utils.validaData as vd
import controllers.equipos as eq
import controllers.jugadores as jg
from datetime import datetime

ARCHIVO_TRANSFERENCIAS = "data/transferencias.json"

TIPOS_TRANSFERENCIA = {
    1: "Venta definitiva",
    2: "Préstamo temporal",
    3: "Intercambio",
    4: "Traspaso libre"
}

def mostrar_tipos_transferencia():
    """Muestra los tipos de transferencia disponibles"""
    print("\n🔄 TIPOS DE TRANSFERENCIA:")
    for num, tipo in TIPOS_TRANSFERENCIA.items():
        print(f"{num}. {tipo}")

def realizar_transferencia():
    """Realiza una transferencia de jugador entre equipos"""
    print("🔄 TRANSFERENCIA DE JUGADOR")
    print("-" * 35)
    
    # Verificar que hay jugadores y equipos
    jugadores = cf.readJson("data/jugadores.json")
    equipos = eq.obtener_todos_equipos()
    
    if not jugadores:
        print("❌ No hay jugadores registrados")
        return
    
    if len(equipos) < 2:
        print("❌ Se necesitan al menos 2 equipos para realizar transferencias")
        return
    
    # Mostrar jugadores disponibles
    print("\n👥 JUGADORES DISPONIBLES:")
    jugadores_activos = {k: v for k, v in jugadores.items() if v.get("activo", True)}
    
    for id_jg, datos in jugadores_activos.items():
        equipo_actual = eq.obtener_equipo_por_id(datos.get("equipo_id", ""))
        equipo_nombre = equipo_actual["nombre"] if equipo_actual else "Sin equipo"
        print(f"{id_jg} - {datos['nombre']} (#{datos['dorsal']}) - {equipo_nombre}")
    
    # Seleccionar jugador
    id_jugador = input("\nID del jugador a transferir: ").strip()
    jugador = jg.obtener_jugador_por_id(id_jugador)
    
    if not jugador:
        print("❌ Jugador no válido o no encontrado")
        return
    
    equipo_origen_id = jugador.get("equipo_id")
    equipo_origen = eq.obtener_equipo_por_id(equipo_origen_id)
    
    print(f"\n📋 Jugador seleccionado: {jugador['nombre']}")
    print(f"   Equipo actual: {equipo_origen['nombre'] if equipo_origen else 'Sin equipo'}")
    
    # Mostrar equipos de destino (excluyendo el actual)
    print("\n🏟️ EQUIPOS DE DESTINO DISPONIBLES:")
    equipos_destino = {k: v for k, v in equipos.items() if k != equipo_origen_id}
    
    for id_eq, datos in equipos_destino.items():
        print(f"{id_eq} - {datos['nombre']} ({datos['pais']})")
    
    # Seleccionar equipo destino
    id_equipo_destino = input("\nID del equipo destino: ").strip()
    if id_equipo_destino not in equipos_destino:
        print("❌ Equipo destino no válido")
        return
    
    equipo_destino = equipos_destino[id_equipo_destino]
    
    # Verificar dorsal disponible en equipo destino
    dorsal_actual = jugador.get("dorsal")
    jugadores_destino = jg.obtener_jugadores_por_equipo(id_equipo_destino)
    dorsales_ocupados = [j.get("dorsal") for j in jugadores_destino.values()]
    
    if dorsal_actual in dorsales_ocupados:
        print(f"⚠️ El dorsal #{dorsal_actual} ya está ocupado en {equipo_destino['nombre']}")
        print("Dorsales disponibles:", [i for i in range(1, 100) if i not in dorsales_ocupados][:10], "...")
        nuevo_dorsal = vd.validateInt("Nuevo número de dorsal: ")
        while nuevo_dorsal in dorsales_ocupados or nuevo_dorsal < 1 or nuevo_dorsal > 99:
            print("❌ Dorsal no disponible")
            nuevo_dorsal = vd.validateInt("Nuevo número de dorsal (1-99): ")
    else:
        nuevo_dorsal = dorsal_actual
    
    # Seleccionar tipo de transferencia
    mostrar_tipos_transferencia()
    tipo_num = vd.validateInt("Seleccione tipo de transferencia (1-4): ")
    while tipo_num not in TIPOS_TRANSFERENCIA:
        print("❌ Tipo inválido")
        tipo_num = vd.validateInt("Seleccione tipo de transferencia (1-4): ")
    
    tipo_transferencia = TIPOS_TRANSFERENCIA[tipo_num]
    
    # Datos adicionales según el tipo
    monto = 0
    duracion_prestamo = None
    
    if tipo_num == 1:  # Venta definitiva
        monto = vd.validateInt("Monto de la transferencia (USD): ")
    elif tipo_num == 2:  # Préstamo
        duracion_prestamo = vd.validateInt("Duración del préstamo (meses): ")
    
    # Confirmar transferencia
    print(f"\n📋 RESUMEN DE TRANSFERENCIA:")
    print(f"   Jugador: {jugador['nombre']} (#{dorsal_actual} → #{nuevo_dorsal})")
    print(f"   De: {equipo_origen['nombre'] if equipo_origen else 'Sin equipo'}")
    print(f"   A: {equipo_destino['nombre']}")
    print(f"   Tipo: {tipo_transferencia}")
    if monto > 0:
        print(f"   Monto: ${monto:,} USD")
    if duracion_prestamo:
        print(f"   Duración: {duracion_prestamo} meses")
    
    confirmacion = input("\n¿Confirmar transferencia? (s/n): ").lower()
    if confirmacion != 's':
        print("❌ Transferencia cancelada")
        return
    
    # Ejecutar transferencia
    id_transferencia = cf.obtener_siguiente_id(ARCHIVO_TRANSFERENCIAS, "TR")
    
    # Registrar transferencia
    transferencia = {
        id_transferencia: {
            "jugador_id": id_jugador,
            "jugador_nombre": jugador['nombre'],
            "equipo_origen_id": equipo_origen_id,
            "equipo_origen_nombre": equipo_origen['nombre'] if equipo_origen else "Sin equipo",
            "equipo_destino_id": id_equipo_destino,
            "equipo_destino_nombre": equipo_destino['nombre'],
            "tipo": tipo_transferencia,
            "dorsal_anterior": dorsal_actual,
            "dorsal_nuevo": nuevo_dorsal,
            "monto": monto,
            "duracion_prestamo": duracion_prestamo,
            "fecha_transferencia": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "estado": "Completada"
        }
    }
    
    # Guardar transferencia
    if not cf.updateJson(ARCHIVO_TRANSFERENCIAS, transferencia):
        print("❌ Error al registrar la transferencia")
        return
    
    # Actualizar jugador
    if not actualizar_jugador_transferencia(id_jugador, id_equipo_destino, nuevo_dorsal):
        print("❌ Error al actualizar datos del jugador")
        return
    
    print(f"\n✅ Transferencia completada exitosamente!")
    print(f"   ID de transferencia: {id_transferencia}")
    print(f"   {jugador['nombre']} ahora juega en {equipo_destino['nombre']}")

def actualizar_jugador_transferencia(id_jugador: str, nuevo_equipo_id: str, nuevo_dorsal: int):
    """Actualiza los datos del jugador tras una transferencia"""
    jugadores = cf.readJson("data/jugadores.json")
    
    if id_jugador not in jugadores:
        return False
    
    # Actualizar datos del jugador
    jugadores[id_jugador]["equipo_id"] = nuevo_equipo_id
    jugadores[id_jugador]["dorsal"] = nuevo_dorsal
    
    # Actualizar historial
    historial = jugadores[id_jugador].get("historial_equipos", [])
    if nuevo_equipo_id not in historial:
        historial.append(nuevo_equipo_id)
        jugadores[id_jugador]["historial_equipos"] = historial
    
    jugadores[id_jugador]["ultima_transferencia"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    cf.writeJson("data/jugadores.json", jugadores)
    return True

def listar_transferencias():
    """Lista todas las transferencias realizadas"""
    print("🔄 HISTORIAL DE TRANSFERENCIAS")
    print("-" * 60)
    
    transferencias = cf.readJson(ARCHIVO_TRANSFERENCIAS)
    
    if not transferencias:
        print("⚠️ No hay transferencias registradas")
        return
    
    print(f"{'ID':<8} {'JUGADOR':<20} {'ORIGEN':<15} {'DESTINO':<15} {'TIPO':<15}")
    print("-" * 73)
    
    # Ordenar por fecha (más recientes primero)
    transferencias_ordenadas = sorted(
        transferencias.items(),
        key=lambda x: x[1].get('fecha_transferencia', ''),
        reverse=True
    )
    
    for id_transfer, datos in transferencias_ordenadas:
        print(f"{id_transfer:<8} {datos['jugador_nombre']:<20} {datos['equipo_origen_nombre']:<15} {datos['equipo_destino_nombre']:<15} {datos['tipo']:<15}")
    
    print(f"\nTotal de transferencias: {len(transferencias)}")

def obtener_transferencias_por_jugador(id_jugador: str):
    """Obtiene todas las transferencias de un jugador específico"""
    transferencias = cf.readJson(ARCHIVO_TRANSFERENCIAS)
    return {k: v for k, v in transferencias.items() if v.get("jugador_id") == id_jugador}

def obtener_transferencias_por_equipo(id_equipo: str, tipo: str = "ambos"):
    """
    Obtiene transferencias de un equipo
    tipo: 'origen', 'destino' o 'ambos'
    """
    transferencias = cf.readJson(ARCHIVO_TRANSFERENCIAS)
    resultado = {}
    
    for k, v in transferencias.items():
        if tipo in ["origen", "ambos"] and v.get("equipo_origen_id") == id_equipo:
            resultado[k] = v
        elif tipo in ["destino", "ambos"] and v.get("equipo_destino_id") == id_equipo:
            resultado[k] = v
    
    return resultado

def mostrar_detalle_transferencia(id_transferencia: str):
    """Muestra información detallada de una transferencia"""
    transferencia = cf.buscar_por_id(ARCHIVO_TRANSFERENCIAS, id_transferencia)
    
    if not transferencia:
        print("❌ Transferencia no encontrada")
        return
    
    print(f"🔄 DETALLE DE TRANSFERENCIA - {id_transferencia}")
    print("-" * 50)
    print(f"Jugador: {transferencia['jugador_nombre']}")
    print(f"Equipo origen: {transferencia['equipo_origen_nombre']}")
    print(f"Equipo destino: {transferencia['equipo_destino_nombre']}")
    print(f"Tipo: {transferencia['tipo']}")
    print(f"Dorsal: #{transferencia['dorsal_anterior']} → #{transferencia['dorsal_nuevo']}")
    print(f"Fecha: {transferencia['fecha_transferencia']}")
    print(f"Estado: {transferencia['estado']}")
    
    if transferencia.get('monto', 0) > 0:
        print(f"Monto: ${transferencia['monto']:,} USD")
    
    if transferencia.get('duracion_prestamo'):
        print(f"Duración préstamo: {transferencia['duracion_prestamo']} meses")

def estadisticas_transferencias():
    """Genera estadísticas de transferencias"""
    transferencias = cf.readJson(ARCHIVO_TRANSFERENCIAS)
    
    if not transferencias:
        return {
            "total": 0,
            "por_tipo": {},
            "monto_total": 0,
            "promedio_monto": 0
        }
    
    stats = {
        "total": len(transferencias),
        "por_tipo": {},
        "monto_total": 0,
        "prestamos_activos": 0
    }
    
    for transfer in transferencias.values():
        tipo = transfer.get("tipo", "Desconocido")
        stats["por_tipo"][tipo] = stats["por_tipo"].get(tipo, 0) + 1
        stats["monto_total"] += transfer.get("monto", 0)
        
        if "préstamo" in tipo.lower():
            stats["prestamos_activos"] += 1
    
    stats["promedio_monto"] = stats["monto_total"] / stats["total"] if stats["total"] > 0 else 0
    
    return stats
=======
import os
import json
import datetime
from utils.screenControllers import limpiar_pantalla, pausar_pantalla

RUTA_JUGADORES_JSON = os.path.join("data", "jugadores.json")
RUTA_EQUIPOS_JSON = os.path.join("data", "equipos.json")
RUTA_TRANSFERENCIAS_JSON = os.path.join("data", "transferencias.json")

TIPOS_TRANSFERENCIA = [
    "Transferencia definitiva",
    "Cesión o préstamo",
    "Transferencia libre",
    "Cláusula de rescisión",
    "Intercambio de jugadores",
    "Transferencias de juveniles",
    "Co-propiedad",
    "Transferencia por subasta o tribunal"
]

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

def obtener_fecha_valida():
    while True:
        fecha_str = input("Ingrese la fecha de la transferencia (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha_str
        except ValueError:
            print("Error: Formato de fecha no válido. Por favor, use YYYY-MM-DD (ej: 2024-07-28).")

def subMenuTransferencias():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Transferencias ---")
        print("1. Realizar una nueva transferencia")
        print("2. Ver historial de transferencias")
        print("3. Volver al Menú Principal")
        print("---------------------------------")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            transferir_jugador()
        elif opcion == '2':
            ver_transferencias()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar_pantalla()

def transferir_jugador():
    jugadores = cargar_datos(RUTA_JUGADORES_JSON)
    equipos = cargar_datos(RUTA_EQUIPOS_JSON)
    transferencias = cargar_datos(RUTA_TRANSFERENCIAS_JSON)

    if not jugadores or not equipos:
        print("Error: Se necesitan datos de jugadores y equipos para realizar una transferencia.")
        pausar_pantalla()
        return

    mapa_equipos = {e['id']: e['nombre'] for e in equipos}

    while True:
        limpiar_pantalla()
        print("--- Jugadores Disponibles para Transferir ---")
        for jugador in jugadores:
            nombre_equipo_actual = mapa_equipos.get(jugador.get('equipo_id'), "Sin Equipo")
            print(f"ID: {jugador['id']} | Nombre: {jugador['nombre']} | Equipo: {nombre_equipo_actual}")
        print("---------------------------------------------")
        
        try:
            jugador_id = int(input("Ingrese el ID del jugador a transferir: "))
            jugador_a_transferir = next((j for j in jugadores if j['id'] == jugador_id), None)
            if jugador_a_transferir:
                break
            else:
                print("\nError: No se encontró un jugador con ese ID. Intente de nuevo.")
                pausar_pantalla()
        except ValueError:
            print("\nError: Por favor, ingrese un número de ID válido. Intente de nuevo.")
            pausar_pantalla()

    equipo_origen_id = jugador_a_transferir['equipo_id']
    nombre_origen = mapa_equipos.get(equipo_origen_id, "Desconocido")
    
    limpiar_pantalla()
    print(f"Jugador seleccionado: {jugador_a_transferir['nombre']}")
    print(f"Equipo de Origen: {nombre_origen} (ID: {equipo_origen_id})")

    equipos_disponibles = [e for e in equipos if e['id'] != equipo_origen_id]
    
    while True:
        print("\n--- Equipos de Destino Disponibles ---")
        for equipo in equipos_disponibles:
            print(f"ID: {equipo['id']} - Nombre: {equipo['nombre']}")
        print("------------------------------------")
        try:
            equipo_destino_id = int(input("Ingrese el ID del nuevo equipo: "))
            if equipo_destino_id in [e['id'] for e in equipos_disponibles]:
                break
            else:
                print("Error: ID de equipo no válido o es el mismo equipo de origen.")
                pausar_pantalla()
                limpiar_pantalla()
        except ValueError:
            print("Error: Por favor, ingrese un número de ID válido.")
            pausar_pantalla()
            limpiar_pantalla()

    tipo_transferencia = ""
    while True:
        limpiar_pantalla()
        print("--- Tipos de Transferencia Disponibles ---")
        for i, tipo in enumerate(TIPOS_TRANSFERENCIA):
            print(f"{i + 1}. {tipo}")
        print("----------------------------------------")
        try:
            opcion_tipo = int(input("Seleccione el número del tipo de transferencia: "))
            if 1 <= opcion_tipo <= len(TIPOS_TRANSFERENCIA):
                tipo_transferencia = TIPOS_TRANSFERENCIA[opcion_tipo - 1]
                break
            else:
                print("Error: Número de opción no válido. Intente de nuevo.")
                pausar_pantalla()
        except ValueError:
            print("Error: Debe ingresar un número. Intente de nuevo.")
            pausar_pantalla()

    fecha_transferencia = obtener_fecha_valida()
    
    nueva_transferencia = {
        "jugador_id": jugador_id,
        "equipo_origen_id": equipo_origen_id,
        "equipo_destino_id": equipo_destino_id,
        "tipo": tipo_transferencia,
        "fecha": fecha_transferencia
    }
    transferencias.append(nueva_transferencia)
    guardar_datos(transferencias, RUTA_TRANSFERENCIAS_JSON)

    for jugador in jugadores:
        if jugador['id'] == jugador_id:
            jugador['equipo_id'] = equipo_destino_id
            break
    guardar_datos(jugadores, RUTA_JUGADORES_JSON)
    
    print("\n¡Transferencia completada y registrada exitosamente!")
    pausar_pantalla()


def ver_transferencias():
    limpiar_pantalla()
    print("--- Historial de Transferencias Realizadas ---")

    transferencias = cargar_datos(RUTA_TRANSFERENCIAS_JSON)
    jugadores = cargar_datos(RUTA_JUGADORES_JSON)
    equipos = cargar_datos(RUTA_EQUIPOS_JSON)
    
    if not transferencias:
        print("No hay transferencias registradas aún.")
    else:
        mapa_jugadores = {j['id']: j['nombre'] for j in jugadores}
        mapa_equipos = {e['id']: e['nombre'] for e in equipos}

        for trans in transferencias:
            nombre_jugador = mapa_jugadores.get(trans['jugador_id'], "Jugador Desconocido")
            nombre_origen = mapa_equipos.get(trans['equipo_origen_id'], "Equipo Origen Desconocido")
            nombre_destino = mapa_equipos.get(trans['equipo_destino_id'], "Equipo Destino Desconocido")

            print(f"  Fecha: {trans['fecha']}")
            print(f"  Jugador: {nombre_jugador} (ID: {trans['jugador_id']})")
            print(f"  Origen: {nombre_origen} -> Destino: {nombre_destino}")
            print(f"  Tipo: {trans['tipo']}")
            print("-" * 40)
    print("Presione Enter para continuar...")
    pausar_pantalla()
>>>>>>> 5c19e46 (primer)
