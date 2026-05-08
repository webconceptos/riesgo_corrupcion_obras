# Notebooks – Sistema de Detección de Riesgos de Corrupción en Obras Públicas

**Entregable:** 08MAY2026  
**Autor:** Fernando García Atúncar

---

## Descripción General

Este directorio contiene los notebooks utilizados para la construcción, análisis, modelado y evaluación del sistema de detección de riesgos de corrupción en obras públicas del Perú.

Actualmente el proyecto se encuentra centrado en el desarrollo y validación del dataset especializado de obras (`obra_v4`), el cual constituye el baseline oficial actual del sistema.

---

# Objetivo del Proyecto

Desarrollar un sistema de Machine Learning capaz de identificar niveles de riesgo de corrupción en obras públicas utilizando variables derivadas de:

- procesos de contratación
- participantes
- comités de selección
- montos ofertados
- ejecución de obra

---

# Flujo Metodológico Actual

```text
EDA Inicial
    ↓
Construcción de datasets especializados
    ↓
Feature Engineering
    ↓
Dataset obra_v4
    ↓
Entrenamiento baseline
    ↓
Cross Validation
    ↓
Hyperparameter Tuning
    ↓
Modelo baseline oficial
```

---

# Estructura de Notebooks

## 1. Exploración Inicial

### 01_eda_diccionarios.ipynb

Exploración de:
- diccionarios de datos
- tipos de variables
- relaciones entre datasets
- análisis inicial de calidad de datos

---

## 2. Construcción de Datasets Especializados

### 02_build_dataset_obra_v4_features_maestro.ipynb

Notebook principal de construcción del dataset `obra_v4`.

Incluye:
- integración de múltiples tablas de obras públicas
- construcción de features agregadas
- análisis de llaves y granularidad
- consolidación de variables económicas
- consolidación de variables de participación
- consolidación de variables de comité
- consolidación de variables de ejecución
- generación del target oficial:

```text
y_riesgo_obra_5niveles
```

### Unidad de análisis

```text
1 fila = 1 obra
```

### Resultado

Genera el dataset final:

```text
dataset_obra_v4_model.parquet
```

Este dataset constituye actualmente el baseline oficial del proyecto.

---

### 02_build_dataset_empresa_v3_4_etiquetas.ipynb

Versión inicial del dataset de empresas.

Estado:
- exploratorio
- pendiente de rediseño orientado a granularidad por obra

---

### 02_build_dataset_funcionario_v3_4_etiquetas.ipynb

Versión inicial del dataset de funcionarios.

Estado:
- exploratorio
- pendiente de rediseño orientado a granularidad por obra

---

## 3. Dataset Maestro

### 03_build_dataset_maestro_v2_4niveles_limpio.ipynb

Versión preliminar del dataset maestro.

Estado:
- experimental
- pendiente de reconstrucción usando la nueva arquitectura obra_v4

---

## 4. EDA Maestro

### 04_EDA_maestro.ipynb

EDA exploratorio del dataset maestro preliminar.

Incluye:
- estadísticas descriptivas
- análisis de distribución
- correlaciones
- identificación de riesgos de leakage

---

## 5. Baseline Inicial Maestro

### 05_train_baseline_maestro_4niveles.ipynb

Primer entrenamiento experimental sobre el dataset maestro preliminar.

Modelos evaluados:
- Random Forest

Estado:
- experimental
- será reemplazado posteriormente por una nueva versión basada en datasets refinados

---

## 6. Entrenamiento Baseline obra_v4

### 03_train_obra_v4.ipynb

Notebook de entrenamiento y evaluación del modelo baseline basado en `obra_v4`.

Incluye:
- separación train/test estratificada
- construcción de pipelines
- entrenamiento multiclase
- comparación de algoritmos
- feature importance
- cross validation
- hyperparameter tuning
- exportación del modelo final

---

## Modelos Evaluados

- Random Forest
- Gradient Boosting
- Logistic Regression

---

## Técnicas Aplicadas

### Cross Validation
Validación cruzada estratificada de 5 folds.

### Hyperparameter Tuning
Optimización mediante:

```text
RandomizedSearchCV
```

---

## Mejor Modelo Actual

```text
RandomForestClassifier
```

---

## Métricas Aproximadas

| Métrica | Valor |
|---|---:|
| Accuracy | ~0.58 |
| Macro F1 | ~0.42 |
| Balanced Accuracy | ~0.41 |

---

## Hallazgos Relevantes

Las variables con mayor importancia fueron:
- montos ofertados
- cantidad de participantes
- variabilidad de ofertas
- patrones de comité
- variables de ejecución

---

## Validaciones Metodológicas

Durante el desarrollo se identificaron y corrigieron:
- data leakage
- evaluación contaminada
- variables derivadas del target
- sobreestimación de métricas

---

## Artefactos Generados

```text
models/
└── obra_v4/
    ├── pipeline_rf_obra_v4.pkl
    ├── metrics_rf_obra_v4.json
    └── feature_importance_rf_obra_v4.csv
```

---

## Estado Actual del Proyecto

| Componente | Estado |
|---|---|
| EDA inicial | ✔ |
| Dataset obra_v4 | ✔ |
| Feature engineering | ✔ |
| Baseline ML | ✔ |
| Cross Validation | ✔ |
| Hyperparameter tuning | ✔ |
| Exportación modelo | ✔ |
| Dataset maestro definitivo | Pendiente |
| Integración empresa/funcionario | Pendiente |

---

## Próximos Pasos

- Rediseño de datasets empresa y funcionario orientados a obra
- Construcción del nuevo dataset maestro
- Integración relacional obra–empresa–funcionario
- SHAP Explainability
- XGBoost / LightGBM
- Detección de redes de riesgo
- Modelado multientidad anticorrupción
