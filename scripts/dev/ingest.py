#!/usr/bin/env python
import hashlib
import json
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
LOG = BASE / "logs" / "ingest.log"
REG = BASE / "data" / "datasets.json"

print("BASE:", BASE)

RAW.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


def sha256sum(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/ingest.py <ruta_origen> [nombre_destino]")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        raise FileNotFoundError(src)

    dst = RAW / (sys.argv[2] if len(sys.argv) > 2 else src.name)
    shutil.copy2(src, dst)

    meta = {
        "file": str(dst.relative_to(BASE)),
        "bytes": dst.stat().st_size,
        "sha256": sha256sum(dst),
        "ingested_at": datetime.utcnow().isoformat() + "Z",
    }

    # registrar en datasets.json
    REG.parent.mkdir(parents=True, exist_ok=True)
    if REG.exists():
        register = json.loads(REG.read_text(encoding="utf-8"))
    else:
        register = []
    register.append(meta)
    REG.write_text(json.dumps(register, indent=2), encoding="utf-8")

    logging.info(f"INGESTED {dst.name} | {meta['bytes']} bytes | {meta['sha256']}")
    print("OK:", json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
