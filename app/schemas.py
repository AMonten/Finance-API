# app/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Union
from datetime import datetime

class PriceData(BaseModel):
    """Modelo para datos históricos de precios"""
    model_config = ConfigDict(
        json_schema_extra={"description": "Datos históricos de precios de un instrumento financiero"}
    )

    date: str = Field(..., json_schema_extra={"example": "2023-10-05"})
    open: float = Field(..., json_schema_extra={"example": 150.25})
    high: float = Field(..., json_schema_extra={"example": 152.30})
    low: float = Field(..., json_schema_extra={"example": 149.80})
    close: float = Field(..., json_schema_extra={"example": 151.75})
    volume: Optional[int] = Field(None, json_schema_extra={"example": 1000000})

class FinancialData(BaseModel):
    """Modelo para datos financieros fundamentales"""
    model_config = ConfigDict(
        populate_by_name=True,  # Permite usar alias y nombres de campo juntos
        arbitrary_types_allowed=True,
        json_schema_extra={"description": "Datos fundamentales de estados financieros"}
    )

    symbol: str = Field(..., json_schema_extra={"example": "AAPL"})
    date: str = Field(..., json_schema_extra={"example": "2022-09-24"})
    revenue: Optional[float] = Field(None, json_schema_extra={"example": 394_328_000_000.0})
    net_income: Optional[float] = Field(None, alias="netIncome", json_schema_extra={"example": 99_803_000_000.0})  # Usar alias para netIncome
    pe_ratio: Optional[float] = Field(None, alias="peRatio", json_schema_extra={"example": 28.5})  # Usar alias para peRatio

class FinancialRatios(BaseModel):
    """Modelo para ratios financieros"""
    model_config = ConfigDict(
        json_schema_extra={"description": "Ratios financieros clave"}
    )

    symbol: str = Field(..., json_schema_extra={"example": "AAPL"})
    date: str = Field(..., json_schema_extra={"example": "2022-09-24"})
    current_ratio: Optional[float] = Field(None, json_schema_extra={"example": 0.85})
    debt_to_equity: Optional[float] = Field(None, json_schema_extra={"example": 1.45})
    roe: Optional[float] = Field(None, json_schema_extra={"example": 0.25})
    pe_ratio: Optional[float] = Field(None, json_schema_extra={"example": 28.5})

class NewsItem(BaseModel):
    """Modelo para artículos de noticias"""
    model_config = ConfigDict(
        json_schema_extra={"description": "Artículo de noticia financiera"}
    )

    title: str = Field(..., json_schema_extra={"example": "Apple anuncia nuevos productos"})
    source: str = Field(..., json_schema_extra={"example": "Reuters"})
    url: str = Field(..., json_schema_extra={"example": "https://example.com/news"})
    published_at: datetime = Field(..., json_schema_extra={"example": "2023-10-05T12:00:00Z"})
    content: Optional[str] = Field(None, json_schema_extra={"example": "Apple ha anunciado hoy..."})
    image_url: Optional[str] = Field(None, json_schema_extra={"example": "https://example.com/image.jpg"})

class InstrumentInfo(BaseModel):
    """Modelo para información de instrumentos financieros"""
    model_config = ConfigDict(
        json_schema_extra={"description": "Información de identificación de instrumento financiero"}
    )

    figi: str = Field(..., json_schema_extra={"example": "BBG000B9XRY4"})
    name: str = Field(..., json_schema_extra={"example": "APPLE INC"})
    ticker: str = Field(..., json_schema_extra={"example": "AAPL"})
    market: str = Field(..., json_schema_extra={"example": "NASDAQ"})
    security_type: str = Field(..., json_schema_extra={"example": "Common Stock"})
    currency: Optional[str] = Field(None, json_schema_extra={"example": "USD"})
    country: Optional[str] = Field(None, json_schema_extra={"example": "United States"})

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    model_config = ConfigDict(
        json_schema_extra={"description": "Respuesta estandarizada para errores"}
    )

    error: str = Field(..., json_schema_extra={"example": "Recurso no encontrado"})
    details: Optional[Union[str, list]] = Field(None, json_schema_extra={"example": "El símbolo no existe"})
    code: Optional[int] = Field(None, json_schema_extra={"example": 404})

class PaginatedResponse(BaseModel):
    """Modelo base para respuestas paginadas"""
    model_config = ConfigDict(
        json_schema_extra={"description": "Respuesta paginada para listados"}
    )

    total_results: int = Field(..., json_schema_extra={"example": 100})
    page: int = Field(..., json_schema_extra={"example": 1})
    page_size: int = Field(..., json_schema_extra={"example": 10})
    data: List[Union[PriceData, FinancialData, NewsItem, InstrumentInfo]]

class SuccessResponse(BaseModel):
    """Modelo base para respuestas exitosas"""
    model_config = ConfigDict(
        json_schema_extra={"description": "Respuesta estandarizada para operaciones exitosas"}
    )

    success: bool = Field(..., json_schema_extra={"example": True})
    message: Optional[str] = Field(None, json_schema_extra={"example": "Operación exitosa"})
    data: Optional[Union[dict, list]] = None
