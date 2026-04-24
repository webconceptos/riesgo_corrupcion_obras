"""
Detecta posibles sesgos en las predicciones del modelo.
"""
import pandas as pd, joblib
from sklearn.metrics import f1_score
from pathlib import Path

pipe = joblib.load("models/pipeline.pkl")
df = pd.read_parquet("data/processed/dataset_integrado.parquet")
X, y = df.drop(columns=["y_riesgo"]), df["y_riesgo"]

# Simular variable sensible (ej. Región, Entidad)
if "REGION" in X.columns:
    groups = X["REGION"].unique()
    print("Sesgo por Región:")
    for g in groups:
        mask = X["REGION"] == g
        y_pred = pipe.predict(X[mask])
        print(f"{g:<20s} F1={f1_score(y[mask], y_pred):.3f}  N={mask.sum()}")
