# 📊 API Financiera con FastAPI

## 📌 Descripción
Esta API permite consultar información financiera a través de múltiples fuentes de datos como **Alpha Vantage, Financial Modeling Prep (FMP), OpenFIGI y NewsAPI**.

✅ Desarrollada con **FastAPI** para alto rendimiento.  
✅ Usa **Redis** para cacheo y optimización.  
✅ Implementa **pytest** para pruebas automáticas.  
✅ Arquitectura modular con separación de servicios.  

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
### 🔹 **📈 Obtener Precios de Acciones**
```http
GET /prices?symbol=AAPL&interval=daily
```
📌 **Parámetros:**
- `symbol` → Símbolo bursátil (Ejemplo: `AAPL`)
- `interval` → (`daily`, `1min`, `5min`, etc.)

### 🔹 **💰 Obtener Ratios Financieros**
```http
GET /financials?symbol=AAPL&period=annual
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

---

## 🧪 Pruebas
Ejecutar tests con:
```sh
pytest tests/
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

