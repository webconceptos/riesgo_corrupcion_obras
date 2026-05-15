# Sistema de Detección de Riesgos de Corrupción en Obras Públicas mediante Machine Learning

Repositorio del proyecto de tesis de Maestría en Inteligencia Artificial – UNI

**Autores:** Fernando García Atúncar / Hilario Aradiel Castañeda  
**Versión:** v0.4.0-obra_v4-baseline  
**Entregable:** Sprint 2 – Semana 5 (08MAY2026)

---

# Objetivo del Proyecto

Desarrollar un sistema basado en Machine Learning capaz de identificar y priorizar obras públicas con riesgo potencial de corrupción utilizando información derivada de:

- Obras públicas
- Empresas contratistas
- Funcionarios públicos
- Contrataciones públicas
- Variables económicas y de ejecución

---

# Enfoque Actual del Proyecto

El proyecto evoluciona hacia una arquitectura multi-actor:

OBRA + EMPRESA + FUNCIONARIO

Sin embargo, el baseline oficial actual del sistema está construido sobre el dataset especializado:

obra_v4

el cual representa la primera versión validada metodológicamente del pipeline ML.

---

# Estado Actual

El proyecto cuenta actualmente con:

- Construcción del dataset especializado `obra_v4`
- Feature engineering multivariable
- Target multiclase oficial de riesgo
- Entrenamiento baseline multiclase
- Cross Validation estratificado
- Hyperparameter Tuning
- Exportación de modelo baseline oficial
- Pipeline reproducible de extremo a extremo
- Corrección y validación de data leakage

---

## Estado de Componentes

| Componente | Estado |
|---|---|
| Dataset obra_v4 | ✔ Finalizado |
| Feature Engineering | ✔ Finalizado |
| Baseline ML | ✔ Finalizado |
| Cross Validation | ✔ Finalizado |
| Hyperparameter Tuning | ✔ Finalizado |
| Dataset empresa | ⚠ Exploratorio |
| Dataset funcionario | ⚠ Exploratorio |
| Dataset maestro definitivo | ⚠ Pendiente reconstrucción |

---

# Arquitectura del Sistema

Fuentes de datos
↓
Ingesta y normalización
↓
Construcción de datasets especializados
↓
Construcción obra_v4
↓
Feature Engineering
↓
Modelo baseline RF
↓
Cross Validation
↓
Hyperparameter Tuning
↓
Exportación modelo final
↓
API de inferencia

---

# Dataset Principal

data/processed/dataset_obra_v4_model.parquet

---

# Dataset obra_v4

## Unidad de análisis

1 fila = 1 obra

## Target Oficial

y_riesgo_obra_5niveles

---

# Modelos Evaluados

- Logistic Regression
- Gradient Boosting
- Random Forest

---

# Mejor Modelo Actual

RandomForestClassifier

---

# Métricas Aproximadas

| Métrica | Valor |
|---|---:|
| Accuracy | ~0.58 |
| Balanced Accuracy | ~0.41 |
| Macro F1 | ~0.43 |

---

# Pipeline Reproducible

notebooks/02_build_dataset_obra_v4_features_maestro.ipynb

notebooks/03_train_obra_v4.ipynb

---

# Artefactos Generados

models/obra_v4/

- pipeline_rf_obra_v4.pkl
- metrics_rf_obra_v4.json
- feature_importance_rf_obra_v4.csv

---

# Roadmap

- Rediseño datasets empresa y funcionario
- Construcción nuevo dataset maestro
- XGBoost / LightGBM
- SHAP Explainability
- Detección de redes de riesgo

---

# Autores

Fernando García Atúncar  
Hilario Aradiel Castañeda

Maestría en Inteligencia Artificial – UNI
