# app/tests/test_prices.py
import pytest
from unittest.mock import patch
from requests_mock import Mocker
from app.services.alpha_vantage import get_stock_prices
from app.config import Config
from app.utils import RateLimiter

# Datos de prueba mock
MOCK_SUCCESS_RESPONSE = {
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "AAPL",
        "3. Last Refreshed": "2023-10-05"
    },
    "Time Series (Daily)": {
        "2023-10-05": {
            "1. open": "172.8100",
            "2. high": "174.2600",
            "3. low": "170.8000",
            "4. close": "173.5000",
            "5. volume": "10058372"
        }
    }
}

MOCK_ERROR_RESPONSE = {
    "Error Message": "Invalid API call. Please retry or visit the documentation."
}

def test_get_stock_prices_success(requests_mock: Mocker):
    """Prueba exitosa de obtención de precios"""
    requests_mock.get(
        "https://www.alphavantage.co/query",
        json=MOCK_SUCCESS_RESPONSE
    )
    
    result = get_stock_prices("AAPL")
    
    assert "Meta Data" in result
    assert "Time Series (Daily)" in result
    assert result["Meta Data"]["2. Symbol"] == "AAPL"

def test_get_stock_prices_api_error(requests_mock: Mocker):
    """Prueba de error en la API"""
    requests_mock.get(
        "https://www.alphavantage.co/query",
        status_code=500
    )
    
    result = get_stock_prices("AAPL")
    
    assert "error" in result
    assert "Error de conexión" in result["error"]

def test_get_stock_prices_invalid_response(requests_mock: Mocker):
    """Prueba de respuesta inválida de la API"""
    requests_mock.get(
        "https://www.alphavantage.co/query",
        json=MOCK_ERROR_RESPONSE
    )
    
    result = get_stock_prices("AAPL")
    
    assert "error" in result
    assert "Error en Alpha Vantage" in result["error"]

def test_get_stock_prices_invalid_interval():
    """Prueba de intervalo inválido"""
    result = get_stock_prices("AAPL", "invalid_interval")
    
    assert "error" in result
    assert "Intervalo no válido" in result["error"]

def test_get_stock_prices_rate_limiting(requests_mock: Mocker):
    """Prueba de límite de tasa"""
    # Resetear el contador de límites
    RateLimiter._limits["alpha_vantage"]["calls"] = 0
    
    # Mock de llamadas exitosas
    requests_mock.get(
        "https://www.alphavantage.co/query",
        json=MOCK_SUCCESS_RESPONSE
    )
    
    # Llamar hasta el límite
    for _ in range(RateLimiter._limits["alpha_vantage"]["max"]):
        get_stock_prices("AAPL")
    
    # La siguiente llamada debería fallar
    result = get_stock_prices("AAPL")
    
    assert "error" in result
    assert "Límite de llamadas excedido" in result["error"]

def test_get_stock_prices_empty_symbol():
    """Prueba de símbolo vacío"""
    result = get_stock_prices("")
    
    assert "error" in result
    assert "El símbolo no puede estar vacío" in result["error"]

@patch.dict("app.config.Config.__dict__", {"ALPHA_VANTAGE_API_KEY": None})
def test_missing_api_key():
    """Prueba de falta de API key"""
    result = get_stock_prices("AAPL")
    
    assert "error" in result
    assert "API key no configurada" in result["error"]

def test_different_intervals(requests_mock: Mocker):
    """Prueba de diferentes intervalos temporales"""
    intervals = ["1min", "5min", "15min", "30min", "60min", "daily"]
    
    for interval in intervals:
        requests_mock.get(
            "https://www.alphavantage.co/query",
            json=MOCK_SUCCESS_RESPONSE
        )
        
        result = get_stock_prices("AAPL", interval)
        assert "Meta Data" in result

def test_response_data_types(requests_mock: Mocker):
    """Prueba de tipos de datos en la respuesta"""
    requests_mock.get(
        "https://www.alphavantage.co/query",
        json=MOCK_SUCCESS_RESPONSE
    )
    
    result = get_stock_prices("AAPL")
    
    assert isinstance(result, dict)
    assert isinstance(result["Meta Data"], dict)
    assert isinstance(result["Time Series (Daily)"], dict)
    assert isinstance(result["Time Series (Daily)"]["2023-10-05"], dict)