# Sistema de Detección de Riesgos de Corrupción en Obras Públicas mediante Machine Learning

Repositorio del proyecto de tesis de Maestría en Inteligencia Artificial – UNI  
Autores: Fernando García Atúncar / Hilario Aradiel Castañeda  
Versión: v0.2.0-sprint1-final

---

## Objetivo del proyecto

Desarrollar un sistema basado en Machine Learning que permita identificar y priorizar obras públicas con riesgo potencial de corrupción, integrando información de:

- Obras públicas
- Empresas contratistas
- Funcionarios públicos

---

## Enfoque del problema

El riesgo de corrupción no depende de un solo factor, sino de la interacción entre:

OBRA + EMPRESA + FUNCIONARIO

Por ello, el sistema implementa una arquitectura multi-actor que permite capturar relaciones relevantes y mejorar la capacidad de detección.

---

## Estado actual

El proyecto cuenta con:

- Datasets especializados por tipo de actor
- Dataset maestro integrado
- Análisis exploratorio de datos (EDA)
- Modelo baseline multiclase
- Pipeline reproducible de datos y modelado

---

## Arquitectura del sistema

Fuentes de datos  
↓  
Ingesta y normalización  
↓  
Construcción de datasets especializados  
↓  
Dataset maestro  
↓  
Modelo de Machine Learning  
↓  
API de inferencia  

---

## Arquitectura de datos

<<<<<<< HEAD
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
=======
### Dataset de Obras
- Unidad: obra + participación
- Target: y_riesgo_obra_4niveles

### Dataset de Empresas
- Unidad: empresa + participación
- Target proxy: y_riesgo_empresa

### Dataset de Funcionarios
- Unidad: funcionario + obra
- Target proxy: y_riesgo_funcionario

### Dataset Maestro
- Unidad: IDENTIFICADOR_OBRA
- Integración de variables de obra, empresa y funcionario

---

## Análisis exploratorio (EDA)
>>>>>>> 0d9cfe5 (feat: Sprint 1 - Aactualiza pipeline ML multi-actor con dataset maestro, EDA y baseline)

El EDA incluye:

- Estadísticas descriptivas
- Distribución del target
- Análisis de outliers
- Correlación entre variables

### Riesgos identificados

- Desbalance de clases
- Data leakage (variables eliminadas)
- Posible drift temporal

---

## Modelo baseline

Modelo implementado:

- Regresión logística multiclase

Pipeline:

- Imputación de valores faltantes
- Codificación de variables categóricas (OneHotEncoder)
- Entrenamiento con class_weight="balanced"

Métricas utilizadas:

- Accuracy
- Balanced Accuracy
- Macro F1

---

## Notebooks

El pipeline es completamente reproducible a través de los siguientes notebooks:

- 01_eda_diccionarios.ipynb
- 02_build_dataset_obra_v3_4_etiquetas.ipynb
- 02_build_dataset_empresa_v3_4_etiquetas.ipynb
- 02_build_dataset_funcionario_v3_4_etiquetas.ipynb
- 03_build_dataset_maestro_v2_4niveles_limpio.ipynb
- 04_EDA_maestro.ipynb
- 05_train_baseline_maestro_4niveles.ipynb

Flujo reproducible:

EDA inicial  
→ construcción de datasets  
→ dataset maestro  
→ EDA final  
→ entrenamiento baseline  

---

## Reproducibilidad

El proyecto garantiza reproducibilidad mediante:

- Estructura clara del repositorio
- Uso de rutas relativas
- Versionamiento de dependencias (requirements.txt)
- Notebooks ejecutables de extremo a extremo
- Scripts de entrenamiento en src/
- Configuración mediante variables de entorno (.env)

Para reproducir:

1. Crear entorno virtual
2. Instalar dependencias
3. Ejecutar notebooks en orden
4. Entrenar modelo baseline
5. Ejecutar API opcionalmente

---

## Ejecución

Instalar dependencias:

pip install -r requirements.txt

Entrenar modelo:

python src/models/train.py

Levantar API:

uvicorn src.api.main:app --reload --port 8000

---

## Roadmap

- Modelos más avanzados (Random Forest, XGBoost)
- Interpretabilidad (SHAP)
- Monitoreo de drift
- Dashboard de priorización

---

## Autores

Fernando García Atúncar  
Hilario Aradiel Castañeda  

Maestría en Inteligencia Artificial – UNI

---

## Nota final

Este sistema implementa un enfoque reproducible y escalable para la detección de riesgos de corrupción, integrando múltiples fuentes de datos y permitiendo su extensión hacia modelos más avanzados.
