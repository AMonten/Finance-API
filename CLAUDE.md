# Finance-API — contexto para Claude Code

API FastAPI que unifica Alpha Vantage, Financial Modeling Prep (FMP), OpenFIGI y
NewsAPI. Antes de tocar nada, **leer `README.md`** (instalación, endpoints,
variables de entorno) y **`CHANGELOG.md`** (historial fechado de qué se hizo y
por qué) — no duplicar detalle que ya vive en esos dos.

## Estructura

- `app/main.py` — endpoints FastAPI, sin lógica de negocio propia.
- `app/services/{alpha_vantage,fmp,news,openfigi}.py` — un módulo por proveedor
  externo; cada uno valida sus propios parámetros y maneja sus propios errores.
- `app/schemas.py` — única fuente de verdad para los modelos Pydantic de
  respuesta (no duplicar clases en `main.py`, ya paso una vez, ver #13/#14 en el
  CHANGELOG).
- `app/config.py` — `Config.verify_keys()` es la única validación de variables de
  entorno requeridas (no reintroducir una segunda en `utils.py`, ver #16).
- `app/utils.py` — `RateLimiter`, `CacheManager` (Redis), decoradores varios.
- `app/tests/` — pytest + `requests_mock`, un archivo por servicio/módulo.

## Correr tests

Necesita un `.env` en la raíz con las 4 API keys (`ALPHA_VANTAGE_API_KEY`,
`FMP_API_KEY`, `OPENFIGI_API_KEY`, `NEWS_API_KEY`) porque `Config.verify_keys()`
se ejecuta al importar `app.config` — para tests alcanza con valores dummy, ya
que las llamadas HTTP van mockeadas con `requests_mock`.

```sh
pip install -r requirements.txt
pytest app/tests/
```

## Decisiones de diseño a respetar

- **Rate limiting vive en la capa de servicios** (`RateLimiter.check_limit()`
  dentro de cada función de `app/services/*.py`), no en `main.py`. Si se agrega
  también en `main.py`, una request real cuenta el límite dos veces (pasó una
  vez, ver PR #22 en el CHANGELOG).
- **`period` público de esta API es `"annual"`/`"quarterly"`**, pero FMP espera
  `"quarter"` (singular) — la traducción vive en `FMP_PERIOD_MAP` en
  `app/services/fmp.py`. No pasar `period` tal cual a la URL de FMP.
- `schemas.FinancialData` tiene alias camelCase (`netIncome`/`peRatio`) para
  aceptar el JSON crudo de FMP como input; el endpoint `/financials` usa
  `response_model_by_alias=False` para que la respuesta siga siendo snake_case.
  No sacarlo sin querer al tocar ese modelo.
- `pydantic` requiere `>=2.0` (código usa `ConfigDict`/`model_config`, sintaxis
  v1-only rompe el arranque). `requirements.txt` ya tiene cotas superiores de
  version — no aflojarlas sin verificar que la app sigue arrancando.

## Convención de trabajo (issues/PRs)

Un PR por grupo de issues relacionadas, siempre en branch propia contra `main`
(no apiladas entre sí salvo que compartan diseño real). Cerrar la issue en
GitHub requiere un comentario/cierre manual — los commits en español
("Cierra #N") no disparan el auto-close de GitHub (solo lo hacen keywords en
inglés: `closes`, `fixes`, `resolves`).
