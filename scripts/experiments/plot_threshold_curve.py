"""
Script: plot_threshold_curve.py
Autor: Fernando García - Hilario Aradiel
Objetivo: Analizar el trade-off entre Precisión y Recall según el umbral.
"""

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from pathlib import Path

MODEL_PATH = Path("models/pipeline.pkl")
DATA_PATH = Path("data/processed/dataset_integrado.parquet")
OUT_FIG = Path("reports/figures/sem6_threshold_curve.png")

print("=== Curva Precisión–Recall vs Umbral ===")
pipe = joblib.load(MODEL_PATH)
df = pd.read_parquet(DATA_PATH)

X = df.drop(columns=["y_riesgo"])
y = df["y_riesgo"]

probs = pipe.predict_proba(X)[:, 1]
precision, recall, thresholds = precision_recall_curve(y, probs)
thresholds = np.append(thresholds, 1.0)

plt.figure(figsize=(8,6))
plt.plot(thresholds, precision, label="Precisión")
plt.plot(thresholds, recall, label="Recall")
plt.title("Curva Precisión–Recall según Umbral")
plt.xlabel("Umbral de decisión")
plt.ylabel("Métrica")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
plt.show()

print(f"✅ Figura guardada en: {OUT_FIG}")
