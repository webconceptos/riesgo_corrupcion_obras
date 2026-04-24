"""
06_latency_tensorrt.py
----------------------
Script del Sprint 4 para medir LATENCIA de un modelo convertido a TensorRT.

Flujo:
1. Verificar disponibilidad de TensorRT + PyCUDA.
2. Cargar engine TensorRT (.engine).
3. Crear buffers de entrada/salida (GPU).
4. Ejecutar inferencia repetida N veces.
5. Calcular métricas de latencia:
   - mean, std, p50, p90, p95, p99
6. Guardar CSV + log en models/sprint4/*

Este archivo PERMITE evidenciar dominio profesional de inferencia optimizada en GPU.

"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Tuple, List, Dict

import numpy as np

from utils_sprint4 import (
    setup_logger,
    save_metrics_csv,
    latency_stats,
    time_function,
)

# Intentar importar TensorRT + PyCUDA
try:
    import tensorrt as trt          # type: ignore
    import pycuda.driver as cuda    # type: ignore
    import pycuda.autoinit          # noqa: F401
    TRT_AVAILABLE = True
except Exception:
    trt = None
    cuda = None
    TRT_AVAILABLE = False



# ============================================================================
# Utilidad: cargar TensorRT engine
# ============================================================================

def load_trt_engine(engine_path: Path, logger) -> Optional[trt.ICudaEngine]:
    """
    Carga un archivo .engine de TensorRT si TensorRT está instalado.
    """
    if not TRT_AVAILABLE:
        logger.error("TensorRT/PyCUDA no están instalados. No se puede ejecutar el benchmark.")
        return None

    if not engine_path.exists():
        logger.error(f"No existe el archivo TensorRT engine: {engine_path}")
        return None

    logger.info(f"Cargando TensorRT engine desde: {engine_path}")

    try:
        TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
        with open(engine_path, "rb") as f:
            runtime = trt.Runtime(TRT_LOGGER)
            engine = runtime.deserialize_cuda_engine(f.read())
        return engine
    except Exception as e:
        logger.error(f"Error cargando modelo TensorRT: {e}")
        return None



# ============================================================================
# TensorRT inferencia
# ============================================================================

def allocate_buffers(engine: trt.ICudaEngine, batch_size: int, n_features: int):
    """
    Crea buffers para entrada y salida en GPU.
    """
    input_size = batch_size * n_features
    output_size = batch_size * 1  # asumimos 1 salida, modificar si fuera multiclase

    host_input = np.random.randn(batch_size, n_features).astype(np.float32)
    host_output = np.zeros((batch_size, 1), dtype=np.float32)

    device_input = cuda.mem_alloc(host_input.nbytes)
    device_output = cuda.mem_alloc(host_output.nbytes)

    bindings = [int(device_input), int(device_output)]
    stream = cuda.Stream()

    return host_input, host_output, device_input, device_output, bindings, stream



def infer_trt(
    context: trt.IExecutionContext,
    host_input: np.ndarray,
    host_output: np.ndarray,
    device_input,
    device_output,
    bindings,
    stream,
):
    """
    Ejecuta una inferencia TensorRT: copia CPU->GPU, ejecuta, GPU->CPU.
    """
    cuda.memcpy_htod_async(device_input, host_input, stream)
    context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
    cuda.memcpy_dtoh_async(host_output, device_output, stream)
    stream.synchronize()



# ============================================================================
# MAIN
# ============================================================================

def main(args: argparse.Namespace) -> None:
    # Logger
    logger = setup_logger(args.log_path)
    logger.info("=== Medición de latencia TensorRT - Sprint 4 ===")

    # Verificación básica
    if not TRT_AVAILABLE:
        logger.error("TensorRT o PyCUDA NO están instalados. Benchmark cancelado.")
        stats = {"error": "TensorRT no disponible"}
        save_metrics_csv(stats, args.out_csv)
        return

    # Cargar engine
    engine_path = Path(args.engine_path)
    engine = load_trt_engine(engine_path, logger)

    if engine is None:
        logger.error("No fue posible cargar el engine TensorRT.")
        return

    # Crear contexto
    logger.info("Creando contexto de ejecución…")
    context = engine.create_execution_context()

    # Asumimos que el modelo recibe batch × features como entrada
    batch_size = args.batch_size
    n_features = args.n_features

    (
        host_input,
        host_output,
        device_input,
        device_output,
        bindings,
        stream
    ) = allocate_buffers(engine, batch_size, n_features)

    # Función de inferencia
    def infer():
        infer_trt(
            context,
            host_input,
            host_output,
            device_input,
            device_output,
            bindings,
            stream,
        )

    # Ejecutar benchmark
    logger.info(f"Ejecutando {args.n_runs} iteraciones TensorRT…")
    lat_list, total_time = time_function(infer, n_runs=args.n_runs)

    # Estadísticas
    stats = latency_stats(lat_list)
    stats["total_time_s"] = float(total_time)
    stats["n_runs"] = int(args.n_runs)

    logger.info(f"=== Estadísticas TensorRT ===\n{stats}")

    # Guardar
    save_metrics_csv(stats, args.out_csv)
    logger.info(f"Resultados guardados en: {args.out_csv}")

    logger.info("=== Benchmark TensorRT finalizado ===")



# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mide latencia de inferencia usando TensorRT (si está disponible)."
    )
    parser.add_argument(
        "--engine-path",
        required=True,
        help="Ruta al archivo TensorRT (.engine).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Tamaño de batch para inferencia.",
    )
    parser.add_argument(
        "--n-features",
        type=int,
        default=128,
        help="Número de features esperadas por el modelo.",
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=50,
        help="Número de iteraciones para benchmark.",
    )
    parser.add_argument(
        "--out-csv",
        default="models/sprint4/resultados/latencia_tensorrt.csv",
        help="Archivo CSV donde se guardarán las métricas.",
    )
    parser.add_argument(
        "--log-path",
        default="models/sprint4/logs/latency_tensorrt.log",
        help="Ruta del archivo de log.",
    )

    main(parser.parse_args())

