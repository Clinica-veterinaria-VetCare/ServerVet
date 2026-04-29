"""
Módulo: services/dueno_service.py
Descripción: Servicio de negocio para Dueños
"""

from dao.dueno_dao import DuenoDAO, Dueno
from services.validator_service import ValidatorService


class DuenoService:
    """Servicio de negocio para Dueños"""
    
    def __init__(self):
        self.dao = DuenoDAO()
        self.validator = ValidatorService
    
    def registrar_dueno(self, nombre: str, telefono: str, email: str = None, direccion: str = None) -> int:
        # Validaciones
        valido, error = self.validator.validar_nombre(nombre, "Nombre del dueño")
        if not valido:
            raise ValueError(error)
        
        valido, error = self.validator.validar_telefono(telefono)
        if not valido:
            raise ValueError(error)
        
        if email:
            valido, error = self.validator.validar_email(email)
            if not valido:
                raise ValueError(error)
        
        # Limpiar datos
        nombre = nombre.strip().title()
        telefono = ''.join(c for c in telefono if c.isdigit())
        
        # Crear entidad
        dueno = Dueno(nombre=nombre, telefono=telefono, email=email, direccion=direccion)
        return self.dao.create(dueno)
    
    def obtener_todos(self):
        return self.dao.get_all()
    
    def obtener_por_id(self, dueno_id: int):
        return self.dao.get_by_id(dueno_id)
    
    def buscar_por_nombre(self, termino: str):
        if not termino or len(termino) < 2:
            return []
        return self.dao.search(termino, ['nombre'])