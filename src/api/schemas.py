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
    probabilidades: dict[str, float] = Field(
        ..., description="Probabilidad estimada por cada clase de riesgo."
    )
    clase_predicha: int = Field(..., ge=0, description="Índice de la clase con mayor probabilidad.")
    clase_predicha_label: str = Field(
        ..., description="Etiqueta de la clase con mayor probabilidad."
    )
    riesgoso: bool = Field(
        ..., description="True si la clase predicha no es la de menor riesgo (índice 0)."
    )


class PredictBatchResponse(BaseModel):
    resultados: list[PredictResponse] = Field(
        ...,
        description="Resultados de predicción para cada fila enviada.",
    )


class ObraSummary(BaseModel):
    identificador_obra: str
    sector: str | None = None
    nivel_gobierno: str | None = None
    departamento: str | None = None


class ObraListResponse(BaseModel):
    obras: list[ObraSummary]


class ObraDetailResponse(BaseModel):
    identificador_obra: str
    features: dict[str, Any] = Field(
        ..., description="Valores de la obra alineados a las columnas que espera el modelo."
    )


class ExplainRequest(BaseModel):
    fila: dict[str, Any] = Field(
        ..., description="Registro con las variables esperadas por el modelo."
    )

    model_config = ConfigDict(extra="allow")


class ShapContribution(BaseModel):
    feature: str
    shap_value: float = Field(
        ..., description="Contribución SHAP a la clase predicha (signo indica dirección)."
    )


class ExplainResponse(BaseModel):
    clase_predicha: int
    clase_predicha_label: str
    contribuciones: list[ShapContribution] = Field(
        ..., description="Top atributos por |valor SHAP|, orden descendente."
    )
