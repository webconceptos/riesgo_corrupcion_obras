import json
from pathlib import Path


def test_meta_file_exists_and_has_keys():
    meta_path = Path("models/obra_v4/pipeline_rf_obra_3clases_final_meta.json")
    assert meta_path.exists(), f"Falta {meta_path}"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    for k in ("features", "class_labels"):
        assert k in meta, f"Meta sin clave '{k}'"
