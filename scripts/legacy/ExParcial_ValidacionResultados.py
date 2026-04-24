# ===============================================================
# Script: validar_parcial.py
# Objetivo: Validación automática de resultados del Parcial
# Autor: Fernando García - Hilario Aradiel
# Fecha: 2025-11-12
# ===============================================================

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

INPUT = "reports/tablas/resultados_modelos_parcial.csv"
GRAPH_DIR = "reports/graficos"

print("=== Validación del Parcial ===")

os.makedirs(GRAPH_DIR, exist_ok=True)

df = pd.read_csv(INPUT)
print(df)

# ===============================================================
# Gráfico F1
# ===============================================================

plt.figure(figsize=(7,4))
sns.barplot(data=df, x="modelo", y="f1")
plt.title("Comparación F1 por Modelo")
plt.xlabel("Modelo")
plt.ylabel("F1 Score")
plt.savefig(f"{GRAPH_DIR}/f1_parcial.png", dpi=200)
plt.close()

# ===============================================================
# Gráfico Recall
# ===============================================================

plt.figure(figsize=(7,4))
sns.barplot(data=df, x="modelo", y="recall")
plt.title("Comparación Recall por Modelo")
plt.xlabel("Modelo")
plt.ylabel("Recall")
plt.savefig(f"{GRAPH_DIR}/recall_parcial.png", dpi=200)
plt.close()

print("Gráficos generados en:", GRAPH_DIR)
print("=== FIN ===")
