"""
Service Layer para lógica de negocio de productos.
Separa la lógica de negocio del acceso a datos y la presentación.
"""

from typing import List, Optional, Dict, Any
from repositories.product_repository import ProductRepository


class ProductService:
    """
    Servicio que contiene la lógica de negocio para productos.
    """
    
    def __init__(self):
        """Inicializa el servicio con su repositorio."""
        self.repository = ProductRepository()
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los productos.
        
        Returns:
            Lista de todos los productos
        """
        return self.repository.get_all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Producto encontrado o None
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if product_id <= 0:
            raise ValueError("El ID del producto debe ser mayor a 0")
        
        return self.repository.get_by_id(product_id)
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Filtra productos por categoría.
        
        Args:
            category: Nombre de la categoría
            
        Returns:
            Lista de productos de la categoría
            
        Raises:
            ValueError: Si la categoría está vacía
        """
        if not category or not category.strip():
            raise ValueError("La categoría no puede estar vacía")
        
        return self.repository.get_by_category(category.strip())
    
    def create_product(self, name: str, category: str, price: float) -> Dict[str, Any]:
        """
        Crea un nuevo producto.
        
        Args:
            name: Nombre del producto
            category: Categoría del producto
            price: Precio del producto
            
        Returns:
            Producto creado con ID asignado
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validaciones de negocio
        if not name or not name.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        
        if not category or not category.strip():
            raise ValueError("La categoría no puede estar vacía")
        
        if price < 0:
            raise ValueError("El precio no puede ser negativo")
        
        if len(name.strip()) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")
        
        # Crear producto
        new_product = {
            'id': self.repository.get_next_id(),
            'name': name.strip(),
            'category': category.strip(),
            'price': round(price, 2)  # Redondear a 2 decimales
        }
        
        return self.repository.add(new_product)