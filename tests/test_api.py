from fastapi.testclient import TestClient

from src.api.main import app


def test_health_and_meta():
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    m = c.get("/model_meta")
    assert m.status_code == 200
    assert "class_labels" in m.json()


def test_predict_shape_ok(monkeypatch):
    # Monkeypatch para evitar cargar modelo real en este test de forma aislada
    from src.api import deps

    class DummyPipe:
        def predict_proba(self, X):
            import numpy as np

            # 2 filas x 3 clases: la primera predice clase 2, la segunda clase 0
            return np.array([[0.1, 0.2, 0.7], [0.8, 0.1, 0.1]])

    def fake_get():
        return DummyPipe(), {
            "columns": ["a", "b"],
            "class_labels": ["Bajo Riesgo", "Med/Alt Riesgosa", "Extrem. Riesgosa"],
        }

    deps.clear_model_cache()
    monkeypatch.setattr(deps, "get_model_and_meta", fake_get)
    c = TestClient(app)
    payload = {"filas": [{"a": 1, "b": 2}, {"a": 5, "b": 9, "extra": 123}]}
    r = c.post("/predict_proba", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert len(body["resultados"]) == 2
    assert body["resultados"][0]["clase_predicha"] == 2
    assert body["resultados"][0]["clase_predicha_label"] == "Extrem. Riesgosa"
    assert body["resultados"][0]["riesgoso"] is True
    assert body["resultados"][1]["clase_predicha"] == 0
    assert body["resultados"][1]["riesgoso"] is False
