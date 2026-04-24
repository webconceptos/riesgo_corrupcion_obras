import os
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import dedent

# ---------------------------
# 1. Detectar raíz del proyecto
# ---------------------------
def find_project_root(start_path):
    current = start_path
    while True:
        if os.path.exists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("No se encontró .git.")
        current = parent

PROJECT_ROOT = find_project_root(os.getcwd())
MODELS_DIR = os.path.join(PROJECT_ROOT, "models", "sprint4")
PITCH_DIR = os.path.join(MODELS_DIR, "pitch")

os.makedirs(PITCH_DIR, exist_ok=True)

print(f"PROJECT_ROOT: {PROJECT_ROOT}")

# ---------------------------
# 2. Archivos base
# ---------------------------
resultados_path = os.path.join(MODELS_DIR, "resultados_modelos.csv")
df = pd.read_csv(resultados_path)

modelo_top = df.sort_values("f1", ascending=False).iloc[0]["modelo"]
f1_top = df.sort_values("f1", ascending=False).iloc[0]["f1"]

# ---------------------------
# 3. Imagen simple para el pitch
# ---------------------------
plt.figure(figsize=(6, 4))
df.plot(x="modelo", y="f1", kind="bar", legend=False)
plt.title("Modelos Evaluados - F1")
plt.tight_layout()

img_path = os.path.join(PITCH_DIR, "pitch_modelos_f1.png")
plt.savefig(img_path)
plt.close()

# ---------------------------
# 4. Generar el texto del pitch
# ---------------------------
pitch_md = os.path.join(PITCH_DIR, "pitch_sprint4.md")

texto = dedent(f"""
# Pitch Técnico Sprint 4

## 1. Objetivo
Identificar riesgo de corrupción en obras públicas usando machine learning.

## 2. Modelo Ganador
- **Modelo:** {modelo_top}
- **F1 Score:** {f1_top:.4f}

## 3. Interpretabilidad
- Se usaron técnicas SHAP/LIME para explicar predicciones.
- Las variables críticas fueron validadas con stakeholders.

## 4. Segmentos Riesgosos
- Se identificaron slices con alta pérdida de desempeño.
- Estos segmentos serán priorizados en auditorías preventivas.

## 5. Resultado
Un modelo optimizado, interpretado y con análisis de segmentos,
listo para integrarse en la plataforma de la CGR.
""")

with open(pitch_md, "w", encoding="utf-8") as f:
    f.write(texto)

print("=== Pitch generado ===")
print(f"Imagen: {img_path}")
print(f"Texto:  {pitch_md}")
