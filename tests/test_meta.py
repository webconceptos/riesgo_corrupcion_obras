import json
from pathlib import Path


def test_meta_file_exists_and_has_keys():
    meta_path = Path("models/pipeline_meta.json")
    assert meta_path.exists(), "Falta models/pipeline_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    for k in ("columns", "best_threshold_f1"):
        assert k in meta, f"Meta sin clave '{k}'"
