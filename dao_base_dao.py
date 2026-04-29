"""
Módulo: dao/base_dao.py
Descripción: Clase base abstracta para todos los DAOs
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic
from db.connection import DatabaseConnection

T = TypeVar('T')


class BaseDAO(ABC, Generic[T]):
    """Clase base abstracta para Data Access Objects"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.table_name: str = ""
        self.primary_key: str = "id"
    
    @abstractmethod
    def _map_to_entity(self, row: Dict[str, Any]) -> T:
        pass
    
    @abstractmethod
    def _map_to_dict(self, entity: T) -> Dict[str, Any]:
        pass
    
    def create(self, entity: T) -> int:
        data = self._map_to_dict(entity)
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        return self.db.execute_query(query, tuple(data.values()), commit=True)
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = %s"
        results = self.db.execute_query(query, (entity_id,))
        return self._map_to_entity(results[0]) if results else None
    
    def get_all(self) -> List[T]:
        query = f"SELECT * FROM {self.table_name}"
        results = self.db.execute_query(query)
        return [self._map_to_entity(row) for row in results]
    
    def update(self, entity_id: int, data: Dict[str, Any]) -> bool:
        if not data:
            return False
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary_key} = %s"
        values = list(data.values()) + [entity_id]
        self.db.execute_query(query, tuple(values), commit=True)
        return True
    
    def delete(self, entity_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = %s"
        self.db.execute_query(query, (entity_id,), commit=True)
        return True