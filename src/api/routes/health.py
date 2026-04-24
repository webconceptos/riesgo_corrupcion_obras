from fastapi import APIRouter, HTTPException, status

from src.api.deps import get_model_and_meta

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    try:
        get_model_and_meta()
        return {"status": "ok", "model_loaded": True}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "error",
                "model_loaded": False,
                "message": str(exc),
            },
        )


@router.get("/model_meta")
def model_meta():
    _, meta = get_model_and_meta()

    excluded_fields = {
        "feature_importances_raw",
        "raw_report",
        "classification_report_raw",
    }

    safe_meta = {k: v for k, v in meta.items() if k not in excluded_fields}

    return safe_meta