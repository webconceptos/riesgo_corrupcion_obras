"""
Script: plot_learning_curves.py
Objetivo: visualizar el rendimiento del modelo con distintas cantidades de datos
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.metrics import make_scorer, f1_score
import numpy as np
from pathlib import Path

MODEL_PATH = Path("models/pipeline.pkl")
DATA_PATH = Path("data/processed/dataset_integrado.parquet")
OUT_FIG = Path("reports/figures/sem6_learning_curve.png")

pipe = joblib.load(MODEL_PATH)
df = pd.read_parquet(DATA_PATH)
X = df.drop(columns=["y_riesgo"])
y = df["y_riesgo"]

print("=== Generando curva de aprendizaje ===")
train_sizes, train_scores, test_scores = learning_curve(
    pipe, X, y, cv=5, scoring=make_scorer(f1_score), n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10), random_state=42
)

train_mean = np.mean(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)

plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_mean, "o-", label="Entrenamiento")
plt.plot(train_sizes, test_mean, "o-", label="Validación")
plt.xlabel("Tamaño del conjunto de entrenamiento")
plt.ylabel("F1-score")
plt.title("Curva de Aprendizaje del Modelo")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
plt.show()

print(f"✅ Curva de aprendizaje guardada en: {OUT_FIG}")
