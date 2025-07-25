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