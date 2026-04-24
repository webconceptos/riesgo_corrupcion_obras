"""
Script: plot_importance.py
Objetivo: generar el ranking de variables más influyentes del modelo XGBoost
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBClassifier
from pathlib import Path

# Paths
MODEL_PATH = Path("models/pipeline.pkl")
DATA_PATH = Path("data/processed/dataset_integrado.parquet")
OUT_FIG = Path("reports/figures/sem6_feature_importance.png")
OUT_FIG.parent.mkdir(parents=True, exist_ok=True)

print("=== Cargando modelo y datos ===")
pipe = joblib.load(MODEL_PATH)
df = pd.read_parquet(DATA_PATH)
X = df.drop(columns=["y_riesgo"])

# Extraer modelo XGB
model = pipe.named_steps["clf"]
if not isinstance(model, XGBClassifier):
    print("⚠️ El modelo no es XGBoost. Este script está optimizado para XGBClassifier.")
else:
    print("✅ Modelo XGBoost detectado.")

# Obtener nombres de variables tras el preprocesamiento
preproc = pipe.named_steps["prep"]
cat_features = preproc.transformers_[1][1].named_steps["ohe"].get_feature_names_out()
num_features = preproc.transformers_[0][2]
feature_names = np.concatenate([num_features, cat_features])

# Importancia
importance = model.feature_importances_
imp_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importance
}).sort_values("importance", ascending=False).head(20)

# Plot
plt.figure(figsize=(8, 6))
plt.barh(imp_df["feature"], imp_df["importance"])
plt.gca().invert_yaxis()
plt.title("Ranking de Importancia de Variables (Top 20)")
plt.xlabel("Importancia relativa")
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
plt.show()

print(f"✅ Gráfico guardado en: {OUT_FIG}")
