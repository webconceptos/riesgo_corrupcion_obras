# -*- coding: utf-8 -*-
"""
Script: opt_random_search.py
Autores: Fernando García - Hilario Aradiel
Objetivo: Optimización de hiperparámetros vía Random Search con early stopping
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score, make_scorer
from xgboost import XGBClassifier
import itertools, json, os
from datetime import datetime
from pathlib import Path

# === Configuración de salida ===
OUT_DIR = Path("reports/tuning")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "random_search_results.csv"
CONFIG_WINNER = OUT_DIR / "config_winner_random.json"

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

# === Espacio de búsqueda ===
param_grid = {
    "n_estimators": [100, 200, 400],
    "max_depth": [4, 6, 8],
    "learning_rate": [0.05, 0.1, 0.2],
    "subsample": [0.8, 0.9],
    "colsample_bytree": [0.8, 0.9],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scorer = make_scorer(f1_score)

results = []
print("\n=== 🔍 RANDOM SEARCH DE HIPERPARÁMETROS ===")
for i, (n, m, lr, ss, cs) in enumerate(itertools.product(*param_grid.values())):
    params = dict(zip(param_grid.keys(), [n, m, lr, ss, cs]))
    model = XGBClassifier(
        random_state=42,
        eval_metric="logloss",
        tree_method="hist",
        early_stopping_rounds=10,
        use_label_encoder=False,
        **params
    )
    try:
        f1 = cross_val_score(model, X, y, cv=cv, scoring=scorer, n_jobs=-1).mean()
        params["f1_score"] = f1
        results.append(params)
        print(f"[{i+1:02d}] {params} → F1={f1:.3f}")
    except Exception as e:
        print(f"⚠️ Error con configuración {params}: {e}")

# === Guardado de resultados ===
res_df = pd.DataFrame(results).sort_values("f1_score", ascending=False)
res_df.to_csv(OUT_FILE, index=False)
winner = res_df.iloc[0].to_dict()

with open(CONFIG_WINNER, "w", encoding="utf-8") as f:
    json.dump(winner, f, indent=2, ensure_ascii=False)

print(f"\n✅ Resultados guardados en {OUT_FILE}")
print(f"🏆 Mejor configuración guardada en {CONFIG_WINNER}")
