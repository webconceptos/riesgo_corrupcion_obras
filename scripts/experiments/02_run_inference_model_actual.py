"""
Script: 02_run_inference_model_actual.py
Calcula métricas del modelo final optimizado del Sprint 4.
"""

import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from pathlib import Path

MODEL_PATH = Path("models/sprint4/modelo_final_RandomForest.pkl")
DATASET_PATH = Path("models/sprint4/dataset_preparado.parquet")
OUTPUT_DIR = Path("models/sprint4/resultados")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Cargando modelo final...")
model = joblib.load(MODEL_PATH)

print("Cargando dataset...")
df = pd.read_parquet(DATASET_PATH)

TARGET = "riesgo_corrupcion"
X = df.drop(columns=[TARGET])
y = df[TARGET]

print("Generando predicciones...")
pred = model.predict(X)
proba = model.predict_proba(X)[:, 1]

print("Calculando métricas...")
metrics = {
    "accuracy": accuracy_score(y, pred),
    "precision_macro": precision_score(y, pred, average="macro", zero_division=0),
    "recall_macro": recall_score(y, pred, average="macro", zero_division=0),
    "f1_macro": f1_score(y, pred, average="macro", zero_division=0),
    "roc_auc": roc_auc_score(y, proba)
}

df_out = pd.DataFrame([metrics])

output_file = OUTPUT_DIR / "metrics_modelo_actual.csv"
df_out.to_csv(output_file, index=False)

print(f"✔ metrics_modelo_actual.csv generado en {output_file}")
