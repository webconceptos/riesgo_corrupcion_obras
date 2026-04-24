"""
02_run_inference_model_actual.py
--------------------------------
Script del Sprint 4 para evaluar el MODELO ACTUAL optimizado.

Flujo:
1. Cargar dataset de evaluación.
2. Preprocesamiento vía utils_sprint4.preprocess_features().
3. Cargar modelo final (RandomForest, XGBoost, o el que hayas elegido).
4. Realizar inferencia.
5. Calcular métricas completas.
6. Guardar resultados en la carpeta Sprint 4.
7. Registrar logs formales en models/sprint4/logs/.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from utils_sprint4 import (
    load_dataset,
    load_sklearn_model,
    save_metrics_csv,
    setup_logger,
    preprocess_features,
)


# =============================================================
# Función auxiliar para métricas
# =============================================================
def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray | None = None,
) -> Dict[str, Any]:
    """
    Calcula métricas estándar de clasificación.
    """
    metrics: Dict[str, Any] = {}

    metrics["accuracy"] = accuracy_score(y_true, y_pred)
    metrics["precision_macro"] = precision_score(
        y_true, y_pred, average="macro", zero_division=0
    )
    metrics["recall_macro"] = recall_score(
        y_true, y_pred, average="macro", zero_division=0
    )
    metrics["f1_macro"] = f1_score(
        y_true, y_pred, average="macro", zero_division=0
    )

    if y_proba is not None:
        try:
            metrics["roc_auc"] = roc_auc_score(y_true, y_proba)
        except Exception:
            metrics["roc_auc"] = float("nan")

    return metrics


# =============================================================
# MAIN
# =============================================================
def main(args: argparse.Namespace) -> None:
    # --------------------------------------
    # 1. Logger
    # --------------------------------------
    logger = setup_logger(args.log_path)
    logger.info("=== Evaluación MODELO ACTUAL - Sprint 4 ===")

    # --------------------------------------
    # 2. Cargar dataset
    # --------------------------------------
    data_path = Path(args.data)
    logger.info(f"Cargando dataset desde: {data_path}")
    df = load_dataset(data_path)

    if args.target_column not in df.columns:
        raise ValueError(
            f"La columna objetivo '{args.target_column}' no existe en el dataset."
        )

    y = df[args.target_column]
    X = df.drop(columns=[args.target_column])

    logger.info(f"Dataset shape: {df.shape}, columnas: {len(df.columns)}")

    # --------------------------------------
    # 3. Preprocesamiento
    # --------------------------------------
    logger.info("Aplicando preprocesamiento (utils_sprint4.preprocess_features)…")
    X_proc = preprocess_features(X)

    # --------------------------------------
    # 4. Cargar modelo actual
    # --------------------------------------
    model_path = Path(args.model_path)
    logger.info(f"Cargando modelo actual desde: {model_path}")
    model = load_sklearn_model(model_path)

    # --------------------------------------
    # 5. Inferencia
    # --------------------------------------
    logger.info("Ejecutando inferencia con el modelo actual…")
    y_pred = model.predict(X_proc)

    # Probabilidades
    y_proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(X_proc)
            if proba.shape[1] == 2:
                y_proba = proba[:, 1]
        except Exception as e:
            logger.warning(f"No se pudo obtener predict_proba: {e}")

    # --------------------------------------
    # 6. Métricas
    # --------------------------------------
    logger.info("Calculando métricas…")
    metrics = compute_classification_metrics(
        y_true=y.values,
        y_pred=y_pred,
        y_proba=y_proba,
    )
    logger.info(f"Métricas modelo actual: {metrics}")

    # --------------------------------------
    # 7. Guardar métricas y predicciones
    # --------------------------------------
    metrics_out = Path(args.metrics_out)
    preds_out = Path(args.predictions_out)

    # Guardar métricas
    logger.info(f"Guardando métricas en: {metrics_out}")
    save_metrics_csv(metrics, metrics_out)

    # Guardar predicciones
    logger.info(f"Guardando predicciones en: {preds_out}")
    preds_df = pd.DataFrame({"y_true": y.values, "y_pred": y_pred})
    if y_proba is not None:
        preds_df["y_proba"] = y_proba

    preds_out.parent.mkdir(parents=True, exist_ok=True)
    preds_df.to_csv(preds_out, index=False)

    logger.info("=== Evaluación del modelo actual completada correctamente ===")


# =============================================================
# CLI
# =============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluación del MODELO ACTUAL (Sprint 4)."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="CSV de evaluación.",
    )
    parser.add_argument(
        "--target-column",
        required=True,
        help="Nombre de la columna objetivo.",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Ruta al modelo actual: models/sprint4/modelos/modelo_actual.pkl",
    )
    parser.add_argument(
        "--metrics-out",
        default="models/sprint4/resultados/metrics_modelo_actual.csv",
        help="Ruta donde se guardarán las métricas.",
    )
    parser.add_argument(
        "--predictions-out",
        default="models/sprint4/resultados/predicciones_modelo_actual.csv",
        help="Ruta donde se guardarán las predicciones.",
    )
    parser.add_argument(
        "--log-path",
        default="models/sprint4/logs/inference_modelo_actual.log",
        help="Ruta del archivo de log.",
    )

    main(parser.parse_args())

