from fastapi.testclient import TestClient

from src.api.main import app


def test_health_and_meta():
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    m = c.get("/model_meta")
    assert m.status_code == 200
    assert "best_threshold_f1" in m.json()


def test_predict_shape_ok(monkeypatch):
    # Monkeypatch para evitar cargar modelo real en este test de forma aislada
    from src.api import deps

    class DummyPipe:
        def predict_proba(self, X):
            import numpy as np

            return np.c_[1 - 0.7, [0.7] * len(X)]

    def fake_get():
        return DummyPipe(), {"columns": ["a", "b"], "best_threshold_f1": 0.6}

    monkeypatch.setattr(deps, "get_model_and_meta", fake_get)
    c = TestClient(app)
    payload = {"filas": [{"a": 1, "b": 2}, {"a": 5, "b": 9, "extra": 123}]}
    r = c.post("/predict_proba", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert len(body["resultados"]) == 2
    assert body["resultados"][0]["riesgoso"] is True
