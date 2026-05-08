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

El proyecto cuenta actualmente con:

- Construcción del dataset especializado `obra_v4`
- Feature engineering multivariable
- Target multiclase oficial de riesgo
- Entrenamiento baseline multiclase
- Cross Validation estratificado
- Hyperparameter Tuning
- Exportación de modelo baseline oficial
- Pipeline reproducible de extremo a extremo

Estado de otros componentes:

| Componente | Estado |
|---|---|
| Dataset obra_v4 | ✔ Finalizado |
| Dataset empresa | ⚠ Exploratorio |
| Dataset funcionario | ⚠ Exploratorio |
| Dataset maestro definitivo | ⚠ Pendiente reconstrucción |

---

## Arquitectura del sistema

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

## Arquitectura de datos

```text
riesgo_corrupcion_obras/
├── data/
│   ├── raw/
│   ├── external/
│   ├── processed/
│   └── README.md
├── models/
│   ├── production/
│   └── experiments/
├── notebooks/
│   ├── 01_eda_diccionarios.ipynb
│   ├── 02_build_dataset_obra_v4_features_maestro.ipynb
│   ├── 02_build_dataset_empresa_v3_4_etiquetas.ipynb
│   ├── 02_build_dataset_funcionario_v3_4_etiquetas.ipynb
│   ├── 03_build_dataset_maestro_v2_4niveles_limpio.ipynb
│   ├── 03_train_obra_v4.ipynb
│   ├── 04_EDA_maestro.ipynb
│   ├── 05_train_baseline_maestro_4niveles.ipynb
│   └── README_notebooks.md
├── scripts/
├── src/
├── tests/
├── requirements.txt
└── README.md
```
##  Dataset

El modelo se entrena a partir de un dataset consolidado que integra información de diversas fuentes institucionales relacionadas a la ejecución de obras públicas en el Perú.

###  Fuentes de datos

- OSCE / SEACE (contrataciones públicas)
- MEF (inversión pública)
- Contraloría General de la República
- Registros administrativos de obras, empresas y funcionarios

---

###  Estructura del dataset

El dataset final se encuentra en:

```text
data/processed/dataset_obra_v4_model.parquet
---
```

## Dataset obra_v4

Unidad de análisis:

```text
1 fila = 1 obra
```

##  Instalación local

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
El pipeline actual se reproduce principalmente mediante notebooks ejecutados en orden.
notebooks/05_train_baseline_maestro_4niveles.ipynb

Este notebook genera:
models/production/pipeline_maestro_4niveles_baseline.pkl
models/production/pipeline_maestro_4niveles_baseline_meta.json


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
