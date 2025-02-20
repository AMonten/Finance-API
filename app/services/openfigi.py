# app/services/openfigi.py
import requests
import logging
from typing import Dict, List, Union
from app.config import Config

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Tipos de identificadores soportados por OpenFIGI
VALID_ID_TYPES = [
    "ID_ISIN", "ID_BB_GLOBAL", "ID_SEDOL", "ID_COMMON", "ID_WERTPAPIER",
    "ID_CUSIP", "ID_CINS", "TICKER", "ID_MIC", "ID_EXCH_SYMBOL"
]

def search_instrument(
    identifier: str,
    id_type: str = "TICKER",
    market: str = "US"
) -> Union[List[Dict], Dict[str, str]]:
    """
    Busca un instrumento financiero usando OpenFIGI
    Args:
        identifier: Valor del identificador (ej: 'AAPL')
        id_type: Tipo de identificador (default: 'TICKER')
        market: Mercado objetivo (ej: 'US', 'EU')
    
    Returns:
        Lista de resultados de mapeo o mensaje de error
    """
    try:
        logger.info(f"Buscando instrumento: {identifier} ({id_type})")
        
        # Validar parámetros
        if id_type not in VALID_ID_TYPES:
            raise ValueError(f"Tipo de ID no válido. Usar: {', '.join(VALID_ID_TYPES)}")
        
        if not identifier.strip():
            raise ValueError("El identificador no puede estar vacío")
        
        # Construir payload para OpenFIGI
        headers = {
            "Content-Type": "application/json",
            "X-OPENFIGI-APIKEY": Config.OPENFIGI_API_KEY
        }
        
        payload = [{
            "idType": id_type,
            "idValue": identifier,
            "exchCode": market
        }]
        
        # Hacer la solicitud POST
        response = requests.post(
            "https://api.openfigi.com/v3/mapping",
            headers=headers,
            json=payload,
            timeout=15  # Aumenté el timeout
        )
        
        response.raise_for_status()
        logger.debug(f"Respuesta recibida: {response.status_code}")
        
        data = response.json()
        
        # Procesar resultados
        results = []
        for item in data:
            if isinstance(item, dict) and "data" in item:
                for match in item.get("data", []):
                    result = {
                        "figi": match.get("figi", ""),
                        "name": match.get("name", identifier),  # Usar identifier como fallback
                        "ticker": match.get("ticker", ""),
                        "market": match.get("exchCode", market),  # Usar parámetro market como fallback
                        "security_type": match.get("securityType", ""),
                        "currency": match.get("currency", "USD")  # Default a USD
                    }
                    results.append(result)
        
        if not results:
            logger.warning("No se encontraron resultados")
            return {"error": "No se encontraron instrumentos", "details": f"Parámetros usados: {id_type}={identifier}"}
        
        return results
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error de conexión: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "code": 503}
    
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Error de parámetros: {error_msg}")
        return {"error": error_msg, "code": 400}
    
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg, "code": 500}