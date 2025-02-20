# app/config.py
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Debug: Mostrar todas las variables cargadas
print("Variables de entorno cargadas:", {k: v for k, v in os.environ.items() if "API" in k})

class Config:
    # API Keys (requeridas)
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    FMP_API_KEY: str = os.getenv("FMP_API_KEY", "")
    OPENFIGI_API_KEY: str = os.getenv("OPENFIGI_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Configuración general
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-insecure-key-!cambiar-en-produccion!")
    
    # Límites de tasa
    ALPHA_VANTAGE_RATE_LIMIT: int = int(os.getenv("ALPHA_VANTAGE_RATE_LIMIT", "5"))
    FMP_RATE_LIMIT: int = int(os.getenv("FMP_RATE_LIMIT", "250"))
    NEWSAPI_RATE_LIMIT: int = int(os.getenv("NEWSAPI_RATE_LIMIT", "100"))
    
    # Base de datos
    DATABASE_URI: Optional[str] = os.getenv("DATABASE_URI")
    DATABASE_USER: Optional[str] = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: Optional[str] = os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME: Optional[str] = os.getenv("DATABASE_NAME")
    
    # CORS
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Metadata
    APP_NAME: str = "Financial API"
    APP_VERSION: str = "1.0.0"

    @classmethod
    def verify_keys(cls):
        """Valida que las claves esenciales estén configuradas"""
        required_keys = {
            "ALPHA_VANTAGE_API_KEY": cls.ALPHA_VANTAGE_API_KEY,
            "FMP_API_KEY": cls.FMP_API_KEY,
            "OPENFIGI_API_KEY": cls.OPENFIGI_API_KEY,
            "NEWS_API_KEY": cls.NEWS_API_KEY
        }
        
        missing = [key for key, value in required_keys.items() if not value]
        
        if missing:
            raise ValueError(
                f"Faltan variables de entorno: {', '.join(missing)}\n"
                "1. Regístrate en los proveedores correspondientes\n"
                "2. Agrega las claves al archivo .env"
            )

# Validar configuración al importar
Config.verify_keys()