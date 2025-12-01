"""
Service Layer para lógica de negocio de categorías.
Separa la lógica de negocio del acceso a datos y la presentación.
"""

from typing import List, Optional, Dict, Any
from repositories.category_repository import CategoryRepository


class CategoryService:
    """
    Servicio que contiene la lógica de negocio para categorías.
    """
    
    def __init__(self):
        """Inicializa el servicio con su repositorio."""
        self.repository = CategoryRepository()
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las categorías.
        
        Returns:
            Lista de todas las categorías
        """
        return self.repository.get_all()
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene una categoría por su ID.
        
        Args:
            category_id: ID de la categoría
            
        Returns:
            Categoría encontrada o None
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if category_id <= 0:
            raise ValueError("El ID de la categoría debe ser mayor a 0")
        
        return self.repository.get_by_id(category_id)
    
    def create_category(self, name: str) -> Dict[str, Any]:
        """
        Crea una nueva categoría.
        
        Args:
            name: Nombre de la categoría
            
        Returns:
            Categoría creada con ID asignado
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validaciones de negocio
        if not name or not name.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío")
        
        if len(name.strip()) > 50:
            raise ValueError("El nombre no puede exceder 50 caracteres")
        
        # Verificar si ya existe
        existing_category = self.repository.get_by_name(name.strip())
        if existing_category:
            raise ValueError("La categoría ya existe")
        
        # Crear categoría
        new_category = {
            'id': self.repository.get_next_id(),
            'name': name.strip()
        }
        
        return self.repository.add(new_category)
    
    def delete_category(self, name: str) -> bool:
        """
        Elimina una categoría por nombre.
        
        Args:
            name: Nombre de la categoría a eliminar
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            ValueError: Si los datos no son válidos o la categoría no existe
        """
        if not name or not name.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío")
        
        # Verificar si existe
        existing_category = self.repository.get_by_name(name.strip())
        if not existing_category:
            raise ValueError("Categoría no encontrada")
        
        return self.repository.remove(name.strip())