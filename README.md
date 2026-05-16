# Sistema de Detección de Riesgos de Corrupción en Obras Públicas mediante Machine Learning

Repositorio del proyecto de tesis de Maestría en Inteligencia Artificial – UNI

**Autores:**  
Fernando García Atúncar  
Hilario Aradiel Castañeda

**Versión actual:** v0.3.0-sprint2-semana5

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

```text
OBRA + EMPRESA + FUNCIONARIO
```

Sin embargo, el baseline oficial actual del sistema está construido sobre el dataset especializado:

```text
obra_v4
```

el cual representa la primera versión validada metodológicamente del pipeline ML reproducible.

---

# Evolución Experimental del Proyecto

El desarrollo del sistema se realiza mediante iteraciones incrementales orientadas a mejorar progresivamente la estabilidad, calidad y capacidad predictiva del modelo.

Cada sprint representa una evolución metodológica respecto a la variante anterior.

---

## Sprint 1 — Variante 1

En la primera iteración se construyó un dataset maestro preliminar integrando información de:

```text
OBRA + EMPRESA + FUNCIONARIO
```

### Objetivos

- validar arquitectura inicial
- explorar relaciones multientidad
- construir baseline preliminar
- evaluar viabilidad predictiva

### Notebooks asociados

```text
04_EDA_maestro.ipynb
05_train_baseline_maestro_4niveles.ipynb
```

### Problemas identificados

- riesgo de data leakage
- alta complejidad estructural
- dificultad de trazabilidad
- métricas inestables
- baja interpretabilidad

---

## Sprint 2 — Variante 2

En la segunda iteración se rediseñó la arquitectura hacia un dataset especializado `obra_v4`, utilizando una unidad de análisis consistente:

```text
1 fila = 1 obra
```

### Mejoras implementadas

- feature engineering agregado
- control de leakage
- pipeline reproducible
- comparación de algoritmos
- cross validation
- hyperparameter tuning
- reporting experimental

### Notebooks oficiales

```text
02_build_dataset_obra_v4_features_maestro.ipynb
03_train_obra_v4.ipynb
06_generate_reports_obra_v4.ipynb
```

### Resultados obtenidos

- mejora de estabilidad
- mejor interpretabilidad
- métricas más consistentes
- baseline oficial reproducible

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
- Generación de evidencia experimental visual

---

# Estado de Componentes

| Componente | Estado |
|---|---|
| Dataset obra_v4 | ✔ Finalizado |
| Feature Engineering | ✔ Finalizado |
| Baseline ML | ✔ Finalizado |
| Cross Validation | ✔ Finalizado |
| Hyperparameter Tuning | ✔ Finalizado |
| Reporting Experimental | ✔ Finalizado |
| Dataset empresa | ⚠ Exploratorio |
| Dataset funcionario | ⚠ Exploratorio |
| Dataset maestro definitivo | ⚠ Pendiente reconstrucción |

---

# Arquitectura del Sistema

```text
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
```

---

# Dataset Principal

```text
data/processed/dataset_obra_v4_model.parquet
```

---

# Dataset obra_v4

## Unidad de análisis

```text
1 fila = 1 obra
```

---

## Target Oficial

```text
y_riesgo_obra_5niveles
```

---

# Modelos Evaluados

- Logistic Regression
- Gradient Boosting
- Random Forest
- Random Forest Tuned

---

# Mejor Modelo Actual

```text
RandomForestClassifier
```

---

# Métricas Aproximadas

| Métrica | Valor |
|---|---:|
| Accuracy | ~0.58 |
| Balanced Accuracy | ~0.41 |
| Macro F1 | ~0.43 |

---

# Variables Más Relevantes

Las variables con mayor importancia predictiva estuvieron asociadas principalmente a:

- montos ofertados
- número de participantes
- ratios de participación
- variabilidad económica
- composición del comité

Esto sugiere que el comportamiento económico y competitivo de los procesos contiene señales relevantes asociadas al riesgo de corrupción.

---

# Pipeline Reproducible

## Construcción Dataset

```text
notebooks/02_build_dataset_obra_v4_features_maestro.ipynb
```

---

## Entrenamiento

```text
notebooks/03_train_obra_v4.ipynb
```

---

## Reporting Experimental

```text
notebooks/06_generate_reports_obra_v4.ipynb
```

---

# Artefactos Generados

## Modelos

```text
models/obra_v4/
```

- pipeline_rf_obra_v4.pkl
- metrics_rf_obra_v4.json
- feature_importance_rf_obra_v4.csv

---

## Figuras

```text
reports/figures/
```

- confusion_matrix_rf_tuned.png
- feature_importance_rf.png
- model_comparison.png

---

# Roadmap

- Rediseño datasets empresa y funcionario
- Reconstrucción del dataset maestro
- Integración multiactor
- XGBoost / LightGBM
- SHAP Explainability
- Detección de redes de riesgo
- API de inferencia

---

# Autor

Fernando García Atúncar  

Maestría en Inteligencia Artificial – UNI

---

# Nota Final

El proyecto consolida actualmente una primera versión reproducible y validada metodológicamente del sistema de detección de riesgos de corrupción basado en Machine Learning aplicado a obras públicas, permitiendo evolucionar progresivamente hacia arquitecturas multiactor más complejas.