import json
import os
from typing import Dict, List, Optional

def readJson(archivo: str) -> Dict:
    """Lee un archivo JSON y retorna su contenido"""
    try:
        with open(archivo, "r", encoding="utf-8") as cf:
            return json.load(cf)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def writeJson(archivo: str, data: Dict) -> None:
    """Escribe datos en un archivo JSON"""
    # Crear directorio si no existe
    directorio = os.path.dirname(archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)
    
    with open(archivo, "w", encoding="utf-8") as cf:
        json.dump(data, cf, indent=4, ensure_ascii=False)

def updateJson(archivo: str, data: Dict, path: Optional[List[str]] = None) -> bool:
    """Actualiza un archivo JSON con nuevos datos"""
    try:
        currentData = readJson(archivo)

        if not path:
            currentData.update(data)
        else:
            current = currentData
            for key in path[:-1]:
                current = current.setdefault(key, {})
            if path:
                current.setdefault(path[-1], {}).update(data)
        
        writeJson(archivo, currentData)
        return True
    except Exception as e:
        print(f"Error al actualizar JSON: {e}")
        return False

def deleteJson(archivo: str, path: List[str]) -> bool:
    """Elimina una entrada específica del archivo JSON"""
    try:
        data = readJson(archivo)
        if not data:
            return False
        
        current = data
        for key in path[:-1]:
            if key not in current:
                return False
            current = current[key]
        
        if path and path[-1] in current:
            del current[path[-1]]
            writeJson(archivo, data)
            return True
        return False
    except Exception as e:
        print(f"Error al eliminar del JSON: {e}")
        return False

def initializeJson(archivo: str, initialStructure: Dict) -> None:
    """Inicializa un archivo JSON con una estructura inicial si no existe"""
    if not os.path.isfile(archivo):
        writeJson(archivo, initialStructure)
    else:
        currentData = readJson(archivo)
        updated = False
        for key, value in initialStructure.items():
            if key not in currentData:
                currentData[key] = value
                updated = True
        if updated:
            writeJson(archivo, currentData)

def buscar_por_id(archivo: str, id_buscar: str) -> Optional[Dict]:
    """Busca un elemento por ID en el archivo JSON"""
    data = readJson(archivo)
    return data.get(id_buscar)

def obtener_siguiente_id(archivo: str, prefijo: str = "") -> str:
    """Genera el siguiente ID disponible"""
    import random
    data = readJson(archivo)
    while True:
        nuevo_id = f"{prefijo}{random.randint(1000, 9999)}"
        if nuevo_id not in data:
            return nuevo_id