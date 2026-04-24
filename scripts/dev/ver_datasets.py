import pandas as pd
from pathlib import Path

for file in Path("data/processed").glob("dataset_*.parquet"):
    print(f"\n=== {file.name} ===")
    try:
        df = pd.read_parquet(file)
        print(f"Filas: {len(df)}, Columnas: {len(df.columns)}")
        print("Columnas:", df.columns.tolist()[:15], "...\n")
    except Exception as e:
        print("Error:", e)
