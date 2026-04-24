"""
Pipeline Sprint 4 - Papermill Runner
Ejecuta todos los notebooks del Sprint 4 en orden.
Compatible con Deteccion_Corrupcion.
"""

import papermill as pm
import os
from datetime import datetime

# -------------------------
# CONFIGURACION
# -------------------------

BASE_PATH = "notebooks/Sprint4"
OUTPUT_BASE = "notebooks/Sprint4/outputs"

NOTEBOOKS = [
    "01_OptimizacionModelo.ipynb",
    "02_SlicesProblematcos.ipynb",
    "03_XAI_SHAP_LIME.ipynb",
    "04_InformeFinalResultados.ipynb",
    "05_PitchGeneracionMaterial.ipynb"
]

# Crear carpeta de outputs si no existe
os.makedirs(OUTPUT_BASE, exist_ok=True)

# Timestamp para versionado
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# -------------------------
# FUNCION EJECUTORA
# -------------------------

def ejecutar_notebook(input_path, output_path):
    print(f"\n>>> Ejecutando: {input_path}")
    pm.execute_notebook(
        input_path=input_path,
        output_path=output_path,
        parameters={}
    )
    print(f"✔ Finalizado: {output_path}")

# -------------------------
# EJECUCION SECUENCIAL
# -------------------------

def main():
    print("\n=== Iniciando Pipeline Sprint 4 con Papermill ===\n")

    for nb in NOTEBOOKS:
        input_nb = f"{BASE_PATH}/{nb}"
        output_nb = f"{OUTPUT_BASE}/{nb.replace('.ipynb', '')}_RUN_{timestamp}.ipynb"
        ejecutar_notebook(input_nb, output_nb)

    print("\n=== Pipeline Sprint 4 COMPLETADO ===\n")


if __name__ == "__main__":
    main()
