# Sistema de Detección y Priorización de Riesgos de Corrupción en Obras Públicas

## README — Carpeta `/notebooks`

Proyecto de investigación aplicado a la detección temprana de riesgos de corrupción en obras públicas del Perú mediante técnicas de Machine Learning, Explainable AI (XAI) y analítica avanzada orientada al control gubernamental.

---

# Descripción General

Este directorio contiene los notebooks utilizados para la construcción, análisis, modelado y evaluación experimental del sistema de detección de riesgos de corrupción en obras públicas.

⚠️ Este README documenta únicamente la carpeta `/notebooks` y sus flujos analíticos experimentales.  
El README principal del repositorio será desarrollado posteriormente cuando se integren reportes, arquitectura completa y componentes adicionales del sistema.

---

# Objetivo de los Notebooks

Los notebooks tienen como finalidad:

- explorar y validar datasets institucionales
- construir datasets especializados
- realizar feature engineering
- entrenar modelos predictivos
- evaluar métricas experimentales
- validar hipótesis analíticas
- reducir riesgos de data leakage
- construir el baseline oficial del sistema

---

# Flujo Experimental Actual

```text
EDA Inicial
    ↓
Validación de datasets
    ↓
Feature Engineering
    ↓
Construcción dataset obra_v4
    ↓
Entrenamiento baseline
    ↓
Cross Validation
    ↓
Hyperparameter Tuning
    ↓
Evaluación experimental
    ↓
Exportación de artefactos
```

---

# Notebooks Principales

## 1. Exploración Inicial y Calidad de Datos

### `01_eda_diccionarios.ipynb`

Notebook orientado a:

- exploración inicial
- análisis de diccionarios
- identificación de variables
- validación de tipos de datos
- análisis de relaciones
- detección de inconsistencias
- evaluación de granularidad
- análisis de calidad de datos

### Funciones principales

```text
✔ profiling de datasets
✔ análisis de nulos
✔ análisis de cardinalidad
✔ revisión de llaves
✔ identificación de variables críticas
✔ validación relacional
```

---

## 2. Construcción del Dataset Especializado

### `02_build_dataset_obra_v4_features_maestro.ipynb`

Notebook principal del pipeline actual.

Construye el dataset especializado `obra_v4`, considerado actualmente el baseline experimental oficial del proyecto.

### Incluye

```text
✔ integración multifuente
✔ consolidación de tablas
✔ normalización
✔ agregaciones por obra
✔ feature engineering
✔ consolidación económica
✔ consolidación contractual
✔ consolidación de participantes
✔ consolidación de comité
✔ consolidación de ejecución
✔ construcción del target
```

### Unidad de análisis

```text
1 fila = 1 obra pública
```

### Dataset generado

```text
dataset_obra_v4_model.parquet
```

---

## Variables relevantes generadas

- montos adjudicados
- variabilidad de ofertas
- cantidad de participantes
- comportamiento contractual
- ampliaciones
- patrones de comité
- señales de concentración
- indicadores de ejecución
- variables financieras
- variables de competencia

---

## 3. Entrenamiento Baseline

### `03_train_obra_v4.ipynb`

Notebook de entrenamiento y evaluación experimental del baseline actual.

### Incluye

```text
✔ train/test split estratificado
✔ pipelines de entrenamiento
✔ evaluación multiclase
✔ comparación de modelos
✔ cross validation
✔ tuning de hiperparámetros
✔ feature importance
✔ exportación del modelo
✔ exportación de métricas
```

---

# Modelos Evaluados

- Random Forest
- Gradient Boosting
- Logistic Regression

---

# Técnicas Aplicadas

## Cross Validation

```text
Stratified K-Fold
```

## Hyperparameter Tuning

```text
RandomizedSearchCV
```

## Evaluación Experimental

- Accuracy
- Macro F1
- Balanced Accuracy
- Confusion Matrix
- Feature Importance

---

# Mejor Modelo Actual

```text
RandomForestClassifier
```

---

# Resultados Experimentales Oficiales — Notebook 03

```text
============================================================
RESUMEN NOTEBOOK 03 — obra_v4
============================================================

Dataset          : 326 obs × 77 features
Target           : 4 niveles (Decisión D1)

Mejor modelo     : RandomForest (hold-out)

Macro F1 baseline: 0.5939
Macro F1 tuned   : 0.5804  (-2.3%)

Bal. Accuracy    : 0.5581
```

## Artefactos Generados

```text
models/obra_v4/pipeline_rf_obra_v4.pkl
models/obra_v4/metrics_rf_obra_v4.json
models/obra_v4/feature_importance_rf_obra_v4.csv

reports/figures/confusion_matrix_rf_tuned.png
reports/figures/feature_importance_rf_tuned.png
reports/figures/model_comparison.png
reports/figures/target_distribution.png
```

## Interpretación Experimental

- El modelo RandomForest continúa siendo el baseline oficial del proyecto.
- El tuning de hiperparámetros no mejoró el Macro F1 respecto al baseline inicial.
- La validación evidenció estabilidad razonable considerando:
  - desbalance de clases
  - tamaño reducido del dataset
  - heterogeneidad de variables
- El pipeline actual constituye una base sólida para el Sprint 3.

---

# Hallazgos Relevantes

Las variables con mayor importancia experimental fueron:

- montos ofertados
- dispersión económica
- cantidad de postores
- patrones de comité
- variables de ejecución
- comportamiento contractual

---

# Validaciones Metodológicas

Durante el proceso experimental se identificaron y corrigieron:

```text
✔ data leakage
✔ evaluación contaminada
✔ variables derivadas del target
✔ sobreestimación de métricas
✔ inconsistencias de granularidad
```

---

# Arquitectura Experimental Actual

```text
EDA
 ↓
Feature Engineering
 ↓
Dataset obra_v4
 ↓
Baseline ML
 ↓
Validación
 ↓
Explainability (próximo)
```

---

# Artefactos Generados

```text
models/
└── obra_v4/
    ├── pipeline_rf_obra_v4.pkl
    ├── metrics_rf_obra_v4.json
    └── feature_importance_rf_obra_v4.csv
```

---

# Estado Actual

| Componente | Estado |
|---|---|
| EDA inicial | ✔ |
| Dataset obra_v4 | ✔ |
| Feature engineering | ✔ |
| Baseline ML | ✔ |
| Cross Validation | ✔ |
| Hyperparameter tuning | ✔ |
| Exportación modelo | ✔ |
| Explainability SHAP | En progreso |
| Dataset maestro definitivo | Pendiente |
| Integración multientidad | Pendiente |

---

# Siguientes Pasos

```text
→ Sprint 3: incorporar dataset empresa + funcionario
→ SHAP explainability
→ Detección de redes de riesgo
→ API de inferencia
```

## Evolución Experimental Esperada

### Sprint 3
- integración multientidad
- consolidación relacional
- nuevas variables de riesgo

### Sprint 4
- explainability institucional
- SHAP global/local
- interpretabilidad avanzada

### Sprint 5
- scoring institucional
- inferencia vía API
- arquitectura MLOps

---

# Observaciones Importantes

Este directorio contiene notebooks experimentales y de investigación aplicada.

Los resultados y métricas pueden evolucionar conforme:

- se integren nuevas fuentes
- se mejoren los datasets
- se reduzcan sesgos
- se optimicen features
- se incorporen nuevos modelos

---

# Autores

- Fernando García Atúncar
- Hilario Aradiel Castañeda

Maestría en Inteligencia Artificial  
Universidad Nacional de Ingeniería – FIIS

---

# Licencia

Uso académico y de investigación.
