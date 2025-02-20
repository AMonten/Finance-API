import requests
import logging
from typing import Dict, List, Union
from app.config import Config

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_financial_ratios(symbol: str) -> Union[List[Dict[str, Union[dict, str]]], Dict[str, str]]:
    """
    Obtiene ratios financieros de Financial Modeling Prep
    Args:
        symbol: Símbolo bursátil (ej: 'AAPL')
    
    Returns:
        Lista de ratios o mensaje de error
    """
    try:
        logger.info(f"Solicitando ratios financieros para {symbol}")
        
        # Construir parámetros de la solicitud
        params = {"apikey": Config.FMP_API_KEY}
        
        # Hacer la solicitud a la API
        response = requests.get(
            f"https://financialmodelingprep.com/api/v3/ratios/{symbol}",
            params=params,
            timeout=10
        )
        
        response.raise_for_status()
        
        logger.debug("Respuesta recibida de Financial Modeling Prep")
        data = response.json()
        
        # Manejar errores de la API
        if isinstance(data, dict) and "Error Message" in data:
            logger.error(f"Error en FMP: {data['Error Message']}")
            return {"error": data["Error Message"]}
        
        return data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {str(e)}")
        return {"error": f"Error de conexión: {str(e)}"}
    
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        return {"error": f"Error interno del servidor: {str(e)}"}

def get_income_statement(symbol: str, period: str = "annual") -> Union[List[Dict[str, Union[dict, str]]], Dict[str, str]]:
    """
    Obtiene el estado de resultados de una empresa
    Args:
        symbol: Símbolo bursátil (ej: 'AAPL')
        period: 'annual' o 'quarterly'
    
    Returns:
        Lista de estados de resultados o mensaje de error
    """
    try:
        logger.info(f"Solicitando estado de resultados para {symbol} ({period})")
        
        # Validar parámetros
        if period not in ["annual", "quarterly"]:
            raise ValueError("Periodo debe ser 'annual' o 'quarterly'")
        
        response = requests.get(
            f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}",
            params={"apikey": Config.FMP_API_KEY, "period": period},
            timeout=10
        )
        
        response.raise_for_status()
        
        raw_data = response.json()
        
        # Transformar datos para que coincidan con el modelo
        processed_data = []
        for item in raw_data:
            processed_item = {
                "symbol": item.get("symbol"),
                "date": item.get("date"),
                "revenue": item.get("revenue"),
                "net_income": item.get("netIncome"),  # Mapear netIncome a net_income
                "pe_ratio": item.get("peRatio")  # Mapear peRatio a pe_ratio
            }
            processed_data.append(processed_item)
        
        return processed_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {str(e)}")
        return {"error": f"Error de conexión: {str(e)}"}
    
    except ValueError as e:
        logger.error(f"Error de parámetros: {str(e)}")
        return {"error": str(e)}
    
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        return {"error": f"Error interno del servidor: {str(e)}"}