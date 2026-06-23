import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api import deps
from src.api.routes.health import router as health_router
from src.api.schemas import BatchPredictRequest, PredictBatchResponse, PredictResponse

app = FastAPI(
    title="Detección de Riesgos de Corrupción",
    version="0.1.0",
    description="API para estimar el riesgo de corrupción en obras públicas.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar por entorno en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)


def _align_columns(rows: list[dict], cols_meta: list[str]) -> pd.DataFrame:
    aligned = [{col: row.get(col, None) for col in cols_meta} for row in rows]
    return pd.DataFrame(aligned, columns=cols_meta)


def _predict_multiclase(pipeline, X: pd.DataFrame, class_labels: list[str]) -> list[PredictResponse]:
    if not hasattr(pipeline, "predict_proba"):
        raise HTTPException(status_code=500, detail="El modelo no soporta predict_proba.")

    probas = pipeline.predict_proba(X)
    preds = probas.argmax(axis=1)

    return [
        PredictResponse(
            probabilidades={class_labels[i]: float(p) for i, p in enumerate(row)},
            clase_predicha=int(pred),
            clase_predicha_label=class_labels[pred],
            riesgoso=bool(pred != 0),
        )
        for row, pred in zip(probas, preds)
    ]


@app.post("/predict_proba", response_model=PredictBatchResponse, tags=["predict"])
def predict_proba(req: BatchPredictRequest):
    pipeline, meta = deps.get_model_and_meta()

    cols_meta = meta.get("features") or meta.get("columns")
    class_labels = meta.get("class_labels")

    if not cols_meta or not isinstance(cols_meta, list):
        raise HTTPException(status_code=500, detail="Metadata sin columnas/features válidas.")
    if not class_labels or not isinstance(class_labels, list):
        raise HTTPException(status_code=500, detail="Metadata sin class_labels válidas.")

    X = _align_columns(req.filas, cols_meta)
    resultados = _predict_multiclase(pipeline, X, class_labels)

    return PredictBatchResponse(resultados=resultados)


@app.post("/predict_batch", response_model=PredictBatchResponse, tags=["predict"])
def predict_batch(payload: list[dict]):
    pipeline, meta = deps.get_model_and_meta()

    cols_meta = meta.get("features") or meta.get("columns")
    class_labels = meta.get("class_labels")

    if not cols_meta or not isinstance(cols_meta, list):
        raise HTTPException(status_code=500, detail="Metadata sin columnas/features válidas.")
    if not class_labels or not isinstance(class_labels, list):
        raise HTTPException(status_code=500, detail="Metadata sin class_labels válidas.")
    if not payload:
        raise HTTPException(status_code=400, detail="El payload no puede estar vacío.")

    X = _align_columns(payload, cols_meta)
    resultados = _predict_multiclase(pipeline, X, class_labels)

    return PredictBatchResponse(resultados=resultados)