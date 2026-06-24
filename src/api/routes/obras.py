import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException

from src.api import deps
from src.api.schemas import ObraDetailResponse, ObraListResponse, ObraSummary

router = APIRouter(tags=["obras"])

ID_COL = "IDENTIFICADOR_OBRA"
SECTOR_COL = "obra_ctx_sector"
NIVEL_GOBIERNO_COL = "obra_ctx_nivel_gobierno"
DEPARTAMENTO_COL = "obra_ctx_departamento"


def _clean(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


@router.get("/obras", response_model=ObraListResponse)
def list_obras():
    df = deps.get_dataset()

    obras = [
        ObraSummary(
            identificador_obra=str(row[ID_COL]),
            sector=_clean(row.get(SECTOR_COL)),
            nivel_gobierno=_clean(row.get(NIVEL_GOBIERNO_COL)),
            departamento=_clean(row.get(DEPARTAMENTO_COL)),
        )
        for row in df.to_dict(orient="records")
    ]

    return ObraListResponse(obras=obras)


@router.get("/obras/{identificador_obra}", response_model=ObraDetailResponse)
def get_obra(identificador_obra: str):
    df = deps.get_dataset()
    _, meta = deps.get_model_and_meta()

    cols_meta = meta.get("features") or meta.get("columns")
    if not cols_meta or not isinstance(cols_meta, list):
        raise HTTPException(status_code=500, detail="Metadata sin columnas/features válidas.")

    match = df[df[ID_COL].astype(str) == identificador_obra]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"No existe la obra '{identificador_obra}'.")

    row = match.iloc[0]
    features = {col: _clean(row.get(col)) for col in cols_meta}

    return ObraDetailResponse(identificador_obra=identificador_obra, features=features)
