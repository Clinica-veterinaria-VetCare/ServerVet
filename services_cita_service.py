"""
Módulo: services/cita_service.py
Descripción: Servicio de negocio para Citas
"""

from dao.cita_dao import CitaDAO, Cita, EstadoCita
from dao.mascota_dao import MascotaDAO
from datetime import datetime
from services.validator_service import ValidatorService


class CitaService:
    """Servicio de negocio para Citas"""
    
    def __init__(self):
        self.dao = CitaDAO()
        self.mascota_dao = MascotaDAO()
    
    def agendar_cita(self, mascota_id: int, veterinario_id: int, 
                     fecha_hora: datetime, motivo: str = None) -> int:
        # Validar mascota existe
        mascota = self.mascota_dao.get_by_id(mascota_id)
        if not mascota:
            raise ValueError("La mascota especificada no existe")
        
        # Validar fecha futura
        if fecha_hora <= datetime.now():
            raise ValueError("La fecha de la cita debe ser futura")
        
        cita = Cita(mascota_id=mascota_id, veterinario_id=veterinario_id,
                    fecha_hora=fecha_hora, motivo=motivo)
        return self.dao.create(cita)
    
    def obtener_proximas_citas(self, limit=10):
        return self.dao.get_upcoming(limit)
    
    def cancelar_cita(self, cita_id: int):
        return self.dao.cancel(cita_id)
    
    def completar_cita(self, cita_id: int):
        return self.dao.complete(cita_id)