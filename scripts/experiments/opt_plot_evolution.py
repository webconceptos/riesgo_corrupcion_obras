"""
Genera gráficos de evolución y top-k de las ejecuciones Random y Bayes
"""
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from pathlib import Path

IN_RANDOM = Path("reports/tuning/random_search_results.csv")
IN_BAYES = Path("reports/tuning/bayes_opt_results.csv")
OUT_DIR = Path("reports/tuning")

plt.figure(figsize=(8,5))
if IN_RANDOM.exists():
    r = pd.read_csv(IN_RANDOM)
    plt.plot(range(len(r)), r["f1_score"], label="Random Search")
if IN_BAYES.exists():
    b = pd.read_csv(IN_BAYES)
    plt.plot(range(len(b)), b["target"], label="Bayes Opt")
plt.xlabel("Iteración"); plt.ylabel("F1-score"); plt.title("Evolución del tuning")
plt.legend(); plt.grid(True)
plt.tight_layout()
plt.savefig(OUT_DIR / "evolution_comparison.png", dpi=300)
plt.show()
print(f"✅ Gráfico guardado en {OUT_DIR}/evolution_comparison.png")
