# app/utils.py
import logging
import time
from functools import lru_cache, wraps
from datetime import datetime, timedelta
from typing import Callable, Any, Optional, Dict
import redis
from app.config import Config

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CacheManager:
    """Gestor de caché para almacenamiento temporal de datos"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            decode_responses=True
        )
    
    @lru_cache(maxsize=100)
    def memory_cache(self, func: Callable, *args, **kwargs):
        """Caché en memoria usando LRU"""
        return func(*args, **kwargs)
    
    def redis_cache(self, key: str, ttl: int = 300):
        """Decorador para caché en Redis"""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cached = self.redis_client.get(key)
                if cached:
                    return cached
                result = func(*args, **kwargs)
                self.redis_client.setex(key, ttl, result)
                return result
            return wrapper
        return decorator

cache = CacheManager()

def log_api_call(func: Callable) -> Callable:
    """Decorador para registrar llamadas a APIs externas"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Iniciando llamada a {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"Llamada a {func.__name__} completada en {execution_time:.2f}s"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error en {func.__name__}: {str(e)}",
                exc_info=True
            )
            raise
    
    return wrapper

class RateLimiter:
    """Gestor de límites de tasa para APIs externas"""
    
    _limits: Dict[str, Dict[str, Any]] = {
        "alpha_vantage": {"calls": 0, "max": 5, "window": 60},
        "fmp": {"calls": 0, "max": 250, "window": 86400},
        "newsapi": {"calls": 0, "max": 100, "window": 86400}
    }
    
    @classmethod
    def check_limit(cls, service: str) -> bool:
        """Verifica si se ha excedido el límite de llamadas"""
        now = time.time()
        limit_data = cls._limits.get(service)
        
        if not limit_data:
            return True
        
        if now - limit_data.get("last_reset", 0) > limit_data["window"]:
            limit_data["calls"] = 0
            limit_data["last_reset"] = now
        
        if limit_data["calls"] >= limit_data["max"]:
            return False
        
        limit_data["calls"] += 1
        return True

def handle_api_error(error: Exception, service: str) -> Dict[str, str]:
    """Maneja errores de APIs externas de forma estandarizada"""
    error_msg = f"Error en {service}: {str(error)}"
    logger.error(error_msg, exc_info=True)
    return {"error": error_msg, "service": service}

def validate_date_format(date_str: str, fmt: str = "%Y-%m-%d") -> bool:
    """Valida el formato de una fecha"""
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False

def convert_date_format(
    date_str: str, 
    from_fmt: str = "%Y-%m-%d", 
    to_fmt: str = "%Y%m%d"
) -> str:
    """Convierte entre formatos de fecha"""
    date_obj = datetime.strptime(date_str, from_fmt)
    return date_obj.strftime(to_fmt)

def generate_date_range(
    start_date: str, 
    end_date: str, 
    date_format: str = "%Y-%m-%d"
) -> list:
    """Genera un rango de fechas"""
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    return [
        (start + timedelta(days=x)).strftime(date_format)
        for x in range((end - start).days + 1)
    ]

def validate_api_key(api_key: str, expected_key: str) -> bool:
    """Valida una API key (para uso futuro con autenticación)"""
    # Implementar lógica de validación segura según necesidades
    return api_key == expected_key

def format_currency(value: float, currency: str) -> str:
    """Formatea valores monetarios"""
    return f"{currency} {value:,.2f}"

def validate_config():
    """Valida que todas las variables de configuración estén presentes"""
    required_keys = [
        'ALPHA_VANTAGE_API_KEY',
        'FMP_API_KEY',
        'NEWS_API_KEY',
        'OPENFIGI_API_KEY'
    ]
    
    missing = [key for key in required_keys if not getattr(Config, key, None)]
    if missing:
        raise EnvironmentError(
            f"Faltan variables de entorno: {', '.join(missing)}"
        )

# Ejecutar validación de configuración al importar
validate_config()