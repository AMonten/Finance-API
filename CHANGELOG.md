# Changelog

Historial de cambios reales de Finance-API. El detalle de cada issue individual
vive en GitHub (issues cerradas); acá va el resumen fechado de qué se hizo y por qué.

## 2026-09-12 — Cierre masivo de las 15 issues abiertas (seguridad, tests, mantenimiento)

Via 7 PRs independientes (#22 a #28), todos mergeados a `main`:

- **Seguridad**: rate limiting real por API externa (Alpha Vantage, FMP, NewsAPI) —
  antes existía la clase `RateLimiter` en `utils.py` pero nunca se invocaba desde
  ningún lado; cualquiera podía agotar las cuotas gratuitas sin control. Ahora vive
  en la capa de servicios (no en `main.py`, para no contar el límite dos veces) y
  devuelve `429` al excederse (#4, PR #22). CORS ya no combina
  `allow_origins=["*"]` con `allow_credentials=True` (inválido según la spec) y usa
  `Config.CORS_ORIGINS`, que existía pero se ignoraba (#5, PR #22).
- **Tests rotos**: arreglados los 4 tests de `test_prices.py` que fallaban —
  mensajes de error de Alpha Vantage sin el prefijo esperado, rate limiting real
  faltante dentro de `get_stock_prices()`, símbolo vacío sin validar (disparaba una
  llamada HTTP real en cada corrida de tests), y un mock de `Config.__dict__`
  (mappingproxy inmutable) que nunca pudo funcionar (#6, #7, #8, #9, PR #22).
- **Modelos duplicados**: `main.py` ya no define sus propias clases Pydantic
  (`NewsItem`, `FinancialData`, `InstrumentInfo`, `ErrorResponse`); usa las de
  `schemas.py`, que ya eran más completas y se habían desalineado con el tiempo
  (#13, #14, PR #23).
- **`utils.py`**: `redis_cache()` arreglado — la key de caché ahora se deriva de
  los argumentos de cada llamada (antes era estática) y se serializa con
  `json.dumps`/`json.loads` (antes fallaba con dicts/listas reales). Eliminados
  `memory_cache()` (código muerto, nunca se llamaba) y `validate_config()`
  (duplicaba exactamente `Config.verify_keys()`) (#11, #15, #16, PR #24).
- **`/news`**: una búsqueda válida sin resultados devuelve `200` con
  `{"total_results": 0, "articles": []}` en vez de `400` (#17, PR #25).
- **FMP**: se enviaba `period=quarterly` a la API externa, que en realidad espera
  `quarter` (confirmado contra la documentación de FMP) — toda solicitud
  trimestral devolvía silenciosamente datos anuales o un error no manejado. Se
  mantiene `quarterly` como contrato público de esta API y se traduce a `quarter`
  al armar la solicitud real (#12, PR #26).
- **Pydantic**: reemplazados los ~38 `Field(example=...)` deprecados en
  `schemas.py` por `json_schema_extra={"example": ...}` (#18, PR #27).
- **`requirements.txt`**: se fijaron cotas superiores de versión (antes solo
  mínimos, lo que ya había causado el incidente de PR #2 al resolver Pydantic v1
  con código escrito para v2) y se subió el mínimo de `pydantic` a `2.0.0` para
  reflejar lo que el código ya requiere. De paso se corrigió el encoding del
  archivo, que estaba en UTF-16LE con CRLF en vez de UTF-8/LF (#19, PR #28).
- README actualizado para reflejar todo lo anterior: badges desactualizados,
  endpoints sin documentar (`/health`, `/instruments`, `/financials/ratios`),
  `/financials` mal etiquetado como "ratios" cuando devuelve el estado de
  resultados, y el bullet de Redis que decía "cacheo" cuando solo se usa para
  `/health`.

## 2026-08-29 — Fugas de datos y limpieza post-v1

- Eliminado un `print()` de arranque en `app/config.py` que volcaba a stdout las
  API keys reales (Alpha Vantage, FMP, OpenFIGI, NewsAPI) en cada boot (#3).
- Eliminado `SECRET_KEY` con default inseguro hardcodeado; nada en el código lo
  leía (#21).
- Eliminado `app/cache/`, un paquete muerto que importaba un módulo `redis_cache`
  inexistente; el `CacheManager` real vive en `app/utils.py` (#10).
- Corregido el README: documentaba `pytest tests/`, los tests viven en
  `app/tests/` (#20).
- Agregados badges (Python, FastAPI, Redis, Pytest, License) al README.

## 2026-08-20 — Ratios financieros, health check y compatibilidad Pydantic v2

- PR #1: agregados los endpoints `/financials/ratios` y `/health`; soporte de
  `period` y mapeo de campos en `get_financial_ratios()`.
- PR #2: migración de `schemas.py` a sintaxis Pydantic v2 (`model_config` en vez
  de la `Config` interna de v1) y `Query(pattern=...)` en vez del parámetro
  `regex` deprecado — arregla el arranque roto cuando se instalaba el proyecto
  con una versión real de Pydantic v2.

## 2025-02-20 — Primera versión

- Primera versión de la API financiera, integrando Alpha Vantage, FMP, OpenFIGI y
  NewsAPI. Licencia MIT.
