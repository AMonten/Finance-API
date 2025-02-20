import requests
import logging
from typing import Dict, Union
from app.config import Config

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Mapeo de funciones de Alpha Vantage
FUNCTION_MAP = {
    "daily": "TIME_SERIES_DAILY",
    "1min": "TIME_SERIES_INTRADAY",
    "5min": "TIME_SERIES_INTRADAY",
    "15min": "TIME_SERIES_INTRADAY",
    "30min": "TIME_SERIES_INTRADAY",
    "60min": "TIME_SERIES_INTRADAY"
}

def get_stock_prices(symbol: str, interval: str = "daily") -> Dict[str, Union[dict, str]]:
    """
    Obtiene datos históricos de precios de Alpha Vantage
    Args:
        symbol: Símbolo bursátil (ej: 'AAPL')
        interval: Intervalo de tiempo (daily, 1min, 5min, etc.)
    
    Returns:
        Dict con datos de precios o mensaje de error
    """
    try:
        # Validar parámetros iniciales
        if not Config.ALPHA_VANTAGE_API_KEY:
            logger.error("API key de Alpha Vantage no configurada")
            return {"error": "Configuración de API incompleta"}
        
        if interval not in FUNCTION_MAP:
            raise ValueError(f"Intervalo no válido: {interval}")

        logger.info(f"Solicitando precios para {symbol} ({interval})")
        
        # Construir parámetros
        params = {
            "function": FUNCTION_MAP[interval],
            "symbol": symbol,
            "apikey": Config.ALPHA_VANTAGE_API_KEY,  # ¡Clave correcta aquí!
            "outputsize": "compact"
        }
        
        if interval != "daily":
            params["interval"] = interval
        
        # Verificar parámetros en logs (solo para debug)
        logger.debug(f"Parámetros de solicitud: {params}")
        
        # Hacer la solicitud
        response = requests.get(
            "https://www.alphavantage.co/query",
            params=params,
            timeout=15
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Manejar errores de Alpha Vantage
        if "Error Message" in data:
            logger.error(f"Error en API: {data['Error Message']}")
            return {"error": data["Error Message"]}
            
        if "Note" in data:
            logger.error("Límite de API alcanzado")
            return {"error": data["Note"]}
        
        return data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {str(e)}")
        return {"error": f"Error de conexión: {str(e)}"}
    
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        return {"error": f"Error interno: {str(e)}"}