# ================================================================
# Script: ExParcial_entrenar_modelos.py
# Entrenamiento del modelo final del Examen Parcial
# Adaptado al dataset REAL
# Autor: Fernando García - Hilario Aradiel
# Fecha: 2025-11-12
# ================================================================

import pandas as pd
import numpy as np
from datetime import datetime
import os

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# ================================================================
# 0. Paths y configuración inicial
# ================================================================

DATA_PATH = "data/processed/dataset_parcial_features.parquet"

os.makedirs("reports/tablas", exist_ok=True)
os.makedirs("reports/logs", exist_ok=True)

log_file = f"reports/logs/parcial_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(msg):
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log("=== INICIO DEL EXPERIMENTO (PARCIAL) ===")

# ================================================================
# 1. Cargar dataset
# ================================================================

log(f"Cargando dataset: {DATA_PATH}")

df = pd.read_parquet(DATA_PATH)

log(f"Registros cargados: {len(df)}")
log(f"Columnas disponibles: {list(df.columns)}")

# ================================================================
# 2. Features REALES corregidos
# ================================================================

features_num = [
    "TIEMPO_ABSOLUCION_CONSULTAS",
    "TIEMPO_PRESENTACION_OFERTAS",
    "MONTO_CONTRACTUAL",
    "MONTO_REFERENCIAL",
    "MONTO_OFERTADO_PROMEDIO",
    "MONTO_OFERTADO",
    "TOTALPROCESOSPARTICIPANTES",
    "DIAS_PLAZO",
    "TOTAL_CONTROL_PREVIO",
    "TOTAL_CONTROL_SIMULTANEO",
    "TOTAL_CONTROL_POSTERIOR",
    "PLANIFICADO",
    "REAL",
    "ANHO",
    "MES"
]

# Columnas que estaban mal como 'num'
features_cat = [
    "SECTOR",
    "DEPARTAMENTO",
    "NIVEL_GOBIERNO",
    "OBJETO_PROCESO",
    "METODO_CONTRATACION",
    "ESTADO_OBRA",
    "ETAPA",
    "IND_INTERVENSION",
    "IND_RESIDENTE",
    "IND_MONTO_ADELANTO_MATERIALES",
    "IND_MONTO_ADELANTO_DIRECTO"
]

X = df[features_num + features_cat]
y = df["y_riesgo"]

log("Variables numéricas utilizadas:")
log(str(features_num))

log("Variables categóricas utilizadas:")
log(str(features_cat))

# ================================================================
# 3. Preprocesamiento robusto
# ================================================================

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, features_num),
        ("cat", categorical_transformer, features_cat)
    ]
)

log("Preprocesamiento configurado correctamente.")

# ================================================================
# 4. Modelos
# ================================================================

modelos = {
    "Dummy": DummyClassifier(strategy="most_frequent"),
    "LogisticRegression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "RandomForest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),
    "XGBoost": XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.7,
        scale_pos_weight=3,   # importante por desbalance
        eval_metric="logloss",
        random_state=42
    )
}

log(f"Modelos configurados: {list(modelos.keys())}")

# ================================================================
# 5. Validación cruzada 5-fold
# ================================================================

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scoring = {
    "f1": "f1",
    "recall": "recall",
    "precision": "precision",
    "roc_auc": "roc_auc"
}

log("Iniciando validación cruzada 5-fold...")

resultados = []

for nombre, modelo in modelos.items():
    log(f"\nEntrenando modelo: {nombre}")

    clf = Pipeline(steps=[
        ("preprocess", preprocess),
        ("model", modelo)
    ])

    try:
        scores = cross_validate(
            clf,
            X, y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1
        )

        res = {
            "modelo": nombre,
            "f1": scores["test_f1"].mean(),
            "recall": scores["test_recall"].mean(),
            "precision": scores["test_precision"].mean(),
            "roc_auc": scores["test_roc_auc"].mean()
        }

        resultados.append(res)

        log(f"Resultados {nombre}: {res}")

    except Exception as e:
        log(f"ERROR en modelo {nombre}: {e}")
        continue

df_res = pd.DataFrame(resultados)

TABLA_OUT = "reports/tablas/resultados_modelos_parcial.csv"
df_res.to_csv(TABLA_OUT, index=False)

log(f"Tabla de resultados guardada en: {TABLA_OUT}")
log("=== FIN DEL EXPERIMENTO (PARCIAL) ===")
