# app/tests/test_news.py
from requests_mock import Mocker
from app.services.news import get_financial_news


def test_get_financial_news_empty_results_is_not_an_error(requests_mock: Mocker):
    """Una búsqueda válida sin resultados no debe tratarse como error (ver #17)"""
    requests_mock.get(
        "https://newsapi.org/v2/everything",
        json={"status": "ok", "totalResults": 0, "articles": []}
    )

    result = get_financial_news("una-empresa-muy-poco-conocida")

    assert "error" not in result
    assert result["total_results"] == 0
    assert result["articles"] == []


def test_get_financial_news_success(requests_mock: Mocker):
    requests_mock.get(
        "https://newsapi.org/v2/everything",
        json={
            "status": "ok",
            "totalResults": 1,
            "articles": [
                {
                    "title": "Apple anuncia nuevos productos",
                    "source": {"name": "Reuters"},
                    "url": "https://example.com/news",
                    "publishedAt": "2023-10-05T12:00:00Z",
                    "content": "..."
                }
            ]
        }
    )

    result = get_financial_news("Apple")

    assert "error" not in result
    assert result["total_results"] == 1
    assert len(result["articles"]) == 1
