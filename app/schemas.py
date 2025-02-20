# app/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Union
from datetime import datetime

class PriceData(BaseModel):
    """Modelo para datos históricos de precios"""
    date: str = Field(..., example="2023-10-05")
    open: float = Field(..., example=150.25)
    high: float = Field(..., example=152.30)
    low: float = Field(..., example=149.80)
    close: float = Field(..., example=151.75)
    volume: Optional[int] = Field(None, example=1000000)

    class Config:
        json_schema_extra = {
            "description": "Datos históricos de precios de un instrumento financiero"
        }

class FinancialData(BaseModel):
    """Modelo para datos financieros fundamentales"""
    symbol: str = Field(..., example="AAPL")
    date: str = Field(..., example="2022-09-24")
    revenue: Optional[float] = Field(None, example=394_328_000_000.0)
    net_income: Optional[float] = Field(None, alias="netIncome", example=99_803_000_000.0)  # Usar alias para netIncome
    pe_ratio: Optional[float] = Field(None, alias="peRatio", example=28.5)  # Usar alias para peRatio

    model_config = ConfigDict(
        populate_by_name=True,  # Permite usar alias y nombres de campo juntos
        arbitrary_types_allowed=True
    )
    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "description": "Datos fundamentales de estados financieros"
        }

class FinancialRatios(BaseModel):
    """Modelo para ratios financieros"""
    symbol: str = Field(..., example="AAPL")
    date: str = Field(..., example="2022-09-24")
    current_ratio: Optional[float] = Field(None, example=0.85)
    debt_to_equity: Optional[float] = Field(None, example=1.45)
    roe: Optional[float] = Field(None, example=0.25)
    pe_ratio: Optional[float] = Field(None, example=28.5)

    class Config:
        json_schema_extra = {
            "description": "Ratios financieros clave"
        }

class NewsItem(BaseModel):
    """Modelo para artículos de noticias"""
    title: str = Field(..., example="Apple anuncia nuevos productos")
    source: str = Field(..., example="Reuters")
    url: str = Field(..., example="https://example.com/news")
    published_at: datetime = Field(..., example="2023-10-05T12:00:00Z")
    content: Optional[str] = Field(None, example="Apple ha anunciado hoy...")
    image_url: Optional[str] = Field(None, example="https://example.com/image.jpg")

    class Config:
        json_schema_extra = {
            "description": "Artículo de noticia financiera"
        }

class InstrumentInfo(BaseModel):
    """Modelo para información de instrumentos financieros"""
    figi: str = Field(..., example="BBG000B9XRY4")
    name: str = Field(..., example="APPLE INC")
    ticker: str = Field(..., example="AAPL")
    market: str = Field(..., example="NASDAQ")
    security_type: str = Field(..., example="Common Stock")
    currency: Optional[str] = Field(None, example="USD")  # Cambio clave aquí
    country: Optional[str] = Field(None, example="United States")

    class Config:
        json_schema_extra = {
            "description": "Información de identificación de instrumento financiero"
        }

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    error: str = Field(..., example="Recurso no encontrado")
    details: Optional[Union[str, list]] = Field(None, example="El símbolo no existe")  # Cambio aquí
    code: Optional[int] = Field(None, example=404)

    class Config:
        json_schema_extra = {
            "description": "Respuesta estandarizada para errores"
        }

class PaginatedResponse(BaseModel):
    """Modelo base para respuestas paginadas"""
    total_results: int = Field(..., example=100)
    page: int = Field(..., example=1)
    page_size: int = Field(..., example=10)
    data: List[Union[PriceData, FinancialData, NewsItem, InstrumentInfo]]

    class Config:
        json_schema_extra = {
            "description": "Respuesta paginada para listados"
        }

class SuccessResponse(BaseModel):
    """Modelo base para respuestas exitosas"""
    success: bool = Field(..., example=True)
    message: Optional[str] = Field(None, example="Operación exitosa")
    data: Optional[Union[dict, list]] = None

    class Config:
        json_schema_extra = {
            "description": "Respuesta estandarizada para operaciones exitosas"
        }