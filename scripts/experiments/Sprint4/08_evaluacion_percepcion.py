"""
08_evaluacion_percepcion.py
---------------------------
Script para evaluar percepción de usuarios sobre el modelo.

Este script forma parte del Sprint 4 y permite medir:
- Claridad percibida de las predicciones
- Confianza del usuario en el sistema
- Utilidad percibida
- Satisfacción general
- Comentarios cualitativos

Formato esperado del CSV de entrada (ejemplo):

user_id, claridad, confianza, utilidad, satisfaccion, comentario
1, 4, 5, 5, 4, "Me pareció claro el resultado."
2, 3, 4, 4, 3, "Puede mejorar."
...

Todas las métricas se consolidan en un archivo CSV y JSON para el informe.

"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from utils_sprint4 import (
    setup_logger,
    save_json,
    save_metrics_csv,
)


def validate_columns(df: pd.DataFrame, cols: list):
    """Valida que el dataset tenga las columnas requeridas."""
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {missing}")


def compute_perception_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas sobre percepción de usuarios.
    Valores esperados: escala Likert 1–5
    """
    metrics = {}

    likert_cols = ["claridad", "confianza", "utilidad", "satisfaccion"]

    for col in likert_cols:
        metrics[f"{col}_promedio"] = float(df[col].mean())
        metrics[f"{col}_mediana"] = float(df[col].median())
        metrics[f"{col}_std"] = float(df[col].std())

    # Métrica global
    global_score = df[likert_cols].mean(axis=1).mean()
    metrics["score_global"] = float(global_score)

    return metrics


def save_comments(df: pd.DataFrame, out_path: str):
    """
    Guarda comentarios cualitativos en un TXT para análisis manual.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    comments = df["comentario"].dropna().tolist()

    with open(out_path, "w", encoding="utf-8") as f:
        for c in comments:
            f.write(f"- {c}\n")


def main(args):
    # ---------------------------------------------------------
    # 1. Logger
    # ---------------------------------------------------------
    logger = setup_logger(args.log_path)
    logger.info("=== Evaluación de Percepción de Usuarios - Sprint 4 ===")

    # ---------------------------------------------------------
    # 2. Cargar dataset
    # ---------------------------------------------------------
    df = pd.read_csv(args.data)
    logger.info(f"Dataset de percepción cargado con {len(df)} filas.")

    required_cols = ["claridad", "confianza", "utilidad", "satisfaccion", "comentario"]
    validate_columns(df, required_cols)

    # ---------------------------------------------------------
    # 3. Calcular métricas
    # ---------------------------------------------------------
    metrics = compute_perception_metrics(df)
    logger.info(f"Métricas de percepción: {metrics}")

    # ---------------------------------------------------------
    # 4. Guardar métricas en CSV y JSON
    # ---------------------------------------------------------
    save_metrics_csv(metrics, args.out_csv)
    save_json(metrics, args.out_json)

    logger.info(f"Métricas guardadas en: {args.out_csv} y {args.out_json}")

    # ---------------------------------------------------------
    # 5. Guardar comentarios cualitativos
    # ---------------------------------------------------------
    save_comments(df, args.out_comments)
    logger.info(f"Comentarios guardados en: {args.out_comments}")

    logger.info("=== Evaluación de percepción completada ===")


# ======================================================================
# CLI
# ======================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evalúa la percepción de usuarios sobre el modelo."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="CSV con resultados de encuestas."
    )
    parser.add_argument(
        "--out-csv",
        default="models/sprint4/resultados/perception_usuarios.csv",
        help="Archivo CSV donde se guardarán las métricas cuantitativas."
    )
    parser.add_argument(
        "--out-json",
        default="models/sprint4/resultados/perception_usuarios.json",
        help="Archivo JSON con el resumen de métricas."
    )
    parser.add_argument(
        "--out-comments",
        default="models/sprint4/resultados/perception_comentarios.txt",
        help="Archivo TXT donde se guardarán los comentarios textuales."
    )
    parser.add_argument(
        "--log-path",
        default="models/sprint4/logs/perception.log",
        help="Log de ejecución."
    )

    main(parser.parse_args())

