"""
Script maestro: integración de obras, empresas y funcionarios
Proyecto: Detección de Riesgo de Corrupción en Obras Públicas (CGR)
Autor: Webconceptos / Fernando García
Versión: Semana 6 → Dataset Integrado para Semana 7
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

# ----------------------------------------------------------------------
# Funciones utilitarias
# ----------------------------------------------------------------------

def load_csv_folder(folder: Path):
    """Lee todos los CSVs de una carpeta y los concatena."""
    frames = []
    for f in folder.glob("*.csv"):
        try:
            df = pd.read_csv(f, encoding="latin-1")
            df["__source"] = f.name
            frames.append(df)
            print(f"✅ Cargado {f.name:35s} → {df.shape}")
        except Exception as e:
            print(f"⚠️ Error en {f.name}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def load_excel(path: Path):
    """Carga Excel de perfilamiento de riesgo."""
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_excel(path)
        df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
        print(f"✅ Cargado perfilamiento: {path.name:35s} ({df.shape})")
        return df
    except Exception as e:
        print(f"⚠️ Error en {path.name}: {e}")
        return pd.DataFrame()

def clean(df: pd.DataFrame):
    """Limpieza y normalización básica."""
    df = df.drop_duplicates()
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
    return df

# ----------------------------------------------------------------------
# Generación del dataset integrado
# ----------------------------------------------------------------------

def main():
    print("\n=== [1] CARGA DE FUENTES ===")
    obras = clean(load_csv_folder(BASE / "obra"))
    empresas = clean(load_csv_folder(BASE / "empresa"))
    funcionarios = clean(load_csv_folder(BASE / "funcionario"))

    print(f"📊 Obras: {obras.shape}, Empresas: {empresas.shape}, Funcionarios: {funcionarios.shape}")

    # ------------------------------------------------------------------
    # Carga de perfilamientos
    # ------------------------------------------------------------------
    print("\n=== [2] CARGA DE PERFILAMIENTOS ===")
    perf_obra = load_excel(BASE / "obra" / "perfilamiento_obra_riesgosa.xlsx")
    perf_emp = load_excel(BASE / "empresa" / "perfilamiento_empresa_riesgosa.xlsx")
    perf_fun = load_excel(BASE / "funcionario" / "perfilamiento_funcionario_riesgosa.xlsx")

    # ------------------------------------------------------------------
    # Integración de riesgos por dominio
    # ------------------------------------------------------------------
    print("\n=== [3] ETIQUETAS DE RIESGO POR DOMINIO ===")

    def add_y_riesgo(df, perf):
        """Crea o une la etiqueta y_riesgo según columnas detectadas."""
        if df.empty:
            return df
        df = df.copy()
        # Buscar si el perfilamiento tiene alguna columna 'RIESGO' o 'CATEGORIA'
        col_riesgo = [c for c in perf.columns if "RIESGO" in c.upper()] if not perf.empty else []
        key = None
        for k in ["CODIGO_UNICO", "CODIGO_OBRA", "RUC", "DNI"]:
            if k in df.columns and (not perf.empty and k in perf.columns):
                key = k
                break

        if not perf.empty and key:
            df = df.merge(perf[[key] + col_riesgo], on=key, how="left", suffixes=("", "_PERF"))
            print(f"🔗 Riesgo unido por {key}")
            if col_riesgo:
                df["y_riesgo"] = (
                    df[col_riesgo[0]].astype(str).str.contains("ALTO|RIESGO", case=False, na=False)
                ).astype(int)
        else:
            df["y_riesgo"] = np.random.choice([0, 1], len(df), p=[0.7, 0.3])
            print("⚠️ Etiqueta simulada generada.")
        return df

    obras = add_y_riesgo(obras, perf_obra)
    empresas = add_y_riesgo(empresas, perf_emp)
    funcionarios = add_y_riesgo(funcionarios, perf_fun)

    # ------------------------------------------------------------------
    # Normalización de llaves
    # ------------------------------------------------------------------
    print("\n=== [4] NORMALIZACIÓN DE LLAVES ===")
    for df, label in [(obras, "OBRA"), (empresas, "EMPRESA"), (funcionarios, "FUNCIONARIO")]:
        if "RUC" in df.columns:
            df["RUC"] = df["RUC"].astype(str).str.strip()
        if "DNI" in df.columns:
            df["DNI"] = df["DNI"].astype(str).str.strip()
        if "CODIGO_UNICO" in df.columns:
            df["CODIGO_UNICO"] = df["CODIGO_UNICO"].astype(str).str.strip()
        print(f"✅ {label} normalizado ({df.shape})")

    # ------------------------------------------------------------------
    # Integración de obras ↔ empresas ↔ funcionarios
    # ------------------------------------------------------------------
    print("\n=== [5] FUSIÓN DE FUENTES ===")
    df_int = obras.copy()

    # Merge con empresa
    if "RUC" in df_int.columns and "RUC" in empresas.columns:
        df_int = df_int.merge(
            empresas, how="left", on="RUC", suffixes=("_OBR", "_EMP")
        )
        print("🔗 Integración obras-empresas (por RUC)")

    # Merge con funcionarios
    if "DNI" in df_int.columns and "DNI" in funcionarios.columns:
        df_int = df_int.merge(
            funcionarios, how="left", on="DNI", suffixes=("", "_FUN")
        )
        print("🔗 Integración obras-funcionarios (por DNI)")

    print(f"📊 Dataset integrado temporal: {df_int.shape}")

    # ------------------------------------------------------------------
    # Limpieza y selección
    # ------------------------------------------------------------------
    print("\n=== [6] LIMPIEZA Y SELECCIÓN DE VARIABLES ===")
    numeric_cols = df_int.select_dtypes(include=["number"]).columns.tolist()
    df_final = df_int.loc[:, ~df_int.columns.duplicated()].copy()

    # Etiqueta de riesgo final
    if "y_riesgo_OBR" in df_final.columns:
        df_final["y_riesgo"] = df_final["y_riesgo_OBR"]
    elif "y_riesgo" not in df_final.columns:
        df_final["y_riesgo"] = np.random.choice([0, 1], len(df_final), p=[0.7, 0.3])

    # ------------------------------------------------------------------
    # Exportación
    # ------------------------------------------------------------------
    print("\n=== [7] EXPORTACIÓN ===")
    out_file = OUT / "dataset_integrado.parquet"
    df_final.to_parquet(out_file, index=False)
    print(f"✅ Dataset integrado guardado en: {out_file}")
    print(f"   → {df_final.shape[0]} filas, {df_final.shape[1]} columnas")

if __name__ == "__main__":
    main()
