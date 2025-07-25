import utils.corefiles as cf
import controllers.equipos as eq
import controllers.jugadores as jg
import controllers.transferencias as tr
from collections import Counter

def mostrar_estadisticas():
    """Muestra estadísticas generales del sistema"""
    print("📊 ESTADÍSTICAS GENERALES DEL TORNEO")
    print("=" * 50)
    
    # Estadísticas básicas
    equipos = eq.obtener_todos_equipos()
    jugadores = cf.readJson("data/jugadores.json")
    transferencias = cf.readJson("data/transferencias.json")
    
    jugadores_activos = {k: v for k, v in jugadores.items() if v.get("activo", True)}
    
    print(f"🏟️  Total de equipos registrados: {len(equipos)}")
    print(f"👥 Total de jugadores activos: {len(jugadores_activos)}")
    print(f"🔄 Total de transferencias: {len(transferencias)}")
    
    if equipos:
        mostrar_estadisticas_equipos(equipos, jugadores_activos)
    
    if jugadores_activos:
        mostrar_estadisticas_jugadores(jugadores_activos, equipos)
    
    if transferencias:
        mostrar_estadisticas_transferencias()

def mostrar_estadisticas_equipos(equipos, jugadores_activos):
    """Muestra estadísticas específicas de equipos"""
    print(f"\n🏟️  ESTADÍSTICAS DE EQUIPOS")
    print("-" * 30)
    
    # Jugadores por equipo
    jugadores_por_equipo = {}
    for jugador in jugadores_activos.values():
        equipo_id = jugador.get("equipo_id")
        if equipo_id:
            jugadores_por_equipo[equipo_id] = jugadores_por_equipo.get(equipo_id, 0) + 1
    
    # Equipo con más jugadores
    if jugadores_por_equipo:
        equipo_max_id = max(jugadores_por_equipo, key=jugadores_por_equipo.get)
        equipo_max = equipos.get(equipo_max_id, {})
        max_jugadores = jugadores_por_equipo[equipo_max_id]
        
        print(f"   Equipo con más jugadores: {equipo_max.get('nombre', 'N/A')} ({max_jugadores} jugadores)")
    
    # Promedio de jugadores por equipo
    if jugadores_por_equipo:
        promedio = sum(jugadores_por_equipo.values()) / len(equipos)
        print(f"   Promedio de jugadores por equipo: {promedio:.1f}")
    
    # Equipos por país
    paises = [equipo.get("pais", "N/A") for equipo in equipos.values()]
    conteo_paises = Counter(paises)
    
    print(f"   Países representados: {len(conteo_paises)}")
    print("   Top 3 países:")
    for pais, cantidad in conteo_paises.most_common(3):
        print(f"     • {pais}: {cantidad} equipos")
    
    # Detalle por equipo
    print(f"\n   📋 DETALLE POR EQUIPO:")
    print(f"   {'EQUIPO':<20} {'PAÍS':<15} {'JUGADORES':<10}")
    print("   " + "-" * 45)
    
    for id_equipo, datos in equipos.items():
        num_jugadores = jugadores_por_equipo.get(id_equipo, 0)
        print(f"   {datos['nombre']:<20} {datos['pais']:<15} {num_jugadores:<10}")

def mostrar_estadisticas_jugadores(jugadores_activos, equipos):
    """Muestra estadísticas específicas de jugadores"""
    print(f"\n👥 ESTADÍSTICAS DE JUGADORES")
    print("-" * 32)
    
    # Edades
    edades = [j.get("edad", 0) for j in jugadores_activos.values() if j.get("edad")]
    if edades:
        edad_promedio = sum(edades) / len(edades)
        edad_min = min(edades)
        edad_max = max(edades)
        
        print(f"   Edad promedio: {edad_promedio:.1f} años")
        print(f"   Jugador más joven: {edad_min} años")
        print(f"   Jugador más veterano: {edad_max} años")
    
    # Posiciones
    posiciones = [j.get("posicion", "N/A") for j in jugadores_activos.values()]
    conteo_posiciones = Counter(posiciones)
    
    print(f"\n   📊 DISTRIBUCIÓN POR POSICIONES:")
    for posicion, cantidad in conteo_posiciones.most_common():
        porcentaje = (cantidad / len(jugadores_activos)) * 100
        print(f"     • {posicion}: {cantidad} ({porcentaje:.1f}%)")
    
    # Nacionalidades
    nacionalidades = [j.get("nacionalidad", "N/A") for j in jugadores_activos.values()]
    conteo_nacionalidades = Counter(nacionalidades)
    
    print(f"\n   🌍 NACIONALIDADES (Top 5):")
    for nacionalidad, cantidad in conteo_nacionalidades.most_common(5):
        print(f"     • {nacionalidad}: {cantidad} jugadores")

def mostrar_estadisticas_transferencias():
    """Muestra estadísticas de transferencias"""
    print(f"\n🔄 ESTADÍSTICAS DE TRANSFERENCIAS")
    print("-" * 35)
    
    stats = tr.estadisticas_transferencias()
    
    print(f"   Total de transferencias: {stats['total']}")
    print(f"   Monto total movido: ${stats['monto_total']:,} USD")
    
    if stats['total'] > 0:
        print(f"   Promedio por transferencia: ${stats['promedio_monto']:,.0f} USD")
    
    print(f"\n   📊 POR TIPO DE TRANSFERENCIA:")
    for tipo, cantidad in stats['por_tipo'].items():
        porcentaje = (cantidad / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"     • {tipo}: {cantidad} ({porcentaje:.1f}%)")

def generar_reporte_completo():
    """Genera un reporte completo del sistema"""
    print("📋 REPORTE COMPLETO DEL SISTEMA")
    print("=" * 60)
    
    from datetime import datetime
    print(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    mostrar_estadisticas()
    
    # Información adicional
    print(f"\n🔍 INFORMACIÓN DETALLADA")
    print("-" * 25)
    
    # Top jugadores por transferencias
    transferencias = cf.readJson("data/transferencias.json")
    if transferencias:
        jugadores_transferidos = {}
        for transfer in transferencias.values():
            jugador_id = transfer.get("jugador_id")
            jugador_nombre = transfer.get("jugador_nombre")
            if jugador_id:
                jugadores_transferidos[jugador_nombre] = jugadores_transferidos.get(jugador_nombre, 0) + 1
        
        if jugadores_transferidos:
            print(f"\n   👤 JUGADORES MÁS TRANSFERIDOS:")
            for nombre, cantidad in sorted(jugadores_transferidos.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"     • {nombre}: {cantidad} transferencias")
    
    # Equipos más activos en transferencias
    if transferencias:
        equipos_activos = {}
        for transfer in transferencias.values():
            origen = transfer.get("equipo_origen_nombre", "N/A")
            destino = transfer.get("equipo_destino_nombre", "N/A")
            
            equipos_activos[origen] = equipos_activos.get(origen, 0) + 1
            equipos_activos[destino] = equipos_activos.get(destino, 0) + 1
        
        print(f"\n   🏟️  EQUIPOS MÁS ACTIVOS EN TRANSFERENCIAS:")
        for equipo, cantidad in sorted(equipos_activos.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"     • {equipo}: {cantidad} movimientos")

def estadisticas_por_equipo(id_equipo: str):
    """Muestra estadísticas específicas de un equipo"""
    equipo = eq.obtener_equipo_por_id(id_equipo)
    if not equipo:
        print("❌ Equipo no encontrado")
        return
    
    print(f"📊 ESTADÍSTICAS DE {equipo['nombre'].upper()}")
    print("=" * 50)
    
    # Jugadores del equipo
    jugadores_equipo = jg.obtener_jugadores_por_equipo(id_equipo)
    print(f"👥 Jugadores actuales: {len(jugadores_equipo)}")
    
    if jugadores_equipo:
        # Estadísticas de jugadores
        edades = [j.get("edad", 0) for j in jugadores_equipo.values() if j.get("edad")]
        if edades:
            print(f"   Edad promedio del plantel: {sum(edades) / len(edades):.1f} años")
        
        # Posiciones
        posiciones = [j.get("posicion") for j in jugadores_equipo.values()]
        conteo_pos = Counter(posiciones)
        print(f"\n   📊 Composición del plantel:")
        for pos, cant in conteo_pos.items():
            print(f"     • {pos}: {cant}")
        
        # Nacionalidades en el equipo
        nacionalidades = [j.get("nacionalidad") for j in jugadores_equipo.values()]
        if len(set(nacionalidades)) > 1:
            print(f"\n   🌍 Diversidad: {len(set(nacionalidades))} nacionalidades")
    
    # Transferencias del equipo
    transferencias_in = tr.obtener_transferencias_por_equipo(id_equipo, "destino")
    transferencias_out = tr.obtener_transferencias_por_equipo(id_equipo, "origen")
    
    print(f"\n🔄 Actividad de transferencias:")
    print(f"   Fichajes: {len(transferencias_in)}")
    print(f"   Salidas: {len(transferencias_out)}")
    print(f"   Balance: {len(transferencias_in) - len(transferencias_out)}")

def exportar_estadisticas():
    """Exporta estadísticas a un archivo de texto"""
    from datetime import datetime
    
    nombre_archivo = f"estadisticas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            # Redirigir la salida al archivo
            import sys
            original_stdout = sys.stdout
            sys.stdout = archivo
            
            generar_reporte_completo()
            
            # Restaurar salida original
            sys.stdout = original_stdout
        
        print(f"✅ Estadísticas exportadas a: {nombre_archivo}")
        
    except Exception as e:
        print(f"❌ Error al exportar estadísticas: {e}")