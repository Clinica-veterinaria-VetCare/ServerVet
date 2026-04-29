"""
Módulo: db/connection.py
Descripción: Gestión de conexión a MySQL con patrón Singleton
SPRINT 1 - Configuración de persistencia
Autor: Equipo VetCare
Versión: 1.0.0
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from typing import Optional, List, Tuple, Any, Dict

load_dotenv()


class DatabaseConfig:
    """Configuración de la base de datos"""
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Obtiene la configuración de conexión"""
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'vetcare_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'port': int(os.getenv('DB_PORT', 3306))
        }


class DatabaseConnection:
    """
    Singleton para manejar la conexión a la base de datos
    Implementa el patrón Singleton para una única instancia de conexión
    """
    
    _instance: Optional['DatabaseConnection'] = None
    
    def __new__(cls) -> 'DatabaseConnection':
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Inicializa la configuración de conexión"""
        self.config = DatabaseConfig.get_config()
        self.connection: Optional[mysql.connector.MySQLConnection] = None
    
    def connect(self) -> Optional[mysql.connector.MySQLConnection]:
        """Establece la conexión a la base de datos"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            return None
    
    def disconnect(self) -> None:
        """Cierra la conexión de manera segura"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
    
    def get_cursor(self, dictionary: bool = True) -> Optional[mysql.connector.cursor.MySQLCursorDict]:
        """Obtiene un cursor para ejecutar consultas"""
        connection = self.connect()
        if connection:
            return connection.cursor(dictionary=dictionary)
        return None
    
    def execute_query(self, query: str, params: Optional[Tuple] = None, commit: bool = False) -> Any:
        """
        Ejecuta una consulta SQL
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta parametrizada
            commit: Si es True, hace commit de la transacción
        
        Returns:
            Resultados de la consulta o ID de último insert
        """
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params or ())
            if commit:
                self.connection.commit()
                return cursor.lastrowid
            return cursor.fetchall()
        except Error as e:
            if commit and self.connection:
                self.connection.rollback()
            print(f"❌ Error ejecutando query: {e}")
            raise e
        finally:
            cursor.close()
    
    def execute_transaction(self, queries: List[Tuple[str, Tuple]]) -> List[int]:
        """
        Ejecuta múltiples consultas en una transacción ACID
        
        Args:
            queries: Lista de tuplas (query, params)
        
        Returns:
            Lista de IDs generados
        """
        cursor = self.get_cursor()
        try:
            self.connection.start_transaction()
            results = []
            for query, params in queries:
                cursor.execute(query, params)
                results.append(cursor.lastrowid)
            self.connection.commit()
            return results
        except Error as e:
            self.connection.rollback()
            print(f"❌ Error en transacción: {e}")
            raise e
        finally:
            cursor.close()
    
    def test_connection(self) -> bool:
        """Prueba la conexión a la base de datos"""
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except:
            return False
    
    def __enter__(self):
        """Soporte para context manager"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra conexión al salir del context manager"""
        self.disconnect()