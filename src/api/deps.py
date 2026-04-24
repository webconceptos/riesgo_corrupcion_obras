import json
from functools import lru_cache
from typing import Any

import joblib

from src.config.config import MODEL_META_PATH, MODEL_PATH


class ModelNotFoundError(RuntimeError):
    pass


class MetaNotFoundError(RuntimeError):
    pass


class InvalidMetaError(RuntimeError):
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