# app/tests/test_fmp.py
from requests_mock import Mocker
from app.services.fmp import get_income_statement, get_financial_ratios


def test_get_income_statement_quarterly_sends_quarter_to_fmp(requests_mock: Mocker):
    """FMP espera period=quarter (singular), no 'quarterly' (ver #12)"""
    requests_mock.get(
        "https://financialmodelingprep.com/api/v3/income-statement/AAPL",
        json=[{"symbol": "AAPL", "date": "2023-09-30", "revenue": 1.0, "netIncome": 1.0, "peRatio": 1.0}]
    )

    get_income_statement("AAPL", "quarterly")

    assert requests_mock.last_request.qs["period"] == ["quarter"]


def test_get_financial_ratios_quarterly_sends_quarter_to_fmp(requests_mock: Mocker):
    requests_mock.get(
        "https://financialmodelingprep.com/api/v3/ratios/AAPL",
        json=[{"symbol": "AAPL", "date": "2023-09-30", "currentRatio": 1.0}]
    )

    get_financial_ratios("AAPL", "quarterly")

    assert requests_mock.last_request.qs["period"] == ["quarter"]


def test_get_income_statement_annual_sends_annual_to_fmp(requests_mock: Mocker):
    requests_mock.get(
        "https://financialmodelingprep.com/api/v3/income-statement/AAPL",
        json=[]
    )

    get_income_statement("AAPL", "annual")

    assert requests_mock.last_request.qs["period"] == ["annual"]
