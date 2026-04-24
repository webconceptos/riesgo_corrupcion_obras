# ===============================================================
# Script: ExParcial_validar_modelos.py
# Autor: Fernando García - Hilario Aradiel
# Fecha: 2025-11-12
# ===============================================================

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

INPUT = "reports/tablas/resultados_modelos_parcial.csv"
GRAPH_DIR = "reports/graficos"

os.makedirs(GRAPH_DIR, exist_ok=True)

df = pd.read_csv(INPUT)

# F1
plt.figure(figsize=(7,4))
sns.barplot(data=df, x="modelo", y="f1")
plt.title("F1 por modelo")
plt.savefig(f"{GRAPH_DIR}/f1_parcial.png", dpi=200)
plt.close()

# Recall
plt.figure(figsize=(7,4))
sns.barplot(data=df, x="modelo", y="recall")
plt.title("Recall por modelo")
plt.savefig(f"{GRAPH_DIR}/recall_parcial.png", dpi=200)
plt.close()

print("Gráficos generados en:", GRAPH_DIR)
