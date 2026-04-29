"""
Módulo: dao/mascota_dao.py
Descripción: Data Access Object para la entidad Mascota
"""

from typing import Optional, List, Dict, Any
from dao.base_dao import BaseDAO
from datetime import datetime


class Mascota:
    """Entidad Mascota"""
    
    def __init__(self, nombre: str, especie: str, dueno_id: int,
                 raza: Optional[str] = None, edad: Optional[int] = None,
                 peso: Optional[float] = None, id: Optional[int] = None,
                 fecha_registro: Optional[datetime] = None, activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.peso = peso
        self.dueno_id = dueno_id
        self.fecha_registro = fecha_registro or datetime.now()
        self.activo = activo
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.especie})"


class MascotaDAO(BaseDAO[Mascota]):
    
    def __init__(self):
        super().__init__()
        self.table_name = "mascotas"
    
    def _map_to_entity(self, row: Dict[str, Any]) -> Mascota:
        return Mascota(
            id=row['id'],
            nombre=row['nombre'],
            especie=row['especie'],
            raza=row.get('raza'),
            edad=row.get('edad'),
            peso=row.get('peso'),
            dueno_id=row['dueno_id'],
            fecha_registro=row['fecha_registro'],
            activo=row['activo']
        )
    
    def _map_to_dict(self, entity: Mascota) -> Dict[str, Any]:
        return {
            'nombre': entity.nombre,
            'especie': entity.especie,
            'raza': entity.raza,
            'edad': entity.edad,
            'peso': entity.peso,
            'dueno_id': entity.dueno_id,
            'activo': entity.activo
        }
    
    def get_by_dueno(self, dueno_id: int) -> List[Mascota]:
        query = "SELECT * FROM mascotas WHERE dueno_id = %s AND activo = TRUE"
        results = self.db.execute_query(query, (dueno_id,))
        return [self._map_to_entity(row) for row in results]