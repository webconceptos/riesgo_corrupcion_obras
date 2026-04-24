# -*- coding: utf-8 -*-
"""
Script: opt_bayes_opt.py
Autores: Fernando García - Hilario Aradiel
Objetivo: Optimización Bayesiana de hiperparámetros con early stopping
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import f1_score, make_scorer
from xgboost import XGBClassifier
from bayes_opt import BayesianOptimization
import json
from pathlib import Path

# === Configuración de salida ===
OUT_DIR = Path("reports/tuning")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "bayes_opt_results.csv"
CONFIG_WINNER = OUT_DIR / "config_winner_bayes.json"

# === Carga del dataset ===
df = pd.read_parquet("data/processed/dataset_integrado.parquet")
X = df.drop(columns=["y_riesgo"])
y = df["y_riesgo"]

# === Limpieza y preprocesamiento robusto ===
# 1. Reemplazar NaN o valores faltantes
X = X.fillna("Desconocido")

# 2. Convertir columnas object o mixtas a categorías numéricas
for col in X.columns:
    if X[col].dtype == "object" or X[col].dtype == "category":
        X[col] = X[col].astype("category").cat.codes
    elif X[col].dtype == "bool":
        X[col] = X[col].astype(int)

# 3. Verificación final
print(f"✅ Dataset preparado: {X.shape[0]} filas, {X.shape[1]} columnas")
print(f"   Tipos únicos: {X.dtypes.value_counts().to_dict()}")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scorer = make_scorer(f1_score)

# === Función objetivo para optimización ===
def xgb_cv(n_estimators, max_depth, learning_rate, subsample, colsample_bytree):
    n_estimators = int(n_estimators)
    max_depth = int(max_depth)
    model = XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        eval_metric="logloss",
        random_state=42,
        tree_method="hist",
        use_label_encoder=False,
        early_stopping_rounds=10
    )
    f1 = cross_val_score(model, X, y, cv=cv, scoring=scorer, n_jobs=-1).mean()
    return f1

# === Espacio de búsqueda ===
pbounds = {
    "n_estimators": (100, 500),
    "max_depth": (3, 9),
    "learning_rate": (0.01, 0.3),
    "subsample": (0.7, 1.0),
    "colsample_bytree": (0.7, 1.0),
}

optimizer = BayesianOptimization(f=xgb_cv, pbounds=pbounds, random_state=42)
print("\n=== 🤖 OPTIMIZACIÓN BAYESIANA ===")
optimizer.maximize(init_points=5, n_iter=15)

# === Guardado de resultados ===
pd.DataFrame(optimizer.res).to_csv(OUT_FILE, index=False)
winner = optimizer.max["params"]
winner["f1_score"] = optimizer.max["target"]

with open(CONFIG_WINNER, "w", encoding="utf-8") as f:
    json.dump(winner, f, indent=2, ensure_ascii=False)

print(f"\n✅ Resultados guardados en {OUT_FILE}")
print(f"🏆 Mejor configuración guardada en {CONFIG_WINNER}")
