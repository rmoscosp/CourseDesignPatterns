"""
Endpoint de categorías refactorizado.
Utiliza Service Layer, Repository Pattern y Decorator Pattern.
"""

from flask_restful import Resource, reqparse
from utils.auth.auth_decorator import token_required
from services.category_service import CategoryService


class CategoriesResource(Resource):
    """
    Resource para operaciones CRUD de categorías.
    Ahora con separación de responsabilidades y código más limpio.
    """
    
    def __init__(self):
        """Inicializa el resource con su servicio."""
        self.service = CategoryService()
        self.parser = reqparse.RequestParser()
    
    @token_required
    def get(self, category_id=None):
        """
        Obtiene categorías.
        
        Args:
            category_id: ID de la categoría (opcional)
            
        Returns:
            - Si category_id: categoría específica o 404
            - Sin parámetros: todas las categorías
        """
        try:
            # Categoría específica por ID
            if category_id is not None:
                category = self.service.get_category_by_id(category_id)
                if category:
                    return category, 200
                else:
                    return {'message': 'Category not found'}, 404
            
            # Todas las categorías
            return self.service.get_all_categories(), 200
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500
    
    @token_required
    def post(self):
        """
        Crea una nueva categoría.
        
        Body:
            name: Nombre de la categoría (requerido)
            
        Returns:
            201: Categoría creada exitosamente
            400: Datos inválidos o categoría ya existe
        """
        try:
            # Configurar parser
            self.parser.add_argument('name', type=str, required=True, 
                                    help='Name of the category is required')
            
            args = self.parser.parse_args()
            
            # Crear categoría usando el servicio
            new_category = self.service.create_category(name=args['name'])
            
            return {
                'message': 'Category added successfully',
                'category': new_category
            }, 201
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500
    
    @token_required
    def delete(self):
        """
        Elimina una categoría.
        
        Body:
            name: Nombre de la categoría a eliminar (requerido)
            
        Returns:
            200: Categoría eliminada exitosamente
            400: Datos inválidos
            404: Categoría no encontrada
        """
        try:
            # Configurar parser
            self.parser.add_argument('name', type=str, required=True, 
                                    help='Name of the category is required')
            
            args = self.parser.parse_args()
            
            # Eliminar categoría usando el servicio
            self.service.delete_category(name=args['name'])
            
            return {'message': 'Category removed successfully'}, 200
            
        except ValueError as e:
            # Si la categoría no existe, retornar 404
            if "no encontrada" in str(e).lower() or "not found" in str(e).lower():
                return {'message': str(e)}, 404
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500