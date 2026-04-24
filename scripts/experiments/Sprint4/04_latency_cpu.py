"""
04_latency_cpu.py
-----------------
Script del Sprint 4 para medir latencia de inferencia en CPU
usando un modelo sklearn (baseline o modelo actual).

Flujo:
1. Cargar dataset de evaluación.
2. Preprocesar features (placeholder en utils).
3. Cargar modelo sklearn (.pkl).
4. Ejecutar inferencia repetida N veces.
5. Calcular estadísticas de latencia:
   - mean, std, min, max
   - p50, p90, p95, p99
6. Guardar resultados en CSV y log.

Este archivo es crítico para el Sprint 4 porque demuestra el
cumplimiento de SLOs técnicos (Service Level Objectives).

"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from utils_sprint4 import (
    load_dataset,
    load_sklearn_model,
    preprocess_features,
    time_function,
    latency_stats,
    save_metrics_csv,
    setup_logger,
)


def main(args: argparse.Namespace) -> None:

    # -------------------------------------------------------------
    # 1. Crear logger
    # -------------------------------------------------------------
    logger = setup_logger(args.log_path)
    logger.info("=== Medición de Latencia en CPU - Sprint 4 ===")

    # -------------------------------------------------------------
    # 2. Cargar dataset
    # -------------------------------------------------------------
    data_path = Path(args.data)
    logger.info(f"Cargando dataset: {data_path}")
    df = load_dataset(data_path)

    if args.target_column not in df.columns:
        raise ValueError(f"La columna objetivo '{args.target_column}' no existe.")

    # Separar X
    X = df.drop(columns=[args.target_column])
    logger.info(f"Dataset shape: {df.shape}")

    # -------------------------------------------------------------
    # 3. Preprocesar features
    # -------------------------------------------------------------
    logger.info("Preprocesando features…")
    X_proc = preprocess_features(X)
    logger.info(f"Shape después del preprocesamiento: {X_proc.shape}")

    # Convertir a numpy para acelerar
    X_np = X_proc.to_numpy(dtype=np.float32)

    # -------------------------------------------------------------
    # 4. Cargar modelo
    # -------------------------------------------------------------
    logger.info(f"Cargando modelo: {args.model_path}")
    model = load_sklearn_model(args.model_path)

    # -------------------------------------------------------------
    # 5. Crear función de inferencia
    # -------------------------------------------------------------
    def infer():
        """Función simple para medir latencia por inferencia"""
        _ = model.predict(X_np)

    # -------------------------------------------------------------
    # 6. Ejecutar N iteraciones para medir latencia
    # -------------------------------------------------------------
    logger.info(f"Ejecutando {args.n_runs} iteraciones…")

    lat_list, total_time = time_function(
        infer,
        n_runs=args.n_runs,
    )

    logger.info(f"Tiempo total ejecutado: {total_time:.4f} s")

    # -------------------------------------------------------------
    # 7. Estadísticas de latencia
    # -------------------------------------------------------------
    stats = latency_stats(lat_list)
    stats["total_time_s"] = float(total_time)
    stats["n_runs"] = int(args.n_runs)

    logger.info(f"Estadísticas de latencia CPU: {stats}")

    # -------------------------------------------------------------
    # 8. Guardar métricas
    # -------------------------------------------------------------
    out_csv = Path(args.out_csv)
    save_metrics_csv(stats, out_csv)
    logger.info(f"Métricas guardadas en: {out_csv}")

    logger.info("=== Latencia CPU completada ===")


# ==========================================================
# CLI
# ==========================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mide latencia de inferencia de un modelo sklearn en CPU."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="Dataset de evaluación (CSV).",
    )
    parser.add_argument(
        "--target-column",
        required=True,
        help="Nombre de la columna objetivo.",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Ruta al modelo .pkl a evaluar.",
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=50,
        help="Número de ejecuciones para medir latencia.",
    )
    parser.add_argument(
        "--out-csv",
        default="models/sprint4/resultados/latencia_cpu.csv",
        help="Archivo donde se guardarán las métricas de latencia.",
    )
    parser.add_argument(
        "--log-path",
        default="models/sprint4/logs/latency_cpu.log",
        help="Archivo de log.",
    )

    main(parser.parse_args())
