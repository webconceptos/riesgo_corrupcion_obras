"""
Combina los resultados, genera top-k y resumen del espacio
"""
import pandas as pd, json
from pathlib import Path

OUT_DIR = Path("reports/tuning")
r = pd.read_csv(OUT_DIR/"random_search_results.csv")
b = pd.read_csv(OUT_DIR/"bayes_opt_results.csv")

r["method"] = "random"
b["method"] = "bayes"

df = pd.concat([r,b], ignore_index=True)
df = df.sort_values(df.columns[-2], ascending=False)
topk = df.head(10)
topk.to_csv(OUT_DIR/"topk_summary.csv", index=False)

print("✅ Top-10 mejores configuraciones guardadas en reports/tuning/topk_summary.csv")
