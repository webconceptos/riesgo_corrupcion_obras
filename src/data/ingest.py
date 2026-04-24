from pathlib import Path

import pandas as pd


def leer_excel(path: str | Path, sheet_name: str | int = 0) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name)


def leer_csv(path: str | Path, sep: str = ",") -> pd.DataFrame:
    return pd.read_csv(path, sep=sep)


def guardar_parquet(df: pd.DataFrame, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)