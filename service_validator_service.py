"""
Módulo: services/validator_service.py
Descripción: Servicio centralizado de validaciones
"""

import re
from typing import Tuple, Optional


class ValidatorService:
    """Servicio de validaciones centralizado"""
    
    ESPECIES_VALIDAS = ['Perro', 'Gato', 'Conejo', 'Hamster', 'Ave', 'Reptil', 'Otro']
    
    @classmethod
    def validar_nombre(cls, nombre: str, campo: str = "Nombre") -> Tuple[bool, Optional[str]]:
        if not nombre or not nombre.strip():
            return False, f"{campo} es obligatorio"
        
        nombre_limpio = nombre.strip()
        if len(nombre_limpio) < 2:
            return False, f"{campo} debe tener al menos 2 caracteres"
        
        if len(nombre_limpio) > 100:
            return False, f"{campo} no puede exceder 100 caracteres"
        
        if not re.match(r'^[a-zA-ZáéíóúñÑüÜ\s]+$', nombre_limpio):
            return False, f"{campo} solo puede contener letras y espacios"
        
        return True, None
    
    @classmethod
    def validar_telefono(cls, telefono: str) -> Tuple[bool, Optional[str]]:
        if not telefono or not telefono.strip():
            return False, "Teléfono es obligatorio"
        
        telefono_limpio = ''.join(c for c in telefono if c.isdigit())
        if len(telefono_limpio) < 7:
            return False, "Teléfono debe tener al menos 7 dígitos"
        
        if len(telefono_limpio) > 15:
            return False, "Teléfono no puede exceder 15 dígitos"
        
        return True, None
    
    @classmethod
    def validar_email(cls, email: str) -> Tuple[bool, Optional[str]]:
        if not email:
            return True, None  # Email es opcional
        
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            return False, "Formato de email inválido"
        
        return True, None
    
    @classmethod
    def validar_especie(cls, especie: str) -> Tuple[bool, Optional[str]]:
        if especie not in cls.ESPECIES_VALIDAS:
            return False, f"Especie no válida. Opciones: {', '.join(cls.ESPECIES_VALIDAS)}"
        return True, None