# app/__init__.py
__version__ = "1.0.0"
__author__ = "Alberto Montenegro <alberto@amonten.com>"

# Importaciones principales para facilitar el acceso
from .main import app  # Importa la instancia FastAPI principal

# Inicialización opcional de componentes
def initialize():
    """Función opcional para inicializar componentes al importar el paquete"""
    pass

# Ejecutar inicialización al importar el paquete
initialize()