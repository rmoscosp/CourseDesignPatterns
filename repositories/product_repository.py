"""
Repository Pattern para gestión de productos.
Separa la lógica de acceso a datos de la lógica de negocio.
"""

from typing import List, Optional, Dict, Any
from utils.database_connection import DatabaseConnection


class ProductRepository:
    """
    Repositorio para operaciones CRUD de productos.
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
        Obtiene todos los productos.
        
        Returns:
            Lista de productos
        """
        try:
            return self.db.get_products()
        except Exception as e:
            raise Exception(f"Error al obtener productos: {str(e)}")
    
    def get_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca un producto por ID.
        
        Args:
            product_id: ID del producto a buscar
            
        Returns:
            Producto encontrado o None
        """
        try:
            products = self.get_all()
            return next((p for p in products if p['id'] == product_id), None)
        except Exception as e:
            raise Exception(f"Error al buscar producto: {str(e)}")
    
    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Filtra productos por categoría.
        
        Args:
            category: Nombre de la categoría
            
        Returns:
            Lista de productos de la categoría
        """
        try:
            products = self.get_all()
            return [p for p in products if p.get('category', '').lower() == category.lower()]
        except Exception as e:
            raise Exception(f"Error al filtrar por categoría: {str(e)}")
    
    def add(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agrega un nuevo producto.
        
        Args:
            product: Datos del producto a agregar
            
        Returns:
            Producto agregado con ID asignado
        """
        try:
            self.db.add_product(product)
            return product
        except Exception as e:
            raise Exception(f"Error al agregar producto: {str(e)}")
    
    def get_next_id(self) -> int:
        """
        Calcula el siguiente ID disponible.
        
        Returns:
            Siguiente ID a utilizar
        """
        try:
            products = self.get_all()
            return len(products) + 1
        except Exception:
            return 1