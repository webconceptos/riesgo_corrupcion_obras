"""
Script: plot_calibration.py
Objetivo: evaluar calibración de probabilidades del modelo final
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import train_test_split
from pathlib import Path

MODEL_PATH = Path("models/pipeline.pkl")
DATA_PATH = Path("data/processed/dataset_integrado.parquet")
OUT_FIG = Path("reports/figures/sem6_calibration_curve.png")

print("=== Calibración del modelo ===")
pipe = joblib.load(MODEL_PATH)
df = pd.read_parquet(DATA_PATH)
X = df.drop(columns=["y_riesgo"])
y = df["y_riesgo"]

# División hold-out
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
probs = pipe.predict_proba(Xte)[:, 1]

# Calibración
prob_true, prob_pred = calibration_curve(yte, probs, n_bins=10)
brier = brier_score_loss(yte, probs)

plt.figure(figsize=(6, 6))
plt.plot(prob_pred, prob_true, "s-", label="Modelo")
plt.plot([0, 1], [0, 1], "k--", label="Perfectamente calibrado")
plt.xlabel("Probabilidad predicha")
plt.ylabel("Probabilidad observada")
plt.title(f"Curva de calibración (Brier={brier:.3f})")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
plt.show()

print(f"✅ Curva de calibración guardada en: {OUT_FIG}")
