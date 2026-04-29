"""
Módulo: dao/dueno_dao.py
Descripción: Data Access Object para la entidad Dueño
"""

from typing import Optional, List, Dict, Any
from dao.base_dao import BaseDAO
from datetime import datetime


class Dueno:
    """Entidad Dueño"""
    
    def __init__(self, nombre: str, telefono: str, email: Optional[str] = None, 
                 direccion: Optional[str] = None, id: Optional[int] = None,
                 fecha_registro: Optional[datetime] = None, activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_registro = fecha_registro or datetime.now()
        self.activo = activo
    
    def __str__(self) -> str:
        return f"{self.nombre} - Tel: {self.telefono}"


class DuenoDAO(BaseDAO[Dueno]):
    
    def __init__(self):
        super().__init__()
        self.table_name = "duenos"
    
    def _map_to_entity(self, row: Dict[str, Any]) -> Dueno:
        return Dueno(
            id=row['id'],
            nombre=row['nombre'],
            telefono=row['telefono'],
            email=row.get('email'),
            direccion=row.get('direccion'),
            fecha_registro=row['fecha_registro'],
            activo=row['activo']
        )
    
    def _map_to_dict(self, entity: Dueno) -> Dict[str, Any]:
        return {
            'nombre': entity.nombre,
            'telefono': entity.telefono,
            'email': entity.email,
            'direccion': entity.direccion,
            'activo': entity.activo
        }
    
    def find_by_email(self, email: str) -> Optional[Dueno]:
        query = "SELECT * FROM duenos WHERE email = %s"
        results = self.db.execute_query(query, (email,))
        return self._map_to_entity(results[0]) if results else None