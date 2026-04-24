"""
03_export_to_onnx.py
--------------------
Script del Sprint 4 para exportar un modelo sklearn a formato ONNX.

Flujo:
1. Cargar dataset de referencia para determinar el tamaño de entrada.
2. Cargar el modelo sklearn serializado (.pkl).
3. Aplicar preprocesamiento simple (placeholder) para tener matrix final.
4. Exportar a ONNX con onnxmltools.
5. Guardar:
    - modelo_onnx.onnx
    - log en models/sprint4/logs/

Uso típico:

python scripts/Sprint4/03_export_to_onnx.py ^
    --model-path models/sprint4/modelos/modelo_actual.pkl ^
    --data data/processed/dataset_modelado.csv ^
    --target-column riesgo_corrupcion
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import onnxmltools
from skl2onnx.common.data_types import FloatTensorType

from utils_sprint4 import (
    load_dataset,
    load_sklearn_model,
    preprocess_features,
    setup_logger,
)


def main(args: argparse.Namespace) -> None:
    # --------------------------------------------------------
    # 1. Logger
    # --------------------------------------------------------
    logger = setup_logger(args.log_path)
    logger.info("=== Exportación modelo ONNX - Sprint 4 ===")

    # --------------------------------------------------------
    # 2. Cargar dataset de referencia
    # --------------------------------------------------------
    logger.info(f"Cargando dataset de referencia: {args.data}")
    df = load_dataset(args.data)

    if args.target_column not in df.columns:
        raise ValueError(f"La columna objetivo '{args.target_column}' no existe.")

    # Separar X
    X = df.drop(columns=[args.target_column])
    logger.info(f"Dataset shape: {df.shape}")

    # Preprocesar (puedes reemplazar por pipeline real)
    logger.info("Aplicando preprocesamiento…")
    X_proc = preprocess_features(X)

    # Número de features finales
    n_features = X_proc.shape[1]
    logger.info(f"Número final de features: {n_features}")

    # --------------------------------------------------------
    # 3. Cargar modelo sklearn
    # --------------------------------------------------------
    logger.info(f"Cargando modelo desde: {args.model_path}")
    model = load_sklearn_model(args.model_path)

    # --------------------------------------------------------
    # 4. Crear entrada para ONNX
    # --------------------------------------------------------
    logger.info("Generando representación ONNX…")
    initial_type = [("input", FloatTensorType([None, n_features]))]

    try:
        onnx_model = onnxmltools.convert_sklearn(
            model,
            initial_types=initial_type,
            name="modelo_sprint4",
        )
    except Exception as e:
        logger.error(f"Error convirtiendo a ONNX: {e}")
        raise

    # --------------------------------------------------------
    # 5. Guardar el archivo ONNX
    # --------------------------------------------------------
    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Guardando modelo ONNX en: {out_path}")
    onnxmltools.utils.save_model(onnx_model, out_path.as_posix())

    logger.info("=== Exportación a ONNX completada exitosamente ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exporta un modelo sklearn a formato ONNX."
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Ruta al modelo sklearn .pkl (modelo_actual.pkl o baseline.pkl).",
    )
    parser.add_argument(
        "--data",
        required=True,
        help="Dataset de referencia para determinar el tamaño de entrada.",
    )
    parser.add_argument(
        "--target-column",
        required=True,
        help="Columna objetivo (target) que debe excluirse de X.",
    )
    parser.add_argument(
        "--out-path",
        default="models/sprint4/modelos/modelo_onnx.onnx",
        help="Ruta donde se guardará el modelo ONNX resultante.",
    )
    parser.add_argument(
        "--log-path",
        default="models/sprint4/logs/export_onnx.log",
        help="Archivo de log.",
    )

    main(parser.parse_args())

