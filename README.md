# Sistema de Detección y Priorización de Riesgos de Corrupción en Obras Públicas mediante Machine Learning

Repositorio oficial del proyecto de tesis de Maestría en Inteligencia Artificial orientado al desarrollo de un sistema predictivo para la detección temprana y priorización de riesgos de corrupción en obras públicas del Perú.

---

# Información General

## Proyecto de Investigación

**Título de tesis:**

> Estrategia Basada en Machine Learning para la Detección y Priorización de Riesgos de Corrupción en la Ejecución de Obras Públicas en la Contraloría General de la República

## Institución Académica

Universidad Nacional de Ingeniería – FIIS  
Maestría en Inteligencia Artificial

## Autores

- Fernando García Atúncar
- Hilario Aradiel Castañeda

## Estado actual del repositorio

```text
Versión actual: v0.4.0-sprint2-semana7
Estado: Sprint 2 finalizado
```

---

# Objetivo del Proyecto

Desarrollar un sistema basado en Machine Learning y Explainable AI (XAI) capaz de:

- detectar riesgos potenciales de corrupción
- priorizar obras públicas riesgosas
- identificar patrones anómalos
- apoyar la fiscalización preventiva
- fortalecer el control gubernamental basado en datos

El sistema utiliza información derivada de:

- obras públicas
- contrataciones públicas
- empresas contratistas
- funcionarios públicos
- ejecución contractual
- variables económicas
- patrones de participación

---

# Problema que Resuelve

El modelo tradicional de control gubernamental es predominantemente reactivo y posterior a la ocurrencia de irregularidades.
Este proyecto busca evolucionar hacia un enfoque:

```text
Preventivo + Predictivo + Basado en Datos
```

mediante técnicas de:
- Machine Learning
- Analítica avanzada
- Explainable AI
- Feature Engineering
- Modelamiento multientidad

---

# Evolución Experimental del Proyecto

El desarrollo del sistema se realiza mediante sprints incrementales.
Cada sprint representa una evolución metodológica respecto a la versión anterior.

---

# Sprint 1 — Variante 1

## Arquitectura Inicial

```text
OBRA + EMPRESA + FUNCIONARIO
```

## Objetivos

- validar arquitectura inicial
- explorar relaciones multientidad
- construir baseline preliminar
- evaluar viabilidad predictiva

## Resultados

### Problemas identificados

- riesgo de data leakage
- métricas inestables
- baja trazabilidad
- complejidad excesiva
- baja interpretabilidad

## Notebooks asociados

```text
04_EDA_maestro.ipynb - Eliminado
05_train_baseline_maestro_4niveles.ipynb - Eliminado
```

---

# Sprint 2 — Variante 2 (Baseline Oficial Actual)

En esta etapa se rediseñó completamente la arquitectura experimental.

## Cambio metodológico principal

Se adoptó una unidad de análisis consistente:

```text
1 fila = 1 obra pública
```

## Nuevo dataset especializado

```text
obra_v4
```

---

# Mejoras Implementadas

```text
✔ control de leakage
✔ feature engineering agregado
✔ pipelines reproducibles
✔ cross validation estratificado
✔ hyperparameter tuning
✔ reporting experimental
✔ exportación de artefactos
✔ validación experimental formal
```

---

# Notebooks Oficiales Sprint 2

```text
notebooks/
├── 01_eda_diccionarios.ipynb
├── 02_build_dataset_obra_v4_features_maestro.ipynb
├── 03_train_obra_v4.ipynb
├── 04_generate_reports_obra_v4.ipynb
└── README.md
```

---

# Resultados Experimentales Oficiales

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

---

# Interpretación Experimental

## Hallazgos relevantes

- El modelo RandomForest continúa siendo el baseline oficial del proyecto.
- El tuning de hiperparámetros no mejoró el Macro F1 respecto al baseline inicial.
- El pipeline alcanzó una estabilidad razonable considerando:
  - tamaño reducido del dataset
  - desbalance de clases
  - heterogeneidad institucional
  - complejidad de variables

## Variables más relevantes

Las variables con mayor importancia predictiva estuvieron asociadas principalmente a:

- montos ofertados
- dispersión económica
- número de participantes
- composición del comité
- ratios de competencia
- patrones contractuales
- ejecución de obra

Esto evidencia que el comportamiento económico y competitivo de los procesos contiene señales relevantes asociadas al riesgo de corrupción.

---

# Estado Actual del Sistema

| Componente | Estado |
|---|---|
| Dataset obra_v4 | ✔ Finalizado |
| Feature Engineering | ✔ Finalizado |
| Baseline ML | ✔ Finalizado |
| Cross Validation | ✔ Finalizado |
| Hyperparameter Tuning | ✔ Finalizado |
| Reporting Experimental | ✔ Finalizado |
| Exportación de artefactos | ✔ Finalizado |
| Explainability SHAP | En progreso |
| Dataset empresa | Exploratorio |
| Dataset funcionario | Exploratorio |
| Dataset maestro definitivo | Pendiente |

---

# Arquitectura del Sistema

```text
Fuentes institucionales
(SEACE / SIAF / SIGA / INFOBRAS / INVIERTE)
                    ↓
Ingesta y validación
                    ↓
Normalización
                    ↓
Feature Engineering
                    ↓
Construcción obra_v4
                    ↓
Entrenamiento baseline
                    ↓
Cross Validation
                    ↓
Hyperparameter Tuning
                    ↓
Reporting experimental
                    ↓
Explainability (SHAP)
                    ↓
API de inferencia
```

---

# Estructura del Repositorio

```text
project/
│
├── notebooks/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── models/
│   └── obra_v4/
│
├── reports/
│   └── figures/
│
├── src/
│
└── README.md
```

---

# Dataset Principal

## Dataset baseline oficial

```text
data/processed/dataset_obra_v4_model.parquet
```

## Unidad de análisis

```text
1 fila = 1 obra
```

## Target oficial

```text
y_riesgo_obra
```

---

# Modelos Evaluados

- Logistic Regression
- Gradient Boosting
- Random Forest
- Random Forest Tuned

---

# Mejor Modelo Actual

```python
RandomForestClassifier
```

---

# Artefactos Generados

## Modelos

```text
models/obra_v4/
├── pipeline_rf_obra_v4.pkl
├── metrics_rf_obra_v4.json
└── feature_importance_rf_obra_v4.csv
```

## Reportes y figuras

```text
reports/figures/
├── confusion_matrix_rf_tuned.png
├── feature_importance_rf_tuned.png
├── model_comparison.png
└── target_distribution.png
```

---

# Validaciones Metodológicas

Durante el desarrollo experimental se identificaron y corrigieron:

```text
✔ data leakage
✔ contaminación train/test
✔ variables derivadas del target
✔ sobreajuste
✔ inconsistencias de granularidad
✔ evaluación sesgada
```

---

# Explainable AI (XAI)

El proyecto incorpora progresivamente mecanismos de interpretabilidad orientados a:

- transparencia algorítmica
- auditabilidad institucional
- explicabilidad de decisiones
- trazabilidad predictiva
- reducción de sesgos

## Técnicas previstas

- SHAP
- LIME
- Feature Importance
- Local Explanations

---

# Roadmap del Proyecto

## Sprint 3

```text
→ indicaciones del profesor
```

## Sprint 4

```text
→ indicaciones del profesor
```

## Sprint 5

```text
→ indicaciones del profesor
```

---

# Visión Objetivo

La arquitectura objetivo del sistema evoluciona hacia:

```text
OBRA + EMPRESA + FUNCIONARIO + REDES
```

permitiendo:

- detección temprana
- análisis relacional
- priorización inteligente
- alertas preventivas
- fiscalización basada en riesgo

---

# Tecnologías Utilizadas

## Lenguaje

- Python

## Machine Learning

- scikit-learn
- pandas
- numpy

## Visualización

- matplotlib
- seaborn

## Experimentación

- Jupyter Notebook

## Versionamiento

- Git
- GitHub

---

# Consideraciones Importantes

## Estado experimental

Este repositorio representa una investigación aplicada en evolución.

Los resultados pueden variar conforme:

- se incorporen nuevas fuentes
- se reduzcan sesgos
- se optimicen features
- se amplíen datasets
- se integren nuevos modelos

---

# Nota Final

El proyecto consolida actualmente una primera versión metodológicamente validada y reproducible de un sistema de detección de riesgos de corrupción basado en Machine Learning aplicado a obras públicas.

La investigación busca evolucionar progresivamente hacia arquitecturas multientidad más complejas orientadas a fortalecer el control gubernamental preventivo mediante inteligencia artificial.
