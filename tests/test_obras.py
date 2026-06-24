import pandas as pd
from fastapi.testclient import TestClient

from src.api import deps
from src.api.main import app


def _fake_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "IDENTIFICADOR_OBRA": ["OBRA-1", "OBRA-2"],
            "obra_ctx_sector": ["TRANSPORTE", "SALUD Y SANEAMIENTO"],
            "obra_ctx_nivel_gobierno": ["GOBIERNO NACIONAL", "GOBIERNO REGIONAL"],
            "obra_ctx_departamento": ["LIMA", "CUSCO"],
            "a": [1.0, 5.0],
            "b": [2.0, 9.0],
        }
    )


def test_list_obras(monkeypatch):
    deps.clear_model_cache()
    monkeypatch.setattr(deps, "get_dataset", _fake_dataset)
    c = TestClient(app)
    r = c.get("/obras")
    assert r.status_code == 200
    obras = r.json()["obras"]
    assert len(obras) == 2
    assert obras[0]["identificador_obra"] == "OBRA-1"
    assert obras[0]["sector"] == "TRANSPORTE"


def test_get_obra_found_and_not_found(monkeypatch):
    deps.clear_model_cache()
    monkeypatch.setattr(deps, "get_dataset", _fake_dataset)
    monkeypatch.setattr(
        deps,
        "get_model_and_meta",
        lambda: (object(), {"features": ["a", "b"]}),
    )
    c = TestClient(app)

    r = c.get("/obras/OBRA-2")
    assert r.status_code == 200
    assert r.json()["features"] == {"a": 5.0, "b": 9.0}

    r404 = c.get("/obras/NO-EXISTE")
    assert r404.status_code == 404
