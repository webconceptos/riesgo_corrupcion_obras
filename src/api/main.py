import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.deps import get_model_and_meta
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


@app.post("/predict_proba", response_model=PredictBatchResponse, tags=["predict"])
def predict_proba(req: BatchPredictRequest):
    pipeline, meta = get_model_and_meta()

    cols_meta = meta.get("features") or meta.get("columns")
    threshold = float(meta.get("threshold", meta.get("best_threshold_f1", 0.5)))

    if not cols_meta or not isinstance(cols_meta, list):
        raise HTTPException(status_code=500, detail="Metadata sin columnas/features válidas.")

    aligned = [{col: row.get(col, None) for col in cols_meta} for row in req.filas]
    X = pd.DataFrame(aligned, columns=cols_meta)

    try:
        probas = pipeline.predict_proba(X)[:, 1]
    except AttributeError:
        if not hasattr(pipeline, "decision_function"):
            raise HTTPException(
                status_code=500,
                detail="El modelo no soporta predict_proba ni decision_function.",
            )

        scores = pipeline.decision_function(X)
        probas = (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)

    resultados = [
        PredictResponse(
            proba=float(proba),
            threshold=threshold,
            riesgoso=bool(proba >= threshold),
        )
        for proba in probas
    ]

    return PredictBatchResponse(resultados=resultados)

@app.post("/predict_batch", tags=["predict"])
def predict_batch(payload: list[dict]):
    pipeline, meta = get_model_and_meta()

    cols_meta = meta.get("features") or meta.get("columns")
    threshold = float(meta.get("threshold", meta.get("best_threshold_f1", 0.5)))

    if not cols_meta or not isinstance(cols_meta, list):
        raise HTTPException(status_code=500, detail="Metadata sin columnas/features válidas.")

    if not payload:
        raise HTTPException(status_code=400, detail="El payload no puede estar vacío.")

    aligned = [{col: row.get(col, None) for col in cols_meta} for row in payload]
    X = pd.DataFrame(aligned, columns=cols_meta)

    try:
        probas = pipeline.predict_proba(X)[:, 1]
    except AttributeError:
        if not hasattr(pipeline, "decision_function"):
            raise HTTPException(
                status_code=500,
                detail="El modelo no soporta predict_proba ni decision_function.",
            )

        scores = pipeline.decision_function(X)
        probas = (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)

    labels = (probas >= threshold).astype(int)

    return {
        "resultados": [
            {
                "proba": float(proba),
                "label": int(label),
                "riesgoso": bool(label),
            }
            for proba, label in zip(probas, labels)
        ],
        "threshold": threshold,
        "n": len(payload),
    }