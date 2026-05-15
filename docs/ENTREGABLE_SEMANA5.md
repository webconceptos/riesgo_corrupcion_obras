# ENTREGABLE SEMANA 5

## Sistema de Detección de Riesgos de Corrupción en Obras Públicas mediante Machine Learning

### Sprint 2 — Semana 5
### Fecha: 15/05/2026

---

## Autores

- Fernando García Atúncar
- Hilario Aradiel Castañeda

Maestría en Inteligencia Artificial – UNI

---

# 1. Objetivo del Sprint

El objetivo de esta iteración fue consolidar un pipeline reproducible de Machine Learning para la detección de riesgos de corrupción en obras públicas, utilizando el dataset especializado `obra_v4`.

Asimismo, se buscó validar metodológicamente el baseline oficial del proyecto mediante:

- entrenamiento multiclase
- comparación de algoritmos
- validación cruzada
- optimización de hiperparámetros
- generación de evidencia experimental

---

# 2. Arquitectura Metodológica

El proyecto evoluciona hacia una arquitectura multi-actor:

```text
OBRA + EMPRESA + FUNCIONARIO
```

Sin embargo, en esta etapa se decidió trabajar inicialmente sobre una unidad de análisis consistente:

```text
1 fila = 1 obra
```

lo cual permitió reducir complejidad, mejorar estabilidad y controlar riesgos de data leakage.

---

# 3. Dataset Utilizado

## Dataset oficial

```text
data/processed/dataset_obra_v4_model.parquet
```

---

## Dimensiones

| Elemento | Valor |
|---|---:|
| Registros | 326 |
| Variables | 33 |
| Features utilizadas | 31 |
| Target | y_riesgo_obra_5niveles |

---

## Distribución del Target

| Clase | Descripción |
|---|---|
| 0 | Sin Riesgo |
| 1 | Bajamente Riesgosa |
| 2 | Medianamente Riesgosa |
| 3 | Altamente Riesgosa |
| 4 | Extremadamente Riesgosa |

---

# 4. Feature Engineering

El dataset `obra_v4` incorpora variables derivadas de:

## Comité de selección

- número de miembros
- DNIs únicos
- convocatorias asociadas
- ratios de repetición

---

## Participación empresarial

- número de participantes
- número de RUCs
- contratos asociados
- ratios de participación

---

## Variables económicas

- promedio de ofertas
- desviación estándar
- rango de ofertas
- coeficiente de variación

---

## Variables de ejecución

- montos planificados
- montos reales
- desviaciones
- registros temporales
- ratio real vs planificado

---

# 5. Prevención de Data Leakage

Durante el entrenamiento se identificaron variables con riesgo de contaminación del modelo debido a su asociación directa con el target.

Por ello se eliminaron:

```text
IDENTIFICADOR_OBRA
RIESGO_DESCRIPCION_OBRA
```

Asimismo, todas las transformaciones fueron ajustadas exclusivamente sobre el conjunto de entrenamiento.

---

# 6. Modelos Evaluados

| Modelo | Accuracy | Macro F1 |
|---|---:|---:|
| Logistic Regression | 0.333 | 0.193 |
| Gradient Boosting | 0.545 | 0.402 |
| Random Forest | 0.561 | 0.408 |
| Random Forest Tuned | 0.576 | 0.427 |

---

# 7. Validación Cruzada

Se aplicó validación cruzada estratificada de 5 folds para evaluar estabilidad y capacidad de generalización del modelo.

La validación permitió verificar consistencia en las métricas obtenidas y reducir riesgo de sobreajuste.

---

# 8. Hyperparameter Tuning

Se aplicó `RandomizedSearchCV` sobre el modelo Random Forest utilizando múltiples combinaciones de hiperparámetros.

## Mejores parámetros encontrados

```json
{
  "bootstrap": false,
  "max_depth": 10,
  "max_features": "log2",
  "min_samples_leaf": 1,
  "min_samples_split": 5,
  "n_estimators": 661
}
```

---

# 9. Resultados Relevantes

Las variables con mayor importancia predictiva fueron:

- montos ofertados
- número de participantes
- ratios de participación
- variabilidad económica
- composición del comité

Esto sugiere que el comportamiento económico y competitivo de los procesos contiene señales relevantes asociadas al riesgo de corrupción.

---

# 10. Artefactos Generados

## Modelos

```text
models/obra_v4/pipeline_rf_obra_v4.pkl
```

---

## Métricas

```text
models/obra_v4/metrics_rf_obra_v4.json
```

---

## Importancia de variables

```text
models/obra_v4/feature_importance_rf_obra_v4.csv
```

---

## Figuras

```text
reports/figures/confusion_matrix_rf_tuned.png
reports/figures/feature_importance_rf.png
reports/figures/model_comparison.png
```

---

# 11. Notebooks Oficiales

## Construcción dataset

```text
02_build_dataset_obra_v4_features_maestro.ipynb
```

---

## Entrenamiento

```text
03_train_obra_v4.ipynb
```

---

## Reporting

```text
06_generate_reports_obra_v4.ipynb
```

---

# 12. Conclusiones

- El modelo Random Forest obtuvo el mejor desempeño general.
- El tuning permitió mejorar ligeramente las métricas del baseline inicial.
- Las variables económicas mostraron alta capacidad predictiva.
- El dataset presenta desbalance de clases, especialmente en niveles intermedios de riesgo.
- La corrección de data leakage permitió obtener métricas más realistas y metodológicamente válidas.
- El pipeline actual constituye el baseline oficial reproducible del proyecto.

---

# 13. Próximos Pasos

- reconstrucción del dataset maestro
- integración obra–empresa–funcionario
- incorporación de modelos avanzados
- explainability mediante SHAP
- detección de redes de riesgo
- despliegue de API de inferencia

---

# Nota Final

El presente sprint consolida la primera versión reproducible y validada metodológicamente del sistema de detección de riesgos de corrupción basado en Machine Learning aplicado a obras públicas.