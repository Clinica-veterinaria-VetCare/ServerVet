"""
Módulo: dao/cita_dao.py
Descripción: Data Access Object para la entidad Cita
"""

from typing import Optional, List, Dict, Any
from dao.base_dao import BaseDAO
from datetime import datetime, date
from enum import Enum


class EstadoCita(Enum):
    AGENDADA = "Agendada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"


class Cita:
    """Entidad Cita Veterinaria"""
    
    def __init__(self, mascota_id: int, veterinario_id: int, fecha_hora: datetime,
                motivo: Optional[str] = None, estado: str = EstadoCita.AGENDADA.value,
                id: Optional[int] = None):
        self.id = id
        self.mascota_id = mascota_id
        self.veterinario_id = veterinario_id
        self.fecha_hora = fecha_hora
        self.motivo = motivo
        self.estado = estado
    
    def __str__(self) -> str:
        return f"Cita {self.id}: {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"


class CitaDAO(BaseDAO[Cita]):
    
    def __init__(self):
        super().__init__()
        self.table_name = "citas"
    
    def _map_to_entity(self, row: Dict[str, Any]) -> Cita:
        return Cita(
            id=row['id'],
            mascota_id=row['mascota_id'],
            veterinario_id=row['veterinario_id'],
            fecha_hora=row['fecha_hora'],
            motivo=row.get('motivo'),
            estado=row['estado']
        )
    
    def _map_to_dict(self, entity: Cita) -> Dict[str, Any]:
        return {
            'mascota_id': entity.mascota_id,
            'veterinario_id': entity.veterinario_id,
            'fecha_hora': entity.fecha_hora,
            'motivo': entity.motivo,
            'estado': entity.estado
        }
    
    def has_conflict(self, veterinario_id: int, fecha_hora: datetime) -> bool:
        query = """
            SELECT COUNT(*) as total FROM citas 
            WHERE veterinario_id = %s AND fecha_hora = %s AND estado != %s
        """
        result = self.db.execute_query(query, (veterinario_id, fecha_hora, EstadoCita.CANCELADA.value))
        return result[0]['total'] > 0
    
    def get_upcoming(self, limit: int = 10) -> List[Dict[str, Any]]:
        query = """
            SELECT c.*, m.nombre as mascota_nombre, v.nombre as veterinario_nombre
            FROM citas c
            JOIN mascotas m ON c.mascota_id = m.id
            JOIN veterinarios v ON c.veterinario_id = v.id
            WHERE c.fecha_hora >= NOW() AND c.estado = %s
            ORDER BY c.fecha_hora
            LIMIT %s
        """
        return self.db.execute_query(query, (EstadoCita.AGENDADA.value, limit))