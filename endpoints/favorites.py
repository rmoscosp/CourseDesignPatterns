"""
Endpoint de favoritos refactorizado.
Utiliza Service Layer, Repository Pattern y Decorator Pattern.
"""

from flask_restful import Resource, reqparse
from decorators.auth_decorator import token_required
from services.favorite_service import FavoriteService


class FavoritesResource(Resource):
    """
    Resource para operaciones CRUD de favoritos.
    Ahora con separación de responsabilidades y código más limpio.
    """
    
    def __init__(self):
        """Inicializa el resource con su servicio."""
        self.service = FavoriteService()
        self.parser = reqparse.RequestParser()
    
    @token_required
    def get(self):
        """
        Obtiene todos los favoritos.
        
        Query params:
            user_id: Filtrar por usuario (opcional)
            
        Returns:
            200: Lista de favoritos
        """
        try:
            # Filtro opcional por usuario
            user_id = request.args.get('user_id', type=int)
            
            if user_id:
                favorites = self.service.get_user_favorites(user_id)
            else:
                favorites = self.service.get_all_favorites()
            
            return favorites, 200
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500
    
    @token_required
    def post(self):
        """
        Agrega un producto a favoritos.
        
        Body:
            user_id: ID del usuario (requerido)
            product_id: ID del producto (requerido)
            
        Returns:
            201: Favorito agregado exitosamente
            400: Datos inválidos o favorito ya existe
        """
        try:
            # Configurar parser
            self.parser.add_argument('user_id', type=int, required=True, 
                                    help='User ID is required')
            self.parser.add_argument('product_id', type=int, required=True, 
                                    help='Product ID is required')
            
            args = self.parser.parse_args()
            
            # Agregar favorito usando el servicio
            new_favorite = self.service.add_favorite(
                user_id=args['user_id'],
                product_id=args['product_id']
            )
            
            return {
                'message': 'Product added to favorites',
                'favorite': new_favorite
            }, 201
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500
    
    @token_required
    def delete(self):
        """
        Elimina un producto de favoritos.
        
        Body:
            user_id: ID del usuario (requerido)
            product_id: ID del producto (requerido)
            
        Returns:
            200: Favorito eliminado exitosamente
            400: Datos inválidos
            404: Favorito no encontrado
        """
        try:
            # Configurar parser
            self.parser.add_argument('user_id', type=int, required=True, 
                                    help='User ID is required')
            self.parser.add_argument('product_id', type=int, required=True, 
                                    help='Product ID is required')
            
            args = self.parser.parse_args()
            
            # Eliminar favorito usando el servicio
            self.service.remove_favorite(
                user_id=args['user_id'],
                product_id=args['product_id']
            )
            
            return {'message': 'Product removed from favorites'}, 200
            
        except ValueError as e:
            # Si el favorito no existe, retornar 404
            if "no existe" in str(e).lower() or "not exist" in str(e).lower():
                return {'message': str(e)}, 404
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500