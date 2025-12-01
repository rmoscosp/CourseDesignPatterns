"""
Decorador de autenticación para proteger endpoints.
Implementa el Decorator Pattern para centralizar la lógica de autenticación.
"""

from functools import wraps
from flask import request
from utils.auth.auth_config import AuthConfig

def token_required(f):
    """
    Decorador que valida el token de autorización antes de ejecutar un endpoint.
    
    Uso:
        @token_required
        def get(self):
            # código del endpoint
    
    Returns:
        función decorada que valida el token antes de ejecutarse
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_config = AuthConfig()
        token = request.headers.get('Authorization')
        
        if not token:
            return {'message': 'Unauthorized: access token not found'}, 401
        
        if not auth_config.is_valid_token(token):
            return {'message': 'Unauthorized: invalid token'}, 401
        
        return f(*args, **kwargs)
    
    return decorated_function