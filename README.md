# 📊 API Financiera con FastAPI

![Python](https://img.shields.io/badge/python-3.x-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-E92063?logo=pydantic&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-cache-DC382D?logo=redis&logoColor=white)
![Pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 📌 Descripción
Esta API permite consultar información financiera a través de múltiples fuentes de datos como **Alpha Vantage, Financial Modeling Prep (FMP), OpenFIGI y NewsAPI**.

✅ Desarrollada con **FastAPI** para alto rendimiento.  
✅ Usa **Redis** para el health-check (`/health`); el decorador de caché en `app/utils.py` está listo pero aún no se aplica a ningún endpoint.  
✅ Implementa **pytest** para pruebas automáticas.  
✅ Arquitectura modular con separación de servicios.  
✅ Rate limiting real por API externa (Alpha Vantage, FMP, NewsAPI) — devuelve `429` al exceder la cuota.  

---

## 🚀 Instalación
### **1️⃣ Clonar el Repositorio**
```sh
git clone https://github.com/AMonten/Finance-API.git
cd Finance-API
```

### **2️⃣ Crear un Entorno Virtual**
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows
```

### **3️⃣ Instalar Dependencias**
```sh
pip install -r requirements.txt
```

---

## 🛠️ Configuración
### **1️⃣ Configurar Variables de Entorno**
Crea un archivo `.env` en la raíz con el siguiente contenido:
```ini
# API Keys
ALPHA_VANTAGE_API_KEY=tu_api_key
FMP_API_KEY=tu_api_key
OPENFIGI_API_KEY=tu_api_key
NEWS_API_KEY=tu_api_key

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Configuración General
DEBUG=True
ENVIRONMENT=development
SECRET_KEY=tu_clave

# CORS (orígenes permitidos, separados por coma; por defecto "*")
CORS_ORIGINS=http://localhost:3000,https://tudominio.com
```

---

## ▶️ Ejecución
Levanta el servidor con:
```sh
uvicorn app.main:app --reload
```
Por defecto, correrá en `http://127.0.0.1:8000`

✅ Para ver la documentación automática:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 Endpoints Disponibles
### 🔹 **🩺 Estado del Servicio**
```http
GET /health
```
Verifica la conexión con Redis. Devuelve `200` si está todo ok, `503` si Redis no responde.

### 🔹 **🔍 Buscar Instrumentos Financieros**
```http
GET /instruments?query=AAPL&id_type=TICKER&market=US
```
📌 **Parámetros:**
- `query` → Identificador a buscar (Ejemplo: `AAPL`)
- `id_type` → (`TICKER`, `ID_ISIN`, `ID_BB_GLOBAL`, `ID_SEDOL`, `ID_COMMON`, `ID_WERTPAPIER`, `ID_CUSIP`, `ID_CINS`, `ID_MIC`, `ID_EXCH_SYMBOL`; default `TICKER`)
- `market` → Mercado/bolsa (Ejemplo: `US`; default `US`)

### 🔹 **📈 Obtener Precios de Acciones**
```http
GET /prices?symbol=AAPL&interval=daily
```
📌 **Parámetros:**
- `symbol` → Símbolo bursátil (Ejemplo: `AAPL`)
- `interval` → (`daily`, `1min`, `5min`, `15min`, `30min`, `60min`)

⚠️ Sujeto al límite de Alpha Vantage (5 llamadas/minuto) — devuelve `429` al excederlo.

### 🔹 **💰 Obtener Estado de Resultados**
```http
GET /financials?symbol=AAPL&period=annual
```
📌 **Parámetros:**
- `symbol` → Símbolo bursátil (Ejemplo: `AAPL`)
- `period` → (`annual` o `quarterly`)

### 🔹 **📊 Obtener Ratios Financieros**
```http
GET /financials/ratios?symbol=AAPL&period=annual
```
📌 **Parámetros:**
- `symbol` → Símbolo bursátil (Ejemplo: `AAPL`)
- `period` → (`annual` o `quarterly`)

### 🔹 **📰 Obtener Noticias Financieras**
```http
GET /news?query=Apple&limit=5&sort_by=publishedAt
```
📌 **Parámetros:**
- `query` → Palabra clave para buscar noticias.
- `limit` → Máximo de noticias a devolver.
- `sort_by` → (`relevancy`, `popularity`, `publishedAt`)

Una búsqueda sin resultados devuelve `200` con `{"total_results": 0, "articles": []}`, no un error.

---

## 🧪 Pruebas
Ejecutar tests con:
```sh
pytest app/tests/
```

---

## 📤 Despliegue
Para producción, usa:
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🎯 Contribuir
1. **Fork** el repositorio.
2. Crea una **rama** (`git checkout -b feature-nueva`).
3. **Commitea** (`git commit -m "Agregada nueva funcionalidad"`).
4. **Push** (`git push origin feature-nueva`).
5. Abre un **Pull Request**.

---

## 📜 Licencia
Este proyecto está bajo la licencia **MIT**.

