# -*- coding: utf-8 -*-
"""
Script maestro: opt_master.py
Autores: Fernando García - Hilario Aradiel
Proyecto: Sistema de Detección de Riesgos de Corrupción en Obras Públicas
Objetivo: Ejecutar y comparar optimización Random Search y Bayesian Optimization,
          generando logs, gráficos y resultados consolidados.
"""

import sys, io, os, json
from pathlib import Path
from datetime import datetime

# === Forzar codificación UTF-8 (Windows compatible) ===
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# === Configuración de carpeta y log ===
OUT_DIR = Path("reports/tuning")
OUT_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = OUT_DIR / f"opt_master_run_{timestamp}.log"

# Crear log inicial
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write(f"=== LOG DE EJECUCIÓN OPT_MASTER ({timestamp}) ===\n")

def log(msg, console=True):
    """Imprime en consola y guarda en log"""
    if console:
        print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log(f"📘 Log iniciado: {LOG_FILE}\n")

# === Imports principales ===
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score, make_scorer
from xgboost import XGBClassifier
from bayes_opt import BayesianOptimization
import matplotlib.pyplot as plt
import seaborn as sns

# === [1] CARGA DE DATOS ===
log("=== [1] CARGA DE DATOS ===")
df = pd.read_parquet("data/processed/dataset_integrado.parquet")
X = df.drop(columns=["y_riesgo"])
y = df["y_riesgo"]

# Limpieza y preprocesamiento robusto
X = X.fillna("Desconocido")
for col in X.columns:
    if X[col].dtype == "object" or X[col].dtype.name == "category":
        X[col] = X[col].astype("category").cat.codes
    elif X[col].dtype == "bool":
        X[col] = X[col].astype(int)

log(f"✅ Dataset preparado: {X.shape[0]} filas, {X.shape[1]} columnas")
log(f"   Tipos de datos: {X.dtypes.value_counts().to_dict()}\n")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scorer = make_scorer(f1_score)

# === [2] RANDOM SEARCH ===
log("=== [2] RANDOM SEARCH ===")
from itertools import product
param_grid = {
    "n_estimators": [100, 200, 400],
    "max_depth": [4, 6, 8],
    "learning_rate": [0.05, 0.1, 0.2],
    "subsample": [0.8, 0.9],
    "colsample_bytree": [0.8, 0.9],
}

results_random = []
for i, (n, m, lr, ss, cs) in enumerate(product(*param_grid.values()), 1):
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
        results_random.append(params)
        log(f"[R{i:02d}] {params} → F1={f1:.3f}")
    except Exception as e:
        log(f"⚠️ Error con configuración {params}: {e}")

df_random = pd.DataFrame(results_random).sort_values("f1_score", ascending=False)
df_random.to_csv(OUT_DIR / "random_search_results.csv", index=False)
log(f"✅ Random Search completado ({len(df_random)} combinaciones)\n")

# === [3] BAYESIAN OPTIMIZATION ===
log("=== [3] BAYESIAN OPTIMIZATION ===")

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
    return cross_val_score(model, X, y, cv=cv, scoring=scorer, n_jobs=-1).mean()

pbounds = {
    "n_estimators": (100, 500),
    "max_depth": (3, 9),
    "learning_rate": (0.01, 0.3),
    "subsample": (0.7, 1.0),
    "colsample_bytree": (0.7, 1.0),
}

optimizer = BayesianOptimization(f=xgb_cv, pbounds=pbounds, random_state=42)
optimizer.maximize(init_points=5, n_iter=15)

df_bayes = pd.DataFrame(optimizer.res)
df_bayes.to_csv(OUT_DIR / "bayes_opt_results.csv", index=False)
log(f"✅ Bayesian Optimization completado ({len(df_bayes)} iteraciones)\n")

# === [4] COMPARACIÓN Y TOP-K ===
log("=== [4] COMPARACIÓN Y TOP-K ===")
df_random["method"] = "random"
df_bayes["method"] = "bayes"

# Unificar resultados
common_cols = list(set(df_random.columns) & set(df_bayes.columns))
df_all = pd.concat([df_random, df_bayes[common_cols]], ignore_index=True)
topk = df_all.sort_values("f1_score", ascending=False).head(10)
topk.to_csv(OUT_DIR / "topk_summary.csv", index=False)
log("🏆 Top-10 combinaciones guardadas en reports/tuning/topk_summary.csv\n")

# === [5] GRAFICO DE EVOLUCIÓN ===
log("=== [5] GRAFICO DE EVOLUCIÓN ===")
plt.figure(figsize=(8,5))
sns.lineplot(x=range(len(df_random)), y=df_random["f1_score"], label="Random Search")
if "target" in df_bayes.columns:
    sns.lineplot(x=range(len(df_bayes)), y=df_bayes["target"], label="Bayes Opt")
plt.xlabel("Iteración")
plt.ylabel("F1-score promedio")
plt.title("Evolución de la optimización de hiperparámetros")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT_DIR / "evolution_comparison.png", dpi=300)
plt.close()
log("✅ Gráfico guardado en reports/tuning/evolution_comparison.png\n")

# === [6] EXPORTACIÓN DE CONFIGURACIONES GANADORAS ===
winner_random = df_random.iloc[0].to_dict()
winner_bayes = optimizer.max["params"]
winner_bayes["f1_score"] = optimizer.max["target"]

with open(OUT_DIR / "config_winner_random.json", "w", encoding="utf-8") as f:
    json.dump(winner_random, f, indent=2, ensure_ascii=False)
with open(OUT_DIR / "config_winner_bayes.json", "w", encoding="utf-8") as f:
    json.dump(winner_bayes, f, indent=2, ensure_ascii=False)

log("✅ Configuraciones ganadoras exportadas")
log("🏁 Pipeline de optimización completado con éxito.\n")
log(f"📜 Log completo en: {LOG_FILE}")
