# app/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # Importación añadida
from typing import Optional, List, Dict, Union
import logging
from app.services import (
    alpha_vantage,
    fmp,
    news,
    openfigi
)
from app.config import Config
from pydantic import BaseModel

# Configurar aplicación FastAPI
app = FastAPI(
    title="API Financiera Integrada",
    description="API que unifica múltiples fuentes de datos financieros",
    version="1.0.0"
)

# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic para respuestas (Actualizados)
class NewsItem(BaseModel):
    title: str
    source: str
    url: str
    published_at: str
    content: Optional[str]

class FinancialData(BaseModel):
    symbol: str
    date: str
    revenue: Optional[float]
    net_income: Optional[float]
    pe_ratio: Optional[float]

class InstrumentInfo(BaseModel):
    figi: str
    name: str
    ticker: str
    market: str
    security_type: str
    currency: Optional[str] = None  # Campo opcional

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str]
    code: Optional[int]  # Nuevo campo

# Endpoints (Actualizados)
@app.get("/", tags=["Root"])
async def root():
    """Endpoint de bienvenida"""
    return {"message": "Bienvenido a la API Financiera Integrada"}

@app.get("/instruments", response_model=Union[List[InstrumentInfo], ErrorResponse], tags=["Instrumentos"])
async def search_instruments(
    query: str = Query(..., min_length=2),
    id_type: str = Query("TICKER", min_length=3),
    market: str = Query("US", min_length=2)
):
    """Buscar instrumentos financieros por identificador"""
    try:
        result = openfigi.search_instrument(query, id_type, market)
        
        # Manejar errores de la API
        if isinstance(result, dict) and "error" in result:
            return JSONResponse(
                status_code=result.get("code", 500),
                content=result
            )
            
        return result
        
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error interno del servidor",
                "details": str(e)
            }
        )

@app.get("/prices", response_model=Union[Dict, ErrorResponse], tags=["Mercado"])
async def get_prices(
    symbol: str = Query(..., min_length=1),
    interval: str = Query("daily", regex="^(daily|1min|5min|15min|30min|60min)$")
):
    """Obtener datos históricos de precios"""
    try:
        prices = alpha_vantage.get_stock_prices(symbol, interval)
        if "error" in prices:
            return JSONResponse(
                status_code=400,
                content=prices
            )
        return prices
    except Exception as e:
        logger.error(f"Error en precios: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error obteniendo precios",
                "details": str(e)
            }
        )

@app.get("/financials", response_model=Union[List[FinancialData], ErrorResponse], tags=["Fundamentales"])
async def get_financials(
    symbol: str = Query(..., min_length=1),
    period: str = Query("annual", regex="^(annual|quarterly)$")
):
    try:
        financials = fmp.get_income_statement(symbol, period)
        if isinstance(financials, dict) and "error" in financials:
            return JSONResponse(
                status_code=400,
                content=financials
            )
        return financials
    except Exception as e:
        logger.error(f"Error en datos financieros: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Error obteniendo datos financieros"}
        )

@app.get("/news", response_model=Union[Dict[str, Union[int, List[NewsItem]]], ErrorResponse], tags=["Noticias"])
async def get_news(
    query: str = Query(..., min_length=2),
    limit: int = Query(5, ge=1, le=100),
    sort_by: str = Query("publishedAt", regex="^(relevancy|popularity|publishedAt)$")
):
    """Obtener noticias financieras relevantes"""
    try:
        news_data = news.get_financial_news(query, limit, sort_by)
        if "error" in news_data:
            return JSONResponse(
                status_code=400,
                content=news_data
            )
        return news_data
    except Exception as e:
        logger.error(f"Error en noticias: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error obteniendo noticias",
                "details": str(e)
            }
        )

# Manejo global de errores mejorado
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error no controlado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "details": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)