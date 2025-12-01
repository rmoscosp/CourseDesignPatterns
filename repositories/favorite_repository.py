"""
Repository Pattern para gestión de favoritos.
Separa la lógica de acceso a datos de la lógica de negocio.
"""

from typing import List, Dict, Any
from utils.database_connection import DatabaseConnection


class FavoriteRepository:
    """
    Repositorio para operaciones CRUD de favoritos.
    Encapsula toda la lógica de acceso a datos.
    """
    
    def __init__(self, db_file: str = 'favorites.json'):
        """
        Inicializa el repositorio con conexión a base de datos.
        
        Args:
            db_file: Ruta al archivo de base de datos JSON
        """
        self.db = DatabaseConnection(db_file)
        self.db.connect()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los favoritos.
        
        Returns:
            Lista de favoritos
        """
        try:
            return self.db.get_favorites()
        except Exception as e:
            raise Exception(f"Error al obtener favoritos: {str(e)}")
    
    def get_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene favoritos de un usuario específico.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de favoritos del usuario
        """
        try:
            favorites = self.get_all()
            return [f for f in favorites if f.get('user_id') == user_id]
        except Exception as e:
            raise Exception(f"Error al obtener favoritos del usuario: {str(e)}")
    
    def add(self, favorite: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agrega un nuevo favorito.
        
        Args:
            favorite: Datos del favorito (user_id, product_id)
            
        Returns:
            Favorito agregado
        """
        try:
            self.db.add_favorite(favorite)
            return favorite
        except Exception as e:
            raise Exception(f"Error al agregar favorito: {str(e)}")
    
    def remove(self, user_id: int, product_id: int) -> bool:
        """
        Elimina un favorito específico.
        
        Args:
            user_id: ID del usuario
            product_id: ID del producto
            
        Returns:
            True si se eliminó exitosamente
        """
        try:
            favorites = self.get_all()
            updated_favorites = [
                f for f in favorites 
                if not (f.get('user_id') == user_id and f.get('product_id') == product_id)
            ]
            self.db.save_favorites(updated_favorites)
            return True
        except Exception as e:
            raise Exception(f"Error al eliminar favorito: {str(e)}")
    
    def exists(self, user_id: int, product_id: int) -> bool:
        """
        Verifica si un favorito ya existe.
        
        Args:
            user_id: ID del usuario
            product_id: ID del producto
            
        Returns:
            True si el favorito existe
        """
        try:
            favorites = self.get_all()
            return any(
                f.get('user_id') == user_id and f.get('product_id') == product_id 
                for f in favorites
            )
        except Exception as e:
            raise Exception(f"Error al verificar existencia de favorito: {str(e)}")