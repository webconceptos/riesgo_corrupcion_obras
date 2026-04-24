"""
Script: plot_radar_model.py
Autor: Fernando García - Hilario Aradiel
Objetivo: Visualizar desempeño global del modelo con gráfico radar.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_FIG = Path("reports/figures/sem6_radar_model.png")
OUT_FIG.parent.mkdir(parents=True, exist_ok=True)

# Métricas promedio (ajústalas según tus resultados reales)
labels = ["F1", "ROC-AUC", "PR-AUC"]
scores = [0.81, 0.88, 0.84]

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
scores += scores[:1]
angles += [angles[0]]

plt.figure(figsize=(6,6))
ax = plt.subplot(111, polar=True)
ax.plot(angles, scores, "o-", linewidth=2, color="#E41E26")
ax.fill(angles, scores, color="#003366", alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), labels)
ax.set_title("Desempeño Global del Modelo XGBoost", size=14, pad=20)
ax.set_ylim(0,1)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
plt.show()

print(f"✅ Figura guardada en: {OUT_FIG}")
