"""
Módulo: utils/helpers.py
Descripción: Funciones auxiliares reutilizables
"""

from datetime import datetime


def format_phone(phone: str) -> str:
    """Formatea número de teléfono"""
    digits = ''.join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return digits


def format_date(date_obj, fmt: str = "%d/%m/%Y") -> str:
    """Formatea una fecha"""
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
    return date_obj.strftime(fmt)


def validate_numeric(value, min_val=None, max_val=None):
    """Valida que un valor sea numérico y esté en rango"""
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except (ValueError, TypeError):
        return False