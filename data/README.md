# Data Directory — Sistema de Detección de Riesgos de Corrupción

Este directorio contiene los datos del sistema de detección de riesgos de corrupción en obras públicas del Perú.

---

# Arquitectura de datos (capas)

```
raw/ → external/ → interim/ → processed/
```

- **`raw/`** — `listado_completo_datasets.csv`: inventario de las fuentes originales (trazabilidad).
- **`external/`** — extractos crudos por dominio, descargados de dashboards institucionales (`DS_DASH_*.csv`):
  - `obra/` (8 archivos, o1a…o5a) — el único dominio que alimenta el pipeline de modelado actual.
  - `empresa/` y `funcionario/` (5 y 4 archivos) — usados solo en los experimentos archivados en `processed/experimentos/` (ver abajo), no en el dataset de producción.
- **`interim/`** — `oXX_clean.parquet`, uno por cada fuente de `external/obra/`, producido por `notebooks/00_eda_inicial.ipynb`.
- **`processed/`** — datasets listos para modelar:
  - `dataset_obra_v4_model.parquet` (326 obras × 77 features) — **dataset oficial**, construido por `notebooks/02_build_dataset_obra_v4.ipynb`. Es la única entrada real del pipeline de entrenamiento (notebooks 03 y 05→08).

---

# Unidad de análisis

**1 fila = 1 obra pública**, clave `IDENTIFICADOR_OBRA`.

# Target

`y_riesgo_obra` en el dataset original, 4 niveles (Sin Riesgo / Bajo / Medio / Alto-Extremo). El modelo final (ver `notebooks/07_var3_anticol_obra_v4.ipynb` y `08_modelo_final_obra_v4.ipynb`) fusiona las dos categorías de menor riesgo y trabaja con **3 clases**: Bajo Riesgo / Med-Alt Riesgosa / Extrem. Riesgosa.

---

# `processed/experimentos/` — intentos multi-entidad (archivados, no vigentes)

Documenta un intento real de extender el modelo a `OBRA + EMPRESA + FUNCIONARIO`, ejecutado y descartado por bajo desempeño (macro F1 = 0.226 vs. 0.58–0.65 del baseline solo-obra). Ver `processed/experimentos/README.md` para el detalle completo.

---

# Artefactos de modelo (no viven en `data/`, viven en `models/obra_v4/`)

- `pipeline_rf_obra_v4.pkl` — baseline tuneado de 4 clases (notebook 03).
- `pipeline_rf_obra_3clases_final.pkl` — modelo final de 3 clases (notebooks 07→08), el que la matriz de consistencia de la tesis (`docs/Matriz_consistencia_preliminar.docx`) declara como oficial. Su metadata de inferencia (features esperadas, etiquetas de clase, métricas) está en `pipeline_rf_obra_3clases_final_meta.json`, junto al `.pkl`.
