# app/services/news.py
import requests
import logging
from typing import Dict, List, Union
from datetime import datetime, timedelta
from app.config import Config

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Parámetros válidos para ordenación
VALID_SORT_VALUES = ["relevancy", "popularity", "publishedAt"]

def get_financial_news(
    query: str,
    limit: int = 5,
    sort_by: str = "publishedAt"
) -> Dict[str, Union[List[Dict], str]]:
    """
    Obtiene noticias financieras de NewsAPI
    Args:
        query: Término de búsqueda (ej: 'Apple')
        limit: Número máximo de noticias (1-100)
        sort_by: Criterio de ordenación (publishedAt, popularity, relevancy)
    
    Returns:
        Dict con listado de noticias o mensaje de error
    """
    try:
        logger.info(f"Buscando noticias: {query}")
        
        # Validar parámetros
        if sort_by not in VALID_SORT_VALUES:
            raise ValueError(f"sort_by debe ser uno de: {VALID_SORT_VALUES}")
        
        if not 1 <= limit <= 100:
            raise ValueError("El límite debe estar entre 1 y 100")
        
        # Construir parámetros de la solicitud
        params = {
            "q": query,
            "apiKey": Config.NEWS_API_KEY,
            "pageSize": limit,
            "sortBy": sort_by,
            "language": "en",
            "from": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")  # Últimos 7 días
        }
        
        # Hacer la solicitud a la API
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params=params,
            timeout=10  # Timeout de 10 segundos
        )
        
        # Log the raw response for debugging
        logger.debug(f"Raw API response: {response.json()}")
        
        response.raise_for_status()
        logger.debug("Respuesta recibida de NewsAPI")
        
        data = response.json()
        
        # Manejar errores de la API
        if data.get("status") != "ok":
            error_msg = data.get("message", "Error desconocido en NewsAPI")
            logger.error(f"Error en NewsAPI: {error_msg}")
            return {"error": error_msg}
        
        # Verificar si hay artículos
        articles = data.get("articles", [])
        if not articles:
            logger.warning(f"No se encontraron noticias para la consulta: {query}")
            return {"error": "No se encontraron noticias para la consulta proporcionada"}
        
        # Formatear resultados
        processed_articles = []
        for article in articles:
            processed_articles.append({
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "content": article.get("content")
            })
        
        return {
            "total_results": data.get("totalResults", 0),
            "articles": processed_articles
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {str(e)}")
        return {"error": f"Error de conexión: {str(e)}"}
    
    except ValueError as e:
        logger.error(f"Error de parámetros: {str(e)}")
        return {"error": str(e)}
    
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        return {"error": f"Error interno del servidor: {str(e)}"}