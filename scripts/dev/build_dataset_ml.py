"""
Script de integración para generar dataset de entrenamiento ML
Proyecto: Detección de Riesgo de Corrupción en Obras Públicas (Semana 6)
Autores: Fernando García - Hilario Aradiel
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path("data/external")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)


# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# =======================
#  Funciones auxiliares
# =======================

def load_all_csv(folder: Path):
    """Lee y concatena todos los CSV de una carpeta."""
    files = list(folder.glob("*.csv"))
    frames = []
    for f in files:
        try:
            df = pd.read_csv(f, encoding="latin-1")
            df["__source"] = f.name
            frames.append(df)
            print(f"✅ Cargado {f.name:40s} → {df.shape[0]} filas, {df.shape[1]} cols")
        except Exception as e:
            print(f"⚠️ Error en {f.name}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def load_riesgo_excel(path: Path):
    """Carga hoja de perfilamiento de riesgo (si existe)."""
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_excel(path)
        df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
        print(f"✅ Perfilamiento de riesgo: {path.name:40s} ({len(df)} filas)")
        return df
    except Exception as e:
        print(f"⚠️ Error leyendo {path.name}: {e}")
        return pd.DataFrame()

def clean_base(df: pd.DataFrame):
    """Limpieza general."""
    df = df.drop_duplicates()
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
    return df

# =======================
#  Ejecución principal
# =======================

def main():
    print("\n=== [1] CARGA DE FUENTES ===")
    obras = load_all_csv(BASE / "obra")
    empresas = load_all_csv(BASE / "empresa")
    funcionarios = load_all_csv(BASE / "funcionario")

    obras = clean_base(obras)
    empresas = clean_base(empresas)
    funcionarios = clean_base(funcionarios)

    print(f"\n📊 Obras: {obras.shape}, Empresas: {empresas.shape}, Funcionarios: {funcionarios.shape}")

    print("\n=== [2] CARGA DE PERFILAMIENTO DE RIESGO ===")
    riesgo_obra = load_riesgo_excel(BASE / "obra" / "perfilamiento_obra_riesgosa.xlsx")
    riesgo_emp = load_riesgo_excel(BASE / "empresa" / "perfilamiento_empresa_riesgosa.xlsx")
    riesgo_fun = load_riesgo_excel(BASE / "funcionario" / "perfilamiento_funcionario_riesgosa.xlsx")

    # =======================
    #  UNIFICACIÓN
    # =======================
    print("\n=== [3] UNIFICACIÓN DE FUENTES ===")

    df = obras.copy()
    # Merge riesgo_obra
    if not riesgo_obra.empty:
        common = list(set(df.columns) & set(riesgo_obra.columns))
        if common:
            df = df.merge(riesgo_obra, how="left", on=common[0], suffixes=("", "_RIESGO"))
            print(f"🔗 Unión con riesgo_obra por {common[0]}")
    # Merge empresas
    if "RUC" in df.columns and "RUC" in empresas.columns:
        df = df.merge(empresas, how="left", on="RUC", suffixes=("_OBR", "_EMP"))
        print("🔗 Unión con empresas por RUC")
    # Merge funcionarios
    if "DNI" in df.columns and "DNI" in funcionarios.columns:
        df = df.merge(funcionarios, how="left", on="DNI", suffixes=("", "_FUN"))
        print("🔗 Unión con funcionarios por DNI")

    print(f"✅ Dataset unificado temporal: {df.shape[0]} filas, {df.shape[1]} columnas")

    # =======================
    #  CREACIÓN DE ETIQUETA
    # =======================
    print("\n=== [4] CREACIÓN DE VARIABLE OBJETIVO (y_riesgo) ===")

    cols_lower = [c.lower() for c in df.columns]
    y_col = None
    for c in df.columns:
        if "riesgo" in c.lower():
            y_col = c
            break

    if y_col:
        df["y_riesgo"] = (
            df[y_col].astype(str).str.contains("alto|riesgo", case=False, na=False)
        ).astype(int)
        print(f"✅ Etiqueta creada desde columna existente: {y_col}")
    else:
        df["y_riesgo"] = np.random.choice([0, 1], len(df), p=[0.7, 0.3])
        print("⚠️ No se encontró columna de riesgo → etiqueta simulada generada.")

    # =======================
    #  SELECCIÓN DE VARIABLES
    # =======================
    print("\n=== [5] SELECCIÓN DE VARIABLES ===")
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    keep = list(set(numeric_cols + ["y_riesgo"]))
    df_final = df[keep].copy()

    # =======================
    #  LIMPIEZA FINAL
    # =======================
    print("\n=== [6] LIMPIEZA FINAL ===")
    dups = df_final.columns[df_final.columns.duplicated()].tolist()
    if dups:
        print(f"⚠️ Columnas duplicadas eliminadas: {dups}")
    df_final = df_final.loc[:, ~df_final.columns.duplicated()].copy()

    # =======================
    #  EXPORTACIÓN
    # =======================
    out_file = OUT / "dataset_obras.parquet"
    df_final.to_parquet(out_file, index=False)
    print(f"\n✅ Dataset final guardado en: {out_file}")
    print(f"   → {df_final.shape[0]} filas, {df_final.shape[1]} columnas")

if __name__ == "__main__":
    main()
