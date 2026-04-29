"""
Módulo: services/mascota_service.py
Descripción: Servicio de negocio para Mascotas
"""

from dao.mascota_dao import MascotaDAO, Mascota
from dao.dueno_dao import DuenoDAO
from services.validator_service import ValidatorService


class MascotaService:
    """Servicio de negocio para Mascotas"""
    
    def __init__(self):
        self.dao = MascotaDAO()
        self.dueno_dao = DuenoDAO()
        self.validator = ValidatorService
    
    def registrar_mascota(self, nombre: str, especie: str, dueno_id: int, 
                          raza: str = None, edad: int = None, peso: float = None) -> int:
        # Validar dueño existe
        dueno = self.dueno_dao.get_by_id(dueno_id)
        if not dueno:
            raise ValueError("El dueño especificado no existe")
        
        # Validar nombre
        valido, error = self.validator.validar_nombre(nombre, "Nombre de la mascota")
        if not valido:
            raise ValueError(error)
        
        # Validar especie
        valido, error = self.validator.validar_especie(especie)
        if not valido:
            raise ValueError(error)
        
        # Validar edad
        if edad is not None and (edad < 0 or edad > 50):
            raise ValueError("La edad debe estar entre 0 y 50 años")
        
        # Validar peso
        if peso is not None and (peso < 0 or peso > 200):
            raise ValueError("El peso debe estar entre 0 y 200 kg")
        
        nombre = nombre.strip().title()
        
        mascota = Mascota(nombre=nombre, especie=especie, dueno_id=dueno_id,
                          raza=raza, edad=edad, peso=peso)
        return self.dao.create(mascota)
    
    def obtener_por_dueno(self, dueno_id: int):
        return self.dao.get_by_dueno(dueno_id)
    
    def obtener_todas(self):
        return self.dao.get_all()