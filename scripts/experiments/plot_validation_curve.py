"""
Script: plot_validation_curve.py
Autor: Fernando García - Hilario Aradiel
Objetivo: Visualizar el efecto del número de árboles (n_estimators) en el F1-score.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import validation_curve
from sklearn.metrics import make_scorer, f1_score
from pathlib import Path

DATA_PATH = Path("data/processed/dataset_integrado.parquet")
OUT_FIG = Path("reports/figures/sem6_validation_curve.png")

df = pd.read_parquet(DATA_PATH)
X = df.drop(columns=["y_riesgo"])
y = df["y_riesgo"]

print("=== Generando curva de validación (n_estimators) ===")
param_range = [50, 100, 200, 400, 600]
train_scores, test_scores = validation_curve(
    XGBClassifier(
        learning_rate=0.1, max_depth=6, subsample=0.9,
        colsample_bytree=0.9, reg_lambda=1.0, eval_metric="logloss", tree_method="hist"
    ),
    X, y,
    param_name="n_estimators",
    param_range=param_range,
    cv=5,
    scoring=make_scorer(f1_score),
    n_jobs=-1
)

plt.figure(figsize=(8,6))
plt.plot(param_range, np.mean(train_scores, axis=1), "o--", label="Entrenamiento")
plt.plot(param_range, np.mean(test_scores, axis=1), "o-", label="Validación")
plt.xlabel("n_estimators")
plt.ylabel("F1-score")
plt.title("Curva de Validación del Modelo XGBoost")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
plt.show()

print(f"✅ Figura guardada en: {OUT_FIG}")
