"""
Repository Pattern para gestión de categorías.
Separa la lógica de acceso a datos de la lógica de negocio.
"""

from typing import List, Optional, Dict, Any
from utils.database_connection import DatabaseConnection


class CategoryRepository:
    """
    Repositorio para operaciones CRUD de categorías.
    Encapsula toda la lógica de acceso a datos.
    """
    
    def __init__(self, db_file: str = 'db.json'):
        """
        Inicializa el repositorio con conexión a base de datos.
        
        Args:
            db_file: Ruta al archivo de base de datos JSON
        """
        self.db = DatabaseConnection(db_file)
        self.db.connect()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las categorías.
        
        Returns:
            Lista de categorías
        """
        try:
            return self.db.get_categories()
        except Exception as e:
            raise Exception(f"Error al obtener categorías: {str(e)}")
    
    def get_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca una categoría por ID.
        
        Args:
            category_id: ID de la categoría a buscar
            
        Returns:
            Categoría encontrada o None
        """
        try:
            categories = self.get_all()
            return next((c for c in categories if c['id'] == category_id), None)
        except Exception as e:
            raise Exception(f"Error al buscar categoría: {str(e)}")
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Busca una categoría por nombre.
        
        Args:
            name: Nombre de la categoría
            
        Returns:
            Categoría encontrada o None
        """
        try:
            categories = self.get_all()
            return next((c for c in categories if c.get('name', '').lower() == name.lower()), None)
        except Exception as e:
            raise Exception(f"Error al buscar categoría por nombre: {str(e)}")
    
    def add(self, category: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agrega una nueva categoría.
        
        Args:
            category: Datos de la categoría a agregar
            
        Returns:
            Categoría agregada
        """
        try:
            self.db.add_category(category)
            return category
        except Exception as e:
            raise Exception(f"Error al agregar categoría: {str(e)}")
    
    def remove(self, name: str) -> bool:
        """
        Elimina una categoría por nombre.
        
        Args:
            name: Nombre de la categoría a eliminar
            
        Returns:
            True si se eliminó exitosamente
        """
        try:
            self.db.remove_category(name)
            return True
        except Exception as e:
            raise Exception(f"Error al eliminar categoría: {str(e)}")
    
    def get_next_id(self) -> int:
        """
        Calcula el siguiente ID disponible.
        
        Returns:
            Siguiente ID a utilizar
        """
        try:
            categories = self.get_all()
            return len(categories) + 1
        except Exception:
            return 1