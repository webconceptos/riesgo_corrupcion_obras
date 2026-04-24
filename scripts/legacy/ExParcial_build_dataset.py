# ===============================================================
# Script: ExParcial_build_dataset.py
# Dataset final para el Examen Parcial
# Adaptado al dataset real
# Autor: Fernando García - Hilario Aradiel
# Fecha: 2025-11-12
# ===============================================================

import pandas as pd
import os

INPUT_PATH = "data/processed/dataset_integrado.parquet"
OUTPUT_PATH = "data/processed/dataset_parcial_features.parquet"

print("=== Construcción del Dataset del Examen Parcial ===")

if not os.path.exists(INPUT_PATH):
    raise FileNotFoundError(f"No se encontró el archivo base: {INPUT_PATH}")

df = pd.read_parquet(INPUT_PATH)

print(f"Registros cargados: {df.shape[0]} filas")
print(f"Columnas iniciales: {df.shape[1]} columnas")

# ===============================================================
# Selección de columnas reales del dataset
# ===============================================================

features_num = [
    "TIEMPO_ABSOLUCION_CONSULTAS",
    "TIEMPO_PRESENTACION_OFERTAS",
    "MONTO_CONTRACTUAL",
    "MONTO_REFERENCIAL",
    "MONTO_OFERTADO_PROMEDIO",
    "MONTO_OFERTADO",
    "TOTALPROCESOSPARTICIPANTES",
    "DIAS_PLAZO",
    "TOTAL_CONTROL_PREVIO",
    "TOTAL_CONTROL_SIMULTANEO",
    "TOTAL_CONTROL_POSTERIOR",
    "PLANIFICADO",
    "REAL",
    "IND_INTERVENSION",
    "IND_RESIDENTE",
    "IND_MONTO_ADELANTO_MATERIALES",
    "IND_MONTO_ADELANTO_DIRECTO",
]

features_cat = [
    "SECTOR",
    "DEPARTAMENTO",
    "NIVEL_GOBIERNO",
    "OBJETO_PROCESO",
    "METODO_CONTRATACION",
    "ESTADO_OBRA",
    "ETAPA",
    "ANHO",
    "MES"
]

all_cols = features_num + features_cat + ["y_riesgo"]

df_final = df[all_cols].copy()

# ===============================================================
# Exportar dataset final
# ===============================================================

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df_final.to_parquet(OUTPUT_PATH, index=False)

print(f"Dataset final generado en: {OUTPUT_PATH}")
print(f"Filas: {df_final.shape[0]}, Columnas: {df_final.shape[1]}")
print("=== FINALIZADO ===")
