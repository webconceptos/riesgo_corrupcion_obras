"""
Script: 01_run_inference_baseline.py
Genera las métricas del modelo baseline para Sprint 4.
"""

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.dummy import DummyClassifier
from pathlib import Path

DATASET_PATH = Path("models/sprint4/dataset_preparado.parquet")
OUTPUT_DIR = Path("models/sprint4/resultados")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Cargando dataset...")
df = pd.read_parquet(DATASET_PATH)

TARGET = "riesgo_corrupcion"
X = df.drop(columns=[TARGET])
y = df[TARGET]

print("Entrenando baseline (DummyClassifier)...")
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X, y)

pred = baseline.predict(X)
proba = baseline.predict_proba(X)[:, 1]

print("Calculando métricas...")
metrics = {
    "accuracy": accuracy_score(y, pred),
    "precision_macro": precision_score(y, pred, average="macro", zero_division=0),
    "recall_macro": recall_score(y, pred, average="macro", zero_division=0),
    "f1_macro": f1_score(y, pred, average="macro", zero_division=0),
    "roc_auc": roc_auc_score(y, proba)
}

df_out = pd.DataFrame([metrics])

output_file = OUTPUT_DIR / "metrics_baseline.csv"
df_out.to_csv(output_file, index=False)

print(f"✔ metrics_baseline.csv generado en {output_file}")
