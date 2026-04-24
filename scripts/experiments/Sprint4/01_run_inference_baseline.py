"""
01_run_inference_baseline.py – VERSION PRO
Garantiza que SIEMPRE se generen métricas válidas.
Detecta errores silenciosos en preprocess_features o predict().
"""

import argparse
from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
)
from utils_sprint4 import (
    load_dataset, load_sklearn_model, save_metrics_csv,
    setup_logger, preprocess_features
)

def compute_metrics(y_true, y_pred, y_proba=None):
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0)
    }

    if y_proba is not None:
        try:
            metrics["roc_auc"] = roc_auc_score(y_true, y_proba)
        except Exception:
            metrics["roc_auc"] = np.nan

    return metrics


def main(args):

    logger = setup_logger(args.log_path)
    logger.info("=== Evaluación BASELINE (PRO) ===")

    # --------------------------------------------------------------
    # Validación dataset
    # --------------------------------------------------------------
    df = load_dataset(Path(args.data))

    if df.empty:
        raise ValueError("ERROR: El dataset cargado está VACÍO.")

    if args.target_column not in df.columns:
        raise ValueError(f"La columna objetivo '{args.target_column}' NO existe en dataset.")

    X = df.drop(columns=[args.target_column])
    y = df[args.target_column]

    if X.shape[1] == 0:
        raise ValueError("ERROR: El dataset NO tiene columnas de features.")

    logger.info(f"Dataset shape: {df.shape}")

    # --------------------------------------------------------------
    # Preprocesamiento
    # --------------------------------------------------------------
    logger.info("Preprocesando features...")

    X_proc = preprocess_features(X)

    if X_proc is None or len(X_proc) == 0:
        raise ValueError("ERROR: preprocess_features() devolvió un DataFrame vacío.")

    if X_proc.shape[1] == 0:
        raise ValueError("ERROR: preprocess_features() devolvió 0 columnas.")

    logger.info(f"Shape después de preprocesar: {X_proc.shape}")

    # --------------------------------------------------------------
    # Carga modelo baseline
    # --------------------------------------------------------------
    model = load_sklearn_model(Path(args.model_path))

    if not hasattr(model, "predict"):
        raise ValueError("El modelo cargado NO soporta .predict()")

    logger.info("Modelo baseline cargado correctamente.")

    # --------------------------------------------------------------
    # Inferencia
    # --------------------------------------------------------------
    logger.info("Ejecutando inferencia...")

    try:
        y_pred = model.predict(X_proc)
    except Exception as e:
        raise RuntimeError(f"ERROR al hacer predict(): {e}")

    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(X_proc)
            y_proba = proba[:, 1] if proba.shape[1] == 2 else None
        except Exception:
            y_proba = None
    else:
        y_proba = None

    # --------------------------------------------------------------
    # Métricas
    # --------------------------------------------------------------
    logger.info("Calculando métricas...")

    metrics = compute_metrics(y, y_pred, y_proba)

    logger.info(f"Métricas baseline: {metrics}")

    # Validación obligatorIa: NO permitir CSV vacío
    if not metrics:
        raise RuntimeError("ERROR: No se generaron métricas. CSV NO será guardado.")

    # --------------------------------------------------------------
    # Guardar métricas y predicciones
    # --------------------------------------------------------------
    metrics_out = Path(args.metrics_out)
    preds_out = Path(args.predictions_out)

    save_metrics_csv(metrics, metrics_out)

    preds_df = pd.DataFrame({"y_true": y, "y_pred": y_pred})
    if y_proba is not None:
        preds_df["y_proba"] = y_proba

    preds_out.parent.mkdir(parents=True, exist_ok=True)
    preds_df.to_csv(preds_out, index=False)

    logger.info("=== Evaluación baseline completada correctamente ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--target-column", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--metrics-out", default="models/sprint4/resultados/metrics_baseline.csv")
    parser.add_argument("--predictions-out", default="models/sprint4/resultados/predicciones_baseline.csv")
    parser.add_argument("--log-path", default="models/sprint4/logs/inference_baseline.log")
    main(parser.parse_args())
