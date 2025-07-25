import os
import sys

def validateInt(msg: str) -> int:
    """Valida entrada de números enteros"""
    while True:
        try:
            x = int(input(msg))
            return x
        except ValueError:
            print("❌ ERROR: Debe ingresar un número entero válido")
            pausar_entrada()
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return 0

def validatetext(msg: str) -> str:
    """Valida entrada de texto (solo letras y espacios)"""
    while True:
        try:
            x = input(msg).strip()
            
            if not x:
                print("❌ ERROR: El campo no puede estar vacío")
                pausar_entrada()
                continue
            
            if all(c.isalpha() or c.isspace() for c in x):
                return x
            else:
                print("❌ ERROR: Solo se permiten letras y espacios")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return ""

def validateFloat(msg: str) -> float:
    """Valida entrada de números decimales"""
    while True:
        try:
            x = float(input(msg))
            return x
        except ValueError:
            print("❌ ERROR: Debe ingresar un número decimal válido")
            pausar_entrada()
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return 0.0

def validateEmail(msg: str) -> str:
    """Valida formato de email básico"""
    import re
    
    while True:
        try:
            email = input(msg).strip()
            
            if not email:
                print("❌ ERROR: El email no puede estar vacío")
                pausar_entrada()
                continue
            
            # Validación básica de email
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(patron, email):
                return email
            else:
                print("❌ ERROR: Formato de email inválido")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return ""

def validatePhone(msg: str) -> str:
    """Valida número de teléfono"""
    while True:
        try:
            phone = input(msg).strip()
            
            if not phone:
                print("❌ ERROR: El teléfono no puede estar vacío")
                pausar_entrada()
                continue
            
            # Permitir números, espacios, guiones y paréntesis
            if all(c.isdigit() or c in ' -()' for c in phone) and len(phone) >= 7:
                return phone
            else:
                print("❌ ERROR: Formato de teléfono inválido (mínimo 7 dígitos)")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return ""

def validateRange(msg: str, min_val: int, max_val: int) -> int:
    """Valida número entero dentro de un rango específico"""
    while True:
        try:
            x = int(input(f"{msg} ({min_val}-{max_val}): "))
            
            if min_val <= x <= max_val:
                return x
            else:
                print(f"❌ ERROR: El valor debe estar entre {min_val} y {max_val}")
                pausar_entrada()
                
        except ValueError:
            print("❌ ERROR: Debe ingresar un número válido")
            pausar_entrada()
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return min_val

def validateAlphanumeric(msg: str) -> str:
    """Valida texto alfanumérico (letras, números y espacios)"""
    while True:
        try:
            x = input(msg).strip()
            
            if not x:
                print("❌ ERROR: El campo no puede estar vacío")
                pausar_entrada()
                continue
            
            if all(c.isalnum() or c.isspace() for c in x):
                return x
            else:
                print("❌ ERROR: Solo se permiten letras, números y espacios")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return ""

def validateDate(msg: str) -> tuple:
    """Valida fecha en formato día, mes, año"""
    print(f"{msg}")
    
    while True:
        try:
            dia = validateRange("Día", 1, 31)
            mes = validateRange("Mes", 1, 12)
            año = validateRange("Año", 1900, 2030)
            
            # Validación básica de fecha
            if mes in [4, 6, 9, 11] and dia > 30:
                print("❌ ERROR: Este mes solo tiene 30 días")
                continue
            elif mes == 2:
                # Año bisiesto básico
                if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0):
                    if dia > 29:
                        print("❌ ERROR: Febrero en año bisiesto tiene máximo 29 días")
                        continue
                else:
                    if dia > 28:
                        print("❌ ERROR: Febrero tiene máximo 28 días")
                        continue
            
            return (dia, mes, año)
            
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            from datetime import datetime
            now = datetime.now()
            return (now.day, now.month, now.year)

def validateYesNo(msg: str) -> bool:
    """Valida respuesta sí/no"""
    while True:
        try:
            respuesta = input(f"{msg} (s/n): ").lower().strip()
            
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                return True
            elif respuesta in ['n', 'no']:
                return False
            else:
                print("❌ ERROR: Responda 's' para sí o 'n' para no")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return False

def validateOption(msg: str, opciones: list) -> str:
    """Valida que la opción seleccionada esté en la lista de opciones válidas"""
    while True:
        try:
            print(f"\n{msg}")
            for i, opcion in enumerate(opciones, 1):
                print(f"{i}. {opcion}")
            
            seleccion = validateRange("Seleccione una opción", 1, len(opciones))
            return opciones[seleccion - 1]
            
        except (IndexError, KeyboardInterrupt):
            print("❌ ERROR: Selección inválida")
            pausar_entrada()

def validateID(msg: str) -> str:
    """Valida ID alfanumérico"""
    while True:
        try:
            id_value = input(msg).strip().upper()
            
            if not id_value:
                print("❌ ERROR: El ID no puede estar vacío")
                pausar_entrada()
                continue
            
            if len(id_value) >= 2 and all(c.isalnum() for c in id_value):
                return id_value
            else:
                print("❌ ERROR: ID debe ser alfanumérico y tener al menos 2 caracteres")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return ""

def validatePositiveNumber(msg: str) -> int:
    """Valida número entero positivo"""
    while True:
        try:
            x = int(input(msg))
            if x > 0:
                return x
            else:
                print("❌ ERROR: El número debe ser positivo (mayor a 0)")
                pausar_entrada()
                
        except ValueError:
            print("❌ ERROR: Debe ingresar un número entero válido")
            pausar_entrada()
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return 1

def pausar_entrada():
    """Pausa para mostrar errores"""
    if sys.platform == "linux" or sys.platform == "darwin":
        input("Presione Enter para continuar...")
    else:
        os.system('pause')

# Funciones adicionales para casos específicos del torneo

def validatePlayerName(msg: str) -> str:
    """Valida nombre de jugador (permite guiones y apostrofes)"""
    while True:
        try:
            name = input(msg).strip()
            
            if not name:
                print("❌ ERROR: El nombre no puede estar vacío")
                pausar_entrada()
                continue
            
            # Permitir letras, espacios, guiones y apostrofes
            if all(c.isalpha() or c in " '-" for c in name) and len(name) >= 2:
                return name.title()  # Formato título
            else:
                print("❌ ERROR: Nombre inválido (solo letras, espacios, guiones y apostrofes)")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return ""

def validateTeamName(msg: str) -> str:
    """Valida nombre de equipo"""
    while True:
        try:
            name = input(msg).strip()
            
            if not name:
                print("❌ ERROR: El nombre del equipo no puede estar vacío")
                pausar_entrada()
                continue
            
            if len(name) >= 2 and len(name) <= 50:
                return name.title()
            else:
                print("❌ ERROR: El nombre debe tener entre 2 y 50 caracteres")
                pausar_entrada()
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return ""