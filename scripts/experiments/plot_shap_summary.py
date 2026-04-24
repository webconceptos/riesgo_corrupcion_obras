"""
Script: plot_shap_summary.py
Autor: Fernando García - Hilario Aradiel
Objetivo: Visualizar importancia global de características mediante SHAP
"""

import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

MODEL_PATH = Path("models/pipeline.pkl")
DATA_PATH = Path("data/processed/dataset_integrado.parquet")
OUT_FIG = Path("reports/figures/sem6_shap_summary.png")
OUT_FIG.parent.mkdir(parents=True, exist_ok=True)

print("=== Cargando modelo y datos ===")
pipe = joblib.load(MODEL_PATH)
df = pd.read_parquet(DATA_PATH)
X = df.drop(columns=["y_riesgo"])

# Tomamos el modelo interno del pipeline
model = pipe.named_steps["clf"]
prep = pipe.named_steps["prep"]
X_transformed = prep.transform(X)

explainer = shap.Explainer(model)
shap_values = explainer(X_transformed)

print("=== Generando gráfico SHAP global ===")
plt.title("Importancia global de variables (SHAP Summary)")
shap.summary_plot(shap_values, X_transformed, show=False)
plt.savefig(OUT_FIG, bbox_inches="tight", dpi=300)
plt.show()
print(f"✅ Gráfico guardado en: {OUT_FIG}")
