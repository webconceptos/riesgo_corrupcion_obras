# 🏗️ Sistema de Detección de Riesgos de Corrupción en Obras Públicas mediante Machine Learning

**Repositorio oficial del proyecto de tesis de Maestría en Inteligencia Artificial – UNI**  
**Autores:** Fernando García Atúncar / Hilario Aradiel Castañeda  
**Proyecto:** Sistema de identificación y priorización de obras públicas con riesgo potencial de corrupción en el Perú  
**Versión:** `v0.1.0-sprint1`

---

## 🎯 Objetivo del proyecto

Desarrollar un sistema basado en **Machine Learning** que permita identificar y priorizar **obras públicas con riesgo potencial de corrupción**, integrando información de obras, empresas, procesos de contratación y actores vinculados.

El sistema busca apoyar un enfoque de control más **preventivo, predictivo y basado en datos**, mediante un pipeline reproducible de procesamiento, entrenamiento, evaluación e inferencia.

---

## 🧠 Problema que aborda

La ejecución de obras públicas presenta riesgos asociados a sobrecostos, retrasos, deficiencias contractuales, concentración de proveedores, antecedentes de empresas y señales tempranas de irregularidad.

El enfoque tradicional de control suele ser principalmente reactivo. Este proyecto propone una estrategia basada en datos para:

- Detectar patrones de riesgo.
- Priorizar obras para evaluación o auditoría.
- Reducir la dependencia de revisión manual no focalizada.
- Fortalecer la toma de decisiones mediante evidencia.

---

## 🧭 Estado actual del Sprint 1

En el Sprint 1 se consolidó un **baseline funcional y reproducible** del sistema:

- Estructura profesional del repositorio.
- Pipeline base de datos y modelado.
- Modelo oficial en `models/production/`.
- API de inferencia con FastAPI.
- Endpoints de salud, metadata y predicción.
- Separación entre código productivo, notebooks, experimentos y documentación.
- Pruebas automáticas con PyTest.
- Configuración para despliegue con Docker.

---

## 🧱 Arquitectura general

```text
Fuentes de datos
    ↓
Ingesta y preprocesamiento
    ↓
Feature engineering
    ↓
Modelo de Machine Learning
    ↓
API FastAPI
    ↓
Predicción de riesgo / priorización
```

Arquitectura por capas:

```text
src/
├── api/        # Servicio REST con FastAPI
├── config/     # Configuración y rutas del sistema
├── data/       # Ingesta y preprocesamiento
├── features/   # Ingeniería de características
├── models/     # Entrenamiento, evaluación e inferencia
└── utils/      # Utilidades generales
```

---

## 🗂️ Estructura del repositorio

```text
riesgo_corrupcion_obras/
├── .github/                 # Workflows CI/CD
├── apps/                    # Frontend o componentes demostrativos
├── data/
│   ├── raw/                 # Datos originales no versionados
│   ├── processed/           # Datos procesados
│   └── external/            # Catálogos y fuentes externas
├── docs/
│   ├── dataset.md           # Descripción de datos
│   ├── run_guide.md         # Guía de ejecución
│   ├── deployment.md        # Despliegue
│   ├── entregables/         # Evidencias académicas
│   └── evidencias/          # Capturas y soportes
├── models/
│   ├── production/          # Modelo oficial del Sprint 1
│   │   ├── pipeline.pkl
│   │   └── pipeline_meta.json
│   └── experiments/         # Experimentos no productivos
├── notebooks/
│   ├── 01_eda/              # Exploración
│   ├── 02_data/             # Construcción de dataset
│   ├── 03_modeling/         # Entrenamiento
│   ├── 04_evaluation/       # Evaluación
│   └── experiments/         # Experimentos por sprint
├── reports/                 # Reportes y figuras
├── scripts/
│   ├── dev/                 # Scripts de desarrollo
│   ├── ops/                 # Operación y ejecución
│   ├── experiments/         # Scripts experimentales
│   └── legacy/              # Código histórico
├── src/                     # Código fuente principal
├── tests/                   # Pruebas automáticas
├── .env.example             # Variables de entorno de ejemplo
├── .gitignore
├── CHANGELOG.md
├── Dockerfile.prod
├── docker-compose.prod.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```
## 📊 Dataset

El modelo se entrena a partir de un dataset consolidado que integra información de diversas fuentes institucionales relacionadas a la ejecución de obras públicas en el Perú.

### 🔗 Fuentes de datos

- OSCE / SEACE (contrataciones públicas)
- MEF (inversión pública)
- Contraloría General de la República
- Registros administrativos de obras, empresas y funcionarios

---

### 🧱 Estructura del dataset

El dataset final se encuentra en:

```text
data/processed/dataset_modelado.parquet
---
```

## ⚙️ Instalación local

### 1. Clonar repositorio

```bash
git clone https://github.com/webconceptos/riesgo_corrupcion_obras.git
cd riesgo_corrupcion_obras
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

Activar en Windows:

```powershell
.venv\Scripts\activate
```

Activar en Linux/Mac:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## 🔐 Configuración

Crear un archivo `.env` a partir de `.env.example`.

```bash
cp .env.example .env
```

Ejemplo de variables:

```env
ENV=dev
DATASET_PATH=data/processed/dataset_modelado.parquet
MODEL_PATH=models/production/pipeline.pkl
MODEL_META_PATH=models/production/pipeline_meta.json
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

---

## 🤖 Entrenamiento del modelo

Ejemplo de entrenamiento:

```bash
python src/models/train.py \
  --input data/processed/dataset_modelado.parquet \
  --target target_column \
  --model rf \
  --out models/production/pipeline.pkl \
  --meta-out models/production/pipeline_meta.json
```

Modelos soportados:

- `rf` → Random Forest
- `xgb` → XGBoost
- `lgbm` → LightGBM

Salida esperada:

```text
models/production/
├── pipeline.pkl
└── pipeline_meta.json
```

---

## 🚀 Ejecución de la API

```bash
uvicorn src.api.main:app --reload --port 8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

---

## 🔎 Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Verifica disponibilidad de la API y carga del modelo |
| `GET` | `/model_meta` | Devuelve metadata segura del modelo |
| `POST` | `/predict_proba` | Predicción batch con esquema validado |
| `POST` | `/predict_batch` | Endpoint alternativo para predicción batch simple |

### Ejemplo de solicitud

```json
{
  "filas": [
    {
      "feature_1": 10,
      "feature_2": "LIMA",
      "feature_3": 1250000
    }
  ]
}
```

### Ejemplo de respuesta

```json
{
  "resultados": [
    {
      "proba": 0.82,
      "threshold": 0.5,
      "riesgoso": true
    }
  ]
}
```

---

## 🧪 Pruebas automáticas

Ejecutar:

```bash
pytest -q
```

También se recomienda validar estilo:

```bash
ruff check .
ruff format .
```

---

## 🐳 Docker

Construcción y ejecución en modo producción:

```bash
docker compose -f docker-compose.prod.yml up --build
```

---

## 📊 Métricas del modelo

Las métricas se registran en `pipeline_meta.json` y pueden incluir:

| Métrica | Descripción |
|---|---|
| Accuracy | Exactitud global |
| Precision | Precisión sobre casos marcados como riesgosos |
| Recall | Capacidad de identificar casos riesgosos |
| F1-Score | Balance entre precisión y recall |
| ROC-AUC | Separabilidad del modelo |

> Las métricas del Sprint 1 son preliminares y deben validarse con nuevos datos, calibración y revisión de sesgos.

---

## 📓 Notebooks

Los notebooks documentan el proceso experimental y de investigación:

```text
notebooks/
├── 01_eda/
├── 02_data/
├── 03_modeling/
├── 04_evaluation/
└── experiments/
```

La implementación operativa del sistema se encuentra en `src/`.

---

## 📚 Documentación

Documentación complementaria:

- `docs/dataset.md` → estructura y descripción de datos
- `docs/run_guide.md` → guía de ejecución
- `docs/deployment.md` → despliegue
- `docs/entregables/` → evidencias académicas
- `docs/evidencias/` → capturas y soportes

---

## 🧩 Tecnologías principales

- Python 3.11+
- FastAPI
- Pandas / NumPy
- Scikit-learn
- XGBoost
- LightGBM
- Joblib
- PyTest
- Ruff
- Docker

---

## 🧭 Roadmap

### Sprint 1
- [x] Estructura profesional del repositorio
- [x] Modelo baseline funcional
- [x] API FastAPI
- [x] Metadata del modelo
- [x] Pruebas básicas

### Próximos pasos
- [ ] Calibración de probabilidades
- [ ] Endpoint `/explain` con SHAP
- [ ] Dashboard de priorización
- [ ] Registro de experimentos con MLflow
- [ ] Monitoreo de drift y desempeño
- [ ] Validación con expertos de control

---

## 👥 Autores

- Fernando García Atúncar @webconceptos
- Hilario Aradiel Castañeda

**Maestría en Inteligencia Artificial – Universidad Nacional de Ingeniería**

---

## ⚖️ Licencia

MIT License.

---

> La detección temprana de patrones de riesgo permite fortalecer el control preventivo, priorizar mejor los recursos y proteger la inversión pública.
