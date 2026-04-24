"""
00_smoke_test.py
----------------
Smoke test del Sprint 4.
Verifica que los artefactos críticos del pipeline existan
antes de considerar el despliegue como válido.
"""

from pathlib import Path
import sys

REQUIRED_FILES = [
    "models/sprint4/dataset_preparado.parquet",
    "models/sprint4/resultados/metrics_baseline.csv",
    "models/sprint4/resultados/metrics_modelo_actual.csv",
    "models/sprint4/reportes/informe_sprint4.md",
]

errors = False

print("🔎 Ejecutando Smoke Test Sprint 4...\n")

for f in REQUIRED_FILES:
    path = Path(f)
    if not path.exists():
        print(f"[ERROR] Falta archivo crítico: {f}")
        errors = True
    else:
        print(f"[OK] {f}")

if errors:
    print("\n❌ Smoke test FALLÓ. No es seguro desplegar.")
    sys.exit(1)

print("\n✅ Smoke test PASADO. Pipeline listo para despliegue.")
