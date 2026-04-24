from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BatchPredictRequest(BaseModel):
    """
    Payload para predicción batch.
    Cada elemento de `filas` representa una obra o registro a evaluar.
    """

    filas: list[dict[str, Any]] = Field(
        ...,
        min_length=1,
        description="Lista de registros con las variables esperadas por el modelo.",
    )

    model_config = ConfigDict(extra="allow")

    @field_validator("filas")
    @classmethod
    def non_empty_rows(cls, value: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for index, row in enumerate(value):
            if not isinstance(row, dict) or not row:
                raise ValueError(f"Fila {index} vacía o inválida.")
        return value


class PredictResponse(BaseModel):
    proba: float = Field(..., ge=0, le=1, description="Probabilidad estimada de riesgo.")
    threshold: float = Field(..., ge=0, le=1, description="Umbral usado para clasificar riesgo.")
    riesgoso: bool = Field(..., description="Indica si el registro supera el umbral de riesgo.")


class PredictBatchResponse(BaseModel):
    resultados: list[PredictResponse] = Field(
        ...,
        description="Resultados de predicción para cada fila enviada.",
    )