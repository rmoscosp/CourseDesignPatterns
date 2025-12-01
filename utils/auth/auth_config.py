"""
Configuración de autenticación centralizada usando Singleton Pattern
"""

class AuthConfig:
    """
    Singleton para configuración de autenticación.
    Asegura una única fuente de verdad para la configuración.
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Token válido único para toda la aplicación
            self.VALID_TOKEN = 'abcd12345'
            # Credenciales de usuario válidas
            self.VALID_CREDENTIALS = {
                'username': 'student',
                'password': 'desingp'
            }
            self._initialized = True
    
    def is_valid_token(self, token: str) -> bool:
        """
        Valida si un token es correcto.
        
        Args:
            token: Token a validar
            
        Returns:
            bool: True si el token es válido, False en caso contrario
        """
        if not token:
            return False
        return token.strip() == self.VALID_TOKEN
    
    def validate_credentials(self, username: str, password: str) -> bool:
        """
        Valida credenciales de usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            bool: True si las credenciales son válidas
        """
        return (username == self.VALID_CREDENTIALS['username'] and 
                password == self.VALID_CREDENTIALS['password'])