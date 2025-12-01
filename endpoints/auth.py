"""
Endpoint de autenticación refactorizado.
Utiliza la configuración centralizada.
"""

from flask_restful import Resource
from flask import request
from utils.auth.auth_config import AuthConfig


class AuthenticationResource(Resource):
    """
    Resource para autenticación de usuarios.
    Utiliza configuración centralizada con Singleton.
    """
    
    def __init__(self):
        """Inicializa el resource con la configuración de autenticación."""
        self.auth_config = AuthConfig()
    
    def post(self):
        """
        Autentica un usuario y retorna un token.
        
        Body:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            200: Token de autenticación
            400: Datos inválidos
            401: Credenciales incorrectas
        """
        try:
            # Obtener credenciales del body
            data = request.get_json()
            
            if not data:
                return {'message': 'Request body is required'}, 400
            
            username = data.get('username')
            password = data.get('password')
            
            # Validar que las credenciales estén presentes
            if not username or not password:
                return {'message': 'Username and password are required'}, 400
            
            # Validar credenciales
            if self.auth_config.validate_credentials(username, password):
                return {'token': self.auth_config.VALID_TOKEN}, 200
            else:
                return {'message': 'Unauthorized: invalid credentials'}, 401
                
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500