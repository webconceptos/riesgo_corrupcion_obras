import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def read_any(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, encoding="utf-8", low_memory=False)
    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    raise ValueError(f"Formato no soportado: {path.suffix}")


def smart_concat(files):
    frames = []
    for f in files:
        try:
            df = read_any(f)
            df.columns = [str(c).strip() for c in df.columns]
            frames.append(df)
        except Exception as e:
            print(f"[WARN] {f.name}: {e}")
    if not frames:
        return pd.DataFrame()
    all_cols = sorted({c for df in frames for c in df.columns})
    aligned = []
    for df in frames:
        for c in all_cols:
            if c not in df.columns:
                df[c] = np.nan
        aligned.append(df[all_cols])
    return pd.concat(aligned, ignore_index=True)


def build_dataset(kind: str, src_dir: Path, out_dir: Path):
    files = [p for p in src_dir.iterdir() if p.suffix.lower() in [".csv", ".xlsx", ".xls"]]
    if not files:
        print(f"[INFO] Sin archivos en {src_dir}")
        return None
    df = smart_concat(files)
    out_path = out_dir / f"dataset_{kind}.parquet"
    df.to_parquet(out_path, index=False)
    print(f"[OK] {kind}: {df.shape} -> {out_path}")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=str, default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args()
    ROOT = Path(args.root)
    out = ROOT / "data/processed"
    out.mkdir(parents=True, exist_ok=True)
    build_dataset("obras", ROOT / "data/external/obra", out)
    build_dataset("empresas", ROOT / "data/external/empresa", out)
    build_dataset("funcionarios", ROOT / "data/external/funcionario", out)


if __name__ == "__main__":
    main()
