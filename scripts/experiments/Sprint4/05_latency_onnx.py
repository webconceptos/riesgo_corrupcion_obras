"""
05_latency_onnx.py
------------------
Script del Sprint 4 para medir LATENCIA usando ONNX Runtime.

Flujo:
1. Cargar dataset de evaluación.
2. Preprocesar features (utils_sprint4.preprocess_features).
3. Cargar modelo ONNX (onnxruntime).
4. Ejecutar inferencia repetida N veces.
5. Obtener estadísticas de latencia:
   - p50, p90, p95, p99, mean, std
6. Guardar métricas + logs.

Este script demuestra cómo un modelo sklearn optimizado en ONNX
tiene una latencia significativamente más baja que en CPU puro.

"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import onnxruntime as ort

from utils_sprint4 import (
    load_dataset,
    preprocess_features,
    time_function,
    latency_stats,
    save_metrics_csv,
    setup_logger,
)


def main(args: argparse.Namespace) -> None:
    # -------------------------------------------------------------
    # 1. Logger
    # -------------------------------------------------------------
    logger = setup_logger(args.log_path)
    logger.info("=== Medición de Latencia en ONNX - Sprint 4 ===")

    # -------------------------------------------------------------
    # 2. Cargar dataset
    # -------------------------------------------------------------
    logger.info(f"Cargando dataset: {args.data}")
    df = load_dataset(args.data)

    if args.target_column not in df.columns:
        raise ValueError(f"Columna objetivo '{args.target_column}' no existe.")

    # Separar X
    X = df.drop(columns=[args.target_column])
    logger.info(f"Dataset shape: {df.shape}")

    # -------------------------------------------------------------
    # 3. Preprocesamiento
    # -------------------------------------------------------------
    logger.info("Preprocesando features…")
    X_proc = preprocess_features(X)
    X_np = X_proc.to_numpy(dtype=np.float32)
    logger.info(f"Shape final features: {X_np.shape}")

    # -------------------------------------------------------------
    # 4. Cargar modelo ONNX
    # -------------------------------------------------------------
    onnx_path = Path(args.model_path)
    logger.info(f"Cargando modelo ONNX desde: {onnx_path}")

    session = ort.InferenceSession(
        onnx_path.as_posix(),
        providers=["CPUExecutionProvider"]
    )

    input_name = session.get_inputs()[0].name
    logger.info(f"ONNX Input name: {input_name}")

    # -------------------------------------------------------------
    # 5. Función de inferencia
    # -------------------------------------------------------------
    def infer():
        """Función simple para benchmark de ONNX."""
        _ = session.run(None, {input_name: X_np})

    # -------------------------------------------------------------
    # 6. Ejecutar iteraciones
    # -------------------------------------------------------------
    logger.info(f"Ejecutando {args.n_runs} iteraciones ONNX…")

    lat_list, total_time = time_function(
        infer,
        n_runs=args.n_runs,
    )

    logger.info(f"Tiempo total ejecutado: {total_time:.4f} s")

    # -------------------------------------------------------------
    # 7. Estadísticas
    # -------------------------------------------------------------
    stats = latency_stats(lat_list)
    stats["total_time_s"] = float(total_time)
    stats["n_runs"] = int(args.n_runs)

    logger.info(f"Estadísticas ONNX: {stats}")

    # -------------------------------------------------------------
    # 8. Guardado de métricas
    # -------------------------------------------------------------
    out_csv = Path(args.out_csv)
    save_metrics_csv(stats, out_csv)
    logger.info(f"Métricas guardadas en: {out_csv}")

    logger.info("=== Latencia ONNX completada ===")


# ==========================================================
# CLI
# ==========================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mide latencia de inferencia usando ONNX Runtime."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="CSV del dataset de evaluación.",
    )
    parser.add_argument(
        "--target-column",
        required=True,
        help="Nombre de la columna objetivo.",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Ruta al archivo .onnx (convertido previamente).",
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=50,
        help="Número de iteraciones para medir latencia.",
    )
    parser.add_argument(
        "--out-csv",
        default="models/sprint4/resultados/latencia_onnx.csv",
        help="Archivo donde se guardarán las métricas de latencia.",
    )
    parser.add_argument(
        "--log-path",
        default="models/sprint4/logs/latency_onnx.log",
        help="Archivo de log.",
    )

    main(parser.parse_args())

