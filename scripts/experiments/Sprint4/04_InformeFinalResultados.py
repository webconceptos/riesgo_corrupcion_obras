import os
import pandas as pd
import matplotlib.pyplot as plt

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
            raise RuntimeError("No se encontró .git en ningún nivel superior.")
        current = parent

PROJECT_ROOT = find_project_root(os.getcwd())

DATA_PROCESSED = os.path.join(PROJECT_ROOT, "data", "processed")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models", "sprint4")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "models", "sprint4", "reportes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"MODELS_DIR:   {MODELS_DIR}")

# ---------------------------
# 2. Cargar resultados
# ---------------------------
file_modelos = os.path.join(MODELS_DIR, "resultados_modelos.csv")
file_slices = os.path.join(MODELS_DIR, "slices_problematicos.csv")

df_modelos = pd.read_csv(file_modelos)
df_slices = pd.read_csv(file_slices)

print("\n=== Métricas de Modelos ===")
print(df_modelos)

print("\n=== Slices Problemáticos ===")
print(df_slices.head())

# ---------------------------
# 3. Graficar ranking F1
# ---------------------------
plt.figure(figsize=(8, 4))
df_modelos.sort_values("f1", ascending=False).plot(
    x="modelo", y="f1", kind="bar", legend=False
)
plt.title("Comparación de Modelos (F1)")
plt.tight_layout()

img_f1 = os.path.join(OUTPUT_DIR, "ranking_f1.png")
plt.savefig(img_f1)
plt.close()

# ---------------------------
# 4. Guardar resumen general
# ---------------------------
resumen_path = os.path.join(OUTPUT_DIR, "informe_sprint4.md")

with open(resumen_path, "w", encoding="utf-8") as f:
    f.write("# Informe Final Sprint 4\n\n")
    f.write("## Modelos Evaluados\n")
    #f.write(df_modelos.to_markdown() + "\n\n")
    try:
        f.write(df_modelos.to_markdown() + "\n\n")
    except:
        f.write(df_modelos.to_string() + "\n\n")

    f.write("## Slices Problemáticos\n")
    f.write(df_slices.head(10).to_markdown() + "\n\n")

    f.write("## Conclusiones\n")
    f.write("- El modelo con mejor F1 es seleccionado como final.\n")
    f.write("- Los slices permiten identificar segmentos de riesgo.\n")
    f.write("- SHAP aporta interpretabilidad técnica valiosa.\n")

print("\n=== Informe Final Generado ===")
print(f"Markdown: {resumen_path}")
print(f"Gráfico:   {img_f1}")
