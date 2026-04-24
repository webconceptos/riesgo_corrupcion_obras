import pandas as pd

def limpiar_campos_texto(df: pd.DataFrame, cols: dict[str, str]) -> pd.DataFrame:
    out = df.copy()
    for col, new in cols.items():
        if col in out.columns:
            out[new] = out[col].astype(str).str.strip().str.lower()
    return out


def imputar_basico(df: pd.DataFrame, fill_map: dict[str, object]) -> pd.DataFrame:
    out = df.copy()
    for col, val in fill_map.items():
        if col in out.columns:
            out[col] = out[col].fillna(val)
    return out