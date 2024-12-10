import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-por-defecto")  # Cambiar en prod
    JWT_ALGORITHM = 'HS256'
