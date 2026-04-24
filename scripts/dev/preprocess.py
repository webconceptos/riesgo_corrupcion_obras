#!/usr/bin/env python
import logging
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
PROC = BASE / "data" / "processed"
LOG = BASE / "logs" / "preprocess.log"

PROC.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

OUT = PROC / "dataset_obras.parquet"


def load_concat(glob_pattern: str) -> pd.DataFrame:
    frames = []
    for p in RAW.glob(glob_pattern):
        try:
            df = pd.read_csv(p, encoding="latin-1")
            frames.append(df)
            logging.info(f"Loaded {p.name} -> {df.shape}")
        except Exception as e:
            logging.error(f"Error reading {p.name}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    # normaliza nombres
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    # elimina duplicadas exactas
    if "codigo_unico" in df.columns:
        df = df.drop_duplicates(subset=["codigo_unico"], keep="last")
    return df


def main():
    # ejemplo simple: solo obra ya consolidada (tu Notebook 02 hizo el enriquecido)
    # aquí asumimos que dataset_obras.parquet fue generado por el Notebook 02
    # si quisieras re-generarlo aquí, sustituye esta parte por tu pipeline de unión.
    src = OUT
    if not src.exists():
        logging.error(f"No existe {src}. Ejecuta el Notebook 02 antes.")
        raise SystemExit(1)

    df = pd.read_parquet(src)
    # limpieza mínima (quita 100% NaN y constantes)
    all_nan = [c for c in df.columns if df[c].isna().all()]
    df = df.drop(columns=all_nan)
    const_cols = [c for c in df.columns if df[c].nunique(dropna=True) <= 1]
    df = df.drop(columns=const_cols)

    df.to_parquet(OUT, index=False)
    logging.info(f"Saved {OUT.name} -> {df.shape}")
    print("OK:", OUT, df.shape)


if __name__ == "__main__":
    main()
