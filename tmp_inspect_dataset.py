import pandas as pd
from pathlib import Path
path = Path("data/processed/dataset_modelado.parquet")
df = pd.read_parquet(path)
print("shape", df.shape)
print("columns", list(df.columns)[:50])
print("dtypes", df.dtypes.value_counts().to_dict())
print("nulls", df.isna().sum().sort_values(ascending=False).head(20).to_dict())
print("target unique", df["target"].value_counts(normalize=True, dropna=False).to_dict())
