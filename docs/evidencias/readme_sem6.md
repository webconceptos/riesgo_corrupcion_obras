# 🧠 Semana 6 – Entrenamiento y Evaluación de Modelos Predictivos

## 🎯 Objetivo del sprint
Implementar el pipeline de **modelado predictivo supervisado** para detectar **obras públicas con riesgo de corrupción**, integrando los datasets de obras, empresas y funcionarios.  
Esta fase corresponde al **Sprint 6** del proyecto de tesis “Sistema de Detección de Riesgos de Corrupción en Obras Públicas mediante Machine Learning”.

---

## ⚙️ 1. Contexto del proyecto

- **Propósito:** desarrollar un sistema que permita identificar obras públicas con indicadores de alto riesgo de corrupción, utilizando fuentes oficiales y técnicas de *machine learning*.
- **Datasets:** integrados a partir de los CSVs ubicados en `data/external/obra`, `empresa` y `funcionario`.
- **Salida procesada:**  
  - `data/processed/dataset_obras.parquet`  
  - `data/processed/dataset_integrado.parquet`
- **Variable objetivo:** `y_riesgo` (1 = Riesgo alto, 0 = Sin riesgo)
- **Tamaño final del dataset integrado:** 14,179 filas × 56 columnas.

---

## 🧩 2. Línea base (baseline)

El modelo base utilizado fue **Regresión Logística**, con balanceo de clases (`class_weight="balanced"`).  
Este baseline permite establecer un punto de comparación para variantes más complejas.

**Configuración:**
```python
LogisticRegression(max_iter=1000, solver="lbfgs", class_weight="balanced")
```

**Advertencia técnica:**  
El optimizador `lbfgs` alcanzó el límite de iteraciones inicial (200), por lo que se ajustó a `max_iter=1000` para lograr convergencia estable sin afectar el rendimiento general del modelo.

---

## 🧪 3. Experimentos A/B

Se evaluaron **3 variantes principales** y una adicional opcional:

| Variante | Modelo | Descripción técnica |
|-----------|---------|---------------------|
| Var1 | Logistic Regression | Línea base con escalado y codificación categórica |
| Var2 | Random Forest | Ensamble con `n_estimators=200`, `class_weight="balanced_subsample"` |
| Var3 | XGBoost | Boosting con `max_depth=6`, `learning_rate=0.1`, `subsample=0.9` |
| (Opc.) | MLP | Red neuronal con capas ocultas (64, 32), activación ReLU |

**Preprocesamiento común:**
- Imputación de valores nulos (`SimpleImputer`)
- Escalado de variables numéricas (`StandardScaler`)
- Codificación de variables categóricas (`OneHotEncoder`)
- Validación cruzada estratificada (k=5)

---

## 📊 4. Resultados comparables

Los resultados se almacenan automáticamente en `reports/metrics_semana6.csv`  
con las métricas **F1**, **ROC-AUC**, **PR-AUC** y tiempo promedio de ejecución por modelo.

| Modelo | F1 | ROC-AUC | PR-AUC | Tiempo (s) | Seleccionado |
|:-------|---:|--------:|-------:|------------:|:-------------:|
| Regresión Logística | 0.67 | 0.74 | 0.70 | 3.5 | – |
| Random Forest | 0.75 | 0.82 | 0.78 | 8.1 | – |
| **XGBoost** | **0.81** | **0.88** | **0.84** | 5.4 | ✅ |
| MLP | 0.77 | 0.86 | 0.80 | 9.3 | – |

📁 **Artefactos generados:**
- `models/pipeline.pkl` → pipeline entrenado del mejor modelo  
- `models/pipeline_meta.json` → metadatos del modelo  
- `reports/metrics_semana6.csv` → registro acumulado de métricas  
- `reports/figures/` → gráficas ROC y PR Curve  

---

## 🧮 5. Validación y sanidad

- División **estratificada** (80/20) sin *leakage* entre folds.  
- `random_state=42` para reproducibilidad.  
- Limpieza de columnas duplicadas y verificación de nulos (`SimpleImputer`).  
- Revisión de correlaciones anómalas en features numéricos.

---

## 🧠 6. Conclusión técnica

- **XGBoost** demostró ser el modelo más robusto, logrando el mejor equilibrio entre precisión, recall y estabilidad.  
- La imputación automática de valores faltantes y la normalización mejoraron significativamente la convergencia.  
- Se estableció un pipeline reproducible para futuras etapas de explicabilidad y despliegue.

---

## 🧾 7. Reproducibilidad

### 🧰 Requisitos
```bash
pip install -r requirements.txt
```

### 🏗️ Construcción de datasets
```bash
python scripts/build_dataset_ml.py
python scripts/build_dataset_integrado.py
```

### 🤖 Entrenamiento de modelos
```bash
python scripts/train_models.py --folds 5
```

### 📈 Evaluación y gráficas
```bash
python scripts/eval_holdout.py
python scripts/plot_curves.py
```

---

## ⚠️ 8. Riesgos y próximos pasos

**Riesgos detectados:**
- Posible *data drift* entre fuentes 2023–2025.  
- Campos heterogéneos entre dominios (obras, empresas, funcionarios).  
- Duplicidad de indicadores con distinto origen institucional.

**Acciones inmediatas (Semana 7):**
1. Exploración EDA avanzada (`EDA_Semana7.ipynb`)  
2. Interpretabilidad con **SHAP/LIME** sobre el modelo XGBoost.  
3. Refinamiento de variables más influyentes (`feature importance`).  
4. Análisis de sesgos y validación temporal cruzada.  
5. Preparar pipeline de despliegue para FastAPI / Docker.

---

## 📚 9. Referencias técnicas

- Scikit-learn 1.5.0 — [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)  
- XGBoost Documentation — [https://xgboost.readthedocs.io/](https://xgboost.readthedocs.io/)  
- Contraloría General de la República (CGR) – Datos abiertos e informes institucionales (2023–2025).  
- Proyecto BID-3 (CT PE-T1600) – Estrategia de fortalecimiento del control gubernamental.  

---

📘 **Autor:** Fernando García - Hilario Aradiel  
📅 **Sprint:** Semana 6 – Modelado Predictivo  
📂 **Repositorio:** [webconceptos/Deteccion_Corrupcion](https://github.com/webconceptos/Deteccion_Corrupcion)
