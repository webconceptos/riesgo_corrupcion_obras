import json
from functools import lru_cache
from typing import Any

import joblib
import pandas as pd

from src.config.config import DATASET_PATH, MODEL_META_PATH, MODEL_PATH


class ModelNotFoundError(RuntimeError):
    pass


class MetaNotFoundError(RuntimeError):
    pass


class InvalidMetaError(RuntimeError):
    pass


class DatasetNotFoundError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_model_and_meta() -> tuple[Any, dict]:
    if not MODEL_PATH.exists():
        raise ModelNotFoundError(f"No existe el modelo: {MODEL_PATH}")

    if not MODEL_META_PATH.exists():
        raise MetaNotFoundError(f"No existe la metadata del modelo: {MODEL_META_PATH}")

    pipeline = joblib.load(MODEL_PATH)

    with open(MODEL_META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    if not isinstance(meta, dict):
        raise InvalidMetaError("La metadata del modelo no tiene formato de diccionario.")

    return pipeline, meta


def clear_model_cache() -> None:
    get_model_and_meta.cache_clear()
    get_dataset.cache_clear()
    get_feature_stats.cache_clear()


@lru_cache(maxsize=1)
def get_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise DatasetNotFoundError(f"No existe el dataset: {DATASET_PATH}")

    return pd.read_parquet(DATASET_PATH)


@lru_cache(maxsize=1)
def get_feature_stats() -> dict[str, dict[str, float]]:
    df = get_dataset()
    numeric = df.select_dtypes(include="number")
    stats = numeric.agg(["median", "min", "max"])
    return {
        col: {
            "median": float(stats.loc["median", col]),
            "min": float(stats.loc["min", col]),
            "max": float(stats.loc["max", col]),
        }
        for col in numeric.columns
    }
