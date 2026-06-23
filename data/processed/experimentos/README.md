# `processed/experimentos/` — archivo de experimentos descartados

Este subdirectorio **no es input del pipeline oficial** (`notebooks/02_build_dataset_obra_v4.ipynb` → `08_modelo_final_obra_v4.ipynb`). Documenta un intento real de extender el modelo a una arquitectura multi-actor `OBRA + EMPRESA + FUNCIONARIO`, que se ejecutó y se descartó por bajo desempeño. Se conserva como registro del experimento, no como trabajo pendiente de retomar sin más.

## Qué hay aquí

- `dataset_empresa_v3_4niveles_*` / `dataset_funcionario_v3_4niveles_*` — datasets por entidad (empresa, funcionario) con riesgo *proxy* (no etiqueta oficial), construidos a partir de sanciones/inhabilitaciones/penalidades.
- `dataset_maestro_v2_4niveles.parquet` (324 obras × 93 cols, `dataset_maestro_v2_4niveles_meta.json`, generado 2026-05-01) — fusión de obra + empresa (agregada) + funcionario (agregado) por `IDENTIFICADOR_OBRA`/`CODIGO_OBRA`.
- `dataset_empresa_v4_features_por_obra.*` / `dataset_funcionario_v4_features_por_obra.*` — segunda iteración de features de empresa/funcionario agregadas por obra, marcada en su propia metadata como "no es dataset final de entrenamiento"; insumo preparado para un eventual maestro v3 que no se llegó a ejecutar.
- `baseline_*_metrics.json` — métricas de cada variante evaluada.

## Resultado y por qué se descartó

`baseline_maestro_4niveles_metrics.json` → **macro F1 = 0.226**, muy por debajo del baseline solo-obra (macro F1 ≈ 0.58–0.65, ver `models/obra_v4/`). Con solo 326 obras y el riesgo de empresa/funcionario siendo un proxy (no etiqueta oficial), sumar esas columnas sobre las mismas filas incrementó la varianza/sobreajuste en vez de aportar señal. Por eso el pipeline oficial (notebooks 02→08) trabaja únicamente con el dataset de obra.

## Si se retoma la integración multi-entidad

Partir de estos archivos y de las notas de `dataset_maestro_v2_4niveles_meta.json` (estrategia de join, llave puente `CODIGO_OBRA`↔`IDENTIFICADOR_OBRA`, columnas constantes eliminadas) en vez de reconstruir desde cero. El cuello de botella real es el tamaño muestral (326 obras), no la falta de columnas — más fuentes sobre las mismas filas no sustituye más filas.
