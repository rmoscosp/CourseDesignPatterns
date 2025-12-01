"""
Endpoint de productos refactorizado.
Utiliza Service Layer, Repository Pattern y Decorator Pattern.
"""

from flask_restful import Resource, reqparse
from flask import request
from utils.auth.auth_decorator import token_required
from services.product_service import ProductService


class ProductsResource(Resource):
    """
    Resource para operaciones CRUD de productos.
    Ahora con separación de responsabilidades y código más limpio.
    """
    
    def __init__(self):
        """Inicializa el resource con su servicio."""
        self.service = ProductService()
        self.parser = reqparse.RequestParser()
    
    @token_required
    def get(self, product_id=None):
        """
        Obtiene productos.
        
        Args:
            product_id: ID del producto (opcional)
            
        Query params:
            category: Filtrar por categoría (opcional)
            
        Returns:
            - Si product_id: producto específico o 404
            - Si category: productos de esa categoría
            - Sin parámetros: todos los productos
        """
        try:
            # Filtro por categoría
            category_filter = request.args.get('category')
            if category_filter:
                products = self.service.get_products_by_category(category_filter)
                return products, 200
            
            # Producto específico por ID
            if product_id is not None:
                product = self.service.get_product_by_id(product_id)
                if product:
                    return product, 200
                else:
                    return {'message': 'Product not found'}, 404
            
            # Todos los productos
            return self.service.get_all_products(), 200
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500
    
    @token_required
    def post(self):
        """
        Crea un nuevo producto.
        
        Body:
            name: Nombre del producto (requerido)
            category: Categoría del producto (requerido)
            price: Precio del producto (requerido)
            
        Returns:
            201: Producto creado exitosamente
            400: Datos inválidos
        """
        try:
            # Configurar parser
            self.parser.add_argument('name', type=str, required=True, 
                                    help='Name of the product is required')
            self.parser.add_argument('category', type=str, required=True, 
                                    help='Category of the product is required')
            self.parser.add_argument('price', type=float, required=True, 
                                    help='Price of the product is required')
            
            args = self.parser.parse_args()
            
            # Crear producto usando el servicio
            new_product = self.service.create_product(
                name=args['name'],
                category=args['category'],
                price=args['price']
            )
            
            return {
                'message': 'Product added successfully',
                'product': new_product
            }, 201
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500