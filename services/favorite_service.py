"""
Service Layer para lógica de negocio de favoritos.
Separa la lógica de negocio del acceso a datos y la presentación.
"""

from typing import List, Dict, Any
from repositories.favorite_repository import FavoriteRepository


class FavoriteService:
    """
    Servicio que contiene la lógica de negocio para favoritos.
    """
    
    def __init__(self):
        """Inicializa el servicio con su repositorio."""
        self.repository = FavoriteRepository()
    
    def get_all_favorites(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los favoritos.
        
        Returns:
            Lista de todos los favoritos
        """
        return self.repository.get_all()
    
    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene los favoritos de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de favoritos del usuario
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if user_id <= 0:
            raise ValueError("El ID del usuario debe ser mayor a 0")
        
        return self.repository.get_by_user(user_id)
    
    def add_favorite(self, user_id: int, product_id: int) -> Dict[str, Any]:
        """
        Agrega un producto a favoritos.
        
        Args:
            user_id: ID del usuario
            product_id: ID del producto
            
        Returns:
            Favorito creado
            
        Raises:
            ValueError: Si los datos no son válidos o el favorito ya existe
        """
        # Validaciones de negocio
        if user_id <= 0:
            raise ValueError("El ID del usuario debe ser mayor a 0")
        
        if product_id <= 0:
            raise ValueError("El ID del producto debe ser mayor a 0")
        
        # Verificar si ya existe
        if self.repository.exists(user_id, product_id):
            raise ValueError("Este producto ya está en favoritos")
        
        # Crear favorito
        new_favorite = {
            'user_id': user_id,
            'product_id': product_id
        }
        
        return self.repository.add(new_favorite)
    
    def remove_favorite(self, user_id: int, product_id: int) -> bool:
        """
        Elimina un producto de favoritos.
        
        Args:
            user_id: ID del usuario
            product_id: ID del producto
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            ValueError: Si los datos no son válidos o el favorito no existe
        """
        # Validaciones
        if user_id <= 0:
            raise ValueError("El ID del usuario debe ser mayor a 0")
        
        if product_id <= 0:
            raise ValueError("El ID del producto debe ser mayor a 0")
        
        # Verificar si existe
        if not self.repository.exists(user_id, product_id):
            raise ValueError("Este favorito no existe")
        
        return self.repository.remove(user_id, product_id)