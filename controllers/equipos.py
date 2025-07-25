import utils.corefiles as cf
import utils.validaData as vd
from datetime import datetime

ARCHIVO_EQUIPOS = "data/equipos.json"

def registrar_equipo():
    """Registra un nuevo equipo en el sistema"""
    print("📘 REGISTRO DE EQUIPO")
    print("-" * 30)
    
    # Generar ID único
    id_equipo = cf.obtener_siguiente_id(ARCHIVO_EQUIPOS, "EQ")
    
    # Solicitar datos del equipo
    nombre = vd.validatetext("Nombre del equipo: ")
    pais = vd.validatetext("País: ")
    
    print("\nFecha de fundación:")
    dia = vd.validateInt("Día (1-31): ")
    mes = vd.validateInt("Mes (1-12): ")
    año = vd.validateInt("Año: ")
    
    try:
        fecha_fundacion = datetime(año, mes, dia).strftime("%d/%m/%Y")
    except ValueError:
        print("❌ Fecha inválida. Se usará la fecha actual.")
        fecha_fundacion = datetime.now().strftime("%d/%m/%Y")
    
    ciudad = vd.validatetext("Ciudad: ")
    estadio = vd.validatetext("Estadio: ")
    
    # Crear diccionario del equipo
    equipo = {
        id_equipo: {
            "nombre": nombre,
            "pais": pais,
            "fecha_fundacion": fecha_fundacion,
            "ciudad": ciudad,
            "estadio": estadio,
            "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "activo": True
        }
    }
    
    # Guardar en archivo JSON
    if cf.updateJson(ARCHIVO_EQUIPOS, equipo):
        print(f"\n✅ Equipo '{nombre}' registrado exitosamente con ID: {id_equipo}")
    else:
        print("❌ Error al registrar el equipo")

def listar_equipos():
    """Lista todos los equipos registrados"""
    print("📋 LISTA DE EQUIPOS REGISTRADOS")
    print("-" * 50)
    
    equipos = cf.readJson(ARCHIVO_EQUIPOS)
    
    if not equipos:
        print("⚠️ No hay equipos registrados")
        return
    
    print(f"{'ID':<8} {'NOMBRE':<20} {'PAÍS':<15} {'CIUDAD':<15}")
    print("-" * 58)
    
    for id_equipo, datos in equipos.items():
        if datos.get("activo", True):
            print(f"{id_equipo:<8} {datos['nombre']:<20} {datos['pais']:<15} {datos['ciudad']:<15}")
    
    print(f"\nTotal de equipos activos: {len([e for e in equipos.values() if e.get('activo', True)])}")

def obtener_equipo_por_id(id_equipo: str):
    """Obtiene un equipo específico por su ID"""
    equipo = cf.buscar_por_id(ARCHIVO_EQUIPOS, id_equipo)
    return equipo if equipo and equipo.get("activo", True) else None

def obtener_todos_equipos():
    """Retorna todos los equipos activos"""
    equipos = cf.readJson(ARCHIVO_EQUIPOS)
    return {k: v for k, v in equipos.items() if v.get("activo", True)}

def mostrar_detalle_equipo(id_equipo: str):
    """Muestra información detallada de un equipo"""
    equipo = obtener_equipo_por_id(id_equipo)
    
    if not equipo:
        print("❌ Equipo no encontrado")
        return
    
    print(f"📘 DETALLES DEL EQUIPO - {equipo['nombre']}")
    print("-" * 40)
    print(f"ID: {id_equipo}")
    print(f"Nombre: {equipo['nombre']}")
    print(f"País: {equipo['pais']}")
    print(f"Ciudad: {equipo['ciudad']}")
    print(f"Estadio: {equipo['estadio']}")
    print(f"Fundación: {equipo['fecha_fundacion']}")
    print(f"Registrado: {equipo['fecha_registro']}")

def desactivar_equipo(id_equipo: str):
    """Desactiva un equipo (soft delete)"""
    equipos = cf.readJson(ARCHIVO_EQUIPOS)
    
    if id_equipo in equipos:
        equipos[id_equipo]["activo"] = False
        equipos[id_equipo]["fecha_desactivacion"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cf.writeJson(ARCHIVO_EQUIPOS, equipos)
        return True
    return False