"""
utils_sprint4.py
----------------
Conjunto de funciones utilitarias utilizadas por todos los scripts del Sprint 4.

Incluye:
- Logging estándar
- Carga de modelos y datasets
- Métricas comunes
- Funciones de latencia (p50, p95, p99)
- Manejo de tiempos de ejecución
- Utilitarios generales para MLOps
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd


# =============================================================
# 1. LOGGING ESTÁNDAR
# =============================================================

def setup_logger(log_path: str | Path) -> logging.Logger:
    """
    Configura un logger que escribe a archivo y a consola.
    Si el archivo existe, se sobreescribe.
    """
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(str(log_path))
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info(f"Logger inicializado en: {log_path}")
    return logger


# =============================================================
# 2. CARGA DE DATASET
# =============================================================

def load_dataset(path: str | Path) -> pd.DataFrame:
    """
    Carga dataset en CSV o Parquet automáticamente.

    - Si termina en .csv → usa pd.read_csv
    - Si termina en .parquet → usa pd.read_parquet
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"El dataset no existe: {path}")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in [".parquet", ".pq"]:
        df = pd.read_parquet(path)
    else:
        raise ValueError(f"Formato no soportado: {path.suffix}")

    if df.empty:
        raise ValueError(f"El dataset cargado está VACÍO: {path}")

    return df



# =============================================================
# 3. CARGA DE MODELOS (sklearn / joblib)
# =============================================================

def load_sklearn_model(model_path: str | Path):
    """
    Carga un modelo sklearn serializado con joblib.
    """
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"El modelo no existe: {model_path}")

    return joblib.load(model_path)


# =============================================================
# 4. MÉTRICAS Y EXPORTACIÓN
# =============================================================

def save_metrics_csv(metrics: Dict[str, Any], out_path: str | Path) -> None:
    """
    Guarda un diccionario de métricas en un CSV.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame([metrics])
    df.to_csv(out_path, index=False)


# =============================================================
# 5. LATENCIA – mediciones repetidas
# =============================================================

def time_function(
    func: Callable,
    *args,
    n_runs: int = 50,
    **kwargs
) -> Tuple[List[float], float]:
    """
    Ejecuta una función varias veces y captura el tiempo de ejecución.

    Returns:
        latencias_ms: lista de latencias en milisegundos
        total_time_s: tiempo total de ejecución en segundos
    """
    latencias_ms = []

    t0_total = perf_counter()
    for _ in range(n_runs):
        t0 = perf_counter()
        func(*args, **kwargs)
        t1 = perf_counter()
        latencias_ms.append((t1 - t0) * 1000.0)
    t1_total = perf_counter()

    return latencias_ms, (t1_total - t0_total)


def latency_stats(latencies_ms: List[float]) -> Dict[str, float]:
    """
    Calcula estadísticos de latencia típicos (p50, p95, p99).
    """
    arr = np.array(latencies_ms)

    return {
        "mean_ms": float(arr.mean()),
        "std_ms": float(arr.std()),
        "min_ms": float(arr.min()),
        "max_ms": float(arr.max()),
        "p50_ms": float(np.percentile(arr, 50)),
        "p90_ms": float(np.percentile(arr, 90)),
        "p95_ms": float(np.percentile(arr, 95)),
        "p99_ms": float(np.percentile(arr, 99)),
    }


# =============================================================
# 6. UTILITARIOS GENERALES
# =============================================================

def ensure_parent_dir(path: str | Path):
    """
    Crea la carpeta padre si no existe.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)


def save_json(data: Dict[str, Any], out_path: str | Path) -> None:
    """
    Guarda un diccionario en un archivo JSON.
    """
    out_path = Path(out_path)
    ensure_parent_dir(out_path)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def pretty_print_dict(d: Dict[str, Any]) -> None:
    """
    Imprime un diccionario de forma legible.
    """
    print(json.dumps(d, indent=4, ensure_ascii=False))


# =============================================================
# 7. FUNCIONES UTILIZADAS PARA SPRINT 4
# =============================================================

def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder de preprocesamiento para Sprint 4.

    Aquí puedes:
    - limpiar valores
    - imputar
    - generar features nuevas
    - normalizar
    - etc.

    Esta función puede ser reemplazada por tu pipeline real.
    """
    df = df.copy()
    df = df.fillna(0)
    return df
