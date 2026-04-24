"""
Script: plot_correlation_target.py
Autor: Fernando García - Hilario Aradiel
Objetivo: Analizar la correlación de las variables numéricas con y_riesgo.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("data/processed/dataset_integrado.parquet")
OUT_FIG = Path("reports/figures/sem6_corr_target.png")

print("=== Correlación con y_riesgo ===")
df = pd.read_parquet(DATA_PATH)
num_df = df.select_dtypes("number")

corr = num_df.corr()["y_riesgo"].drop("y_riesgo").sort_values(ascending=False)

plt.figure(figsize=(6,10))
sns.barplot(x=corr.values, y=corr.index, palette="coolwarm")
plt.title("Correlación de variables numéricas con y_riesgo")
plt.xlabel("Coeficiente de correlación")
plt.ylabel("Variable")
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
plt.show()

print(f"✅ Figura guardada en: {OUT_FIG}")
