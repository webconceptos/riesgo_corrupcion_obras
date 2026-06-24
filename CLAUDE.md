# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexto del proyecto

Este es un repositorio de investigación de tesis de Maestría (Maestría en Inteligencia Artificial, UNI-FIIS, Perú) que construye un sistema de ML para detectar y priorizar el riesgo de corrupción en obras públicas del Perú. El repo combina experimentación dirigida por Jupyter notebooks con una API FastAPI ligera para servir el modelo. La mayor parte del trabajo "real" — construcción de datasets, feature engineering, selección de modelo — ocurre en `notebooks/`, no en `src/`. `src/` es solo la capa de serving (`api/` + `config/`); no contiene lógica de feature engineering ni de entrenamiento del modelo de producción, esos viven en los notebooks.

`apps/frontend/` es un dashboard React/Vite/Tailwind reconstruido el 2026-06-23 (el anterior, abandonado desde el primer sprint con endpoints incompatibles, se había eliminado el 2026-06-22) — este sí consume la API real (`/obras`, `/predict_proba`, `/explain`, `/predict_batch`, `/model_meta`), verificado end-to-end en navegador (Playwright headless: las 4 pestañas renderizan, predicen y no arrojan errores de consola). `demo/demo_app.py` (Streamlit) sigue siendo la alternativa sin red (carga el `.pkl` directo, sin pasar por la API) — útil como respaldo si la API no está disponible el día de la sustentación.

El español es el idioma de trabajo en todo el repo: nombres de variables, docstrings, mensajes de commit y prosa de los notebooks son mayoritariamente en español. Sigue esa convención al añadir código o documentación aquí.

`docs/Matriz_consistencia_preliminar.docx` es el documento de referencia metodológica de la tesis (hipótesis general H1-H3, objetivos específicos OE1-OE3, indicadores e variables de control). Define el modelo "oficial" actual como el **Random Forest anti-colinealidad de 3 clases** con Macro F1 = 0.6469, Balanced Accuracy = 0.6460, Recall Extrema = 1.00, Brier Extrema = 0.1448, gap train-val = 0.2971 — cifras que coinciden exactamente con el log de NB08 (`logs/metrics_experimentos.csv`). También define un plan de validación fuera de muestra (holdout temporal externo, holdout por grupo/región, backtesting por ventanas, robustez sintética con missingness/ruido/reescala) que **todavía no está implementado en código**; es el siguiente trabajo pendiente de la tesis, no algo ya construido en `src/` o `notebooks/`.

## Comandos comunes

Backend (ejecutar desde la raíz del repo, Python 3.11, venv en `.venv/`):
```bash
make install   # pip install -r requirements.txt (+ requirements-dev.txt si existe)
make lint      # ruff check .
make fmt       # ruff format .
make test      # PYTHONPATH=. pytest -q
make serve     # uvicorn src.api.main:app --reload --port 8000
```

Ejecutar un solo test:
```bash
PYTHONPATH=. pytest -q tests/test_api.py::test_predict_shape_ok
```

No hay script de entrenamiento en `src/` (ver limpieza 2026-06-22 más abajo) — el entrenamiento del modelo vive enteramente en los notebooks.

Demo (Streamlit, independiente — única UI funcional hoy):
```bash
streamlit run demo/demo_app.py
```

## Arquitectura

**Pipeline experimental (`notebooks/`, fuente de verdad para el trabajo de modelado):**
```
00_eda_inicial → 02_build_dataset_obra_v4 → 03_train_obra_v4 →
04_generate_reports_obra_v4(/v5) → 05_ab_experiments_obra_v4 →
06_shap_calibration_obra_v4 → 07_var3_anticol_obra_v4 → 08_modelo_final_obra_v4
```
- Unidad de análisis: **1 fila = 1 obra pública**, clave `IDENTIFICADOR_OBRA` (decisión D3 de `00_eda_inicial.ipynb`).
- Dataset de entrada al modelado: `data/processed/dataset_obra_v4_model.parquet` (326 obs × 77 features), construido en `02_build_dataset_obra_v4.ipynb` a partir de 8 fuentes crudas (`o1a`…`o5a`, cada una limpiada primero a `data/interim/oXX_clean.parquet` por `00_eda_inicial.ipynb`).
- Target original: `y_riesgo_obra`, 4 niveles (Sin Riesgo / Bajamente Riesgosa / Med/Alt Riesgosa / Extrem. Riesgosa). El pipeline experimental (notebooks 05→07) evolucionó este baseline:
  - `03_train_obra_v4.ipynb` entrena y exporta el baseline de 4 clases tuneado → `models/obra_v4/pipeline_rf_obra_v4.pkl` + `metrics_rf_obra_v4.json` (macro F1 ≈ 0.58). Este es el único artefacto de modelo realmente presente en el repo.
  - `07_var3_anticol_obra_v4.ipynb` prueba eliminar features colineales (77→61, VIF/correlación), SMOTE, y finalmente **fusionar a 3 clases** (Bajo / Med-Alt / Extrem. Riesgosa) — variante "Var5", adoptada explícitamente en el log de experimentos con macro F1 = 0.6469.
  - `08_modelo_final_obra_v4.ipynb` entrena ese modelo de 3 clases definitivo, corre SHAP/curvas de aprendizaje/calibración, y guarda (`joblib.dump`) en `MODEL_DIR = BASE_DIR / 'models' / 'obra_v4'` → `models/obra_v4/pipeline_rf_obra_3clases_final.pkl`. Esta ruta ya coincide con la que espera `demo/demo_app.py:27`; el artefacto fue regenerado el 2026-06-22 (métricas reproducidas idénticas al log original: macro F1 = 0.6469, seed=42) y ambos quedaron consistentes — ya no hace falta mover el archivo a mano tras reejecutar el notebook.
- `data/` está organizado en capas: `raw/` (inventario de fuentes) → `external/` (extractos crudos por dominio: `obra/`, `empresa/`, `funcionario/`) → `interim/` (parquet limpios, solo para el dominio obra) → `processed/` (datasets finales). Ver `data/README.md` (reescrito 2026-06-22, refleja el estado real) para el detalle completo. Dentro de `processed/experimentos/` (con su propio `README.md`) hay un intento real y completo de arquitectura multi-entidad: `dataset_maestro_v2_4niveles.parquet` (324×93, fusión de obra+empresa+funcionario agregados, generado 2026-05-01) fue entrenado y evaluado (`baseline_maestro_4niveles_metrics.json` → macro F1 = 0.226, muy por debajo del baseline solo-obra) y por eso **se descartó**, no porque falte construir.
- Limpieza 2026-06-22: se eliminaron `data/external/priorizacion/` (huérfano, sin ninguna referencia en notebooks/scripts) y `data/processed/dataset_obra_v4_model_old.parquet` (no era un duplicado trivial — su target `y_riesgo_obra` difería en 155/326 filas respecto al oficial y ningún notebook explicaba su origen; se confirmó con el usuario antes de borrar).

**Capa de serving (`src/`):**
- `src/config/config.py` lee `DATASET_PATH`, `MODEL_PATH`, `MODEL_META_PATH` desde variables de entorno (`.env`, ver `.env.example`). Los defaults apuntan al modelo oficial de 3 clases: `models/obra_v4/pipeline_rf_obra_3clases_final.pkl` + `models/obra_v4/pipeline_rf_obra_3clases_final_meta.json` (este último generado a mano a partir de `pipe.feature_names_in_` y las métricas del log de NB08 — el notebook no exporta meta JSON, solo el `.pkl` y una fila en `logs/metrics_experimentos.csv`; si se reentrena, regenerar el meta).
- `src/api/deps.py::get_model_and_meta()` carga de forma perezosa y cachea (`lru_cache`) el pipeline joblib + el JSON de metadata. Llamar a `clear_model_cache()` después de reemplazar el archivo del modelo o en tests que mockeen el modelo (necesario porque, al ser singleton de proceso, una llamada real previa deja cacheado el pipeline real y un monkeypatch posterior no lo reemplaza).
- `src/api/main.py` expone `POST /predict_proba` y `POST /predict_batch`, ambos con el mismo contrato multi-clase: devuelven `probabilidades` (dict clase→prob), `clase_predicha` (índice argmax), `clase_predicha_label` y `riesgoso` (`True` si la clase predicha no es la de menor riesgo, índice 0). **Importante:** este endpoint asume que `meta["class_labels"]` existe y está alineado con el orden de columnas que produce `pipeline.predict_proba()` — si se sirve un modelo distinto, su meta JSON debe traer esa clave o la API devuelve 500. `src/api/routes/health.py` añade `GET /health` y `GET /model_meta`.
- Los payloads de inferencia se alinean por nombre a las columnas que espera el modelo (`meta["features"]` o `meta["columns"]`); los campos faltantes se rellenan con `None`, los campos extra se descartan. `BatchPredictRequest` usa `extra="allow"` en el modelo pydantic, pero cada fila se realinea igualmente a la lista de columnas de la metadata.
- En `main.py` el módulo `deps` se importa como `from src.api import deps` y se llama `deps.get_model_and_meta()` (no `from ... import get_model_and_meta`) — necesario para que `monkeypatch.setattr(deps, "get_model_and_meta", ...)` en los tests funcione; con un import directo del nombre, el monkeypatch no intercepta la llamada porque el módulo `main` ya tiene su propia referencia vinculada al objeto original.
- Limpieza 2026-06-22: se eliminaron `src/data/ingest.py`, `src/features/engineering.py`, `src/utils/logging.py`, `src/main.py` y `src/models/train.py` (este último: CLI binario genérico, incompatible con el modelo real multi-clase, sin imports reales en todo el repo salvo el target `train:` del Makefile, que también se eliminó). `src/` ahora solo contiene `api/` y `config/` — exclusivamente la capa de serving, sin nada de entrenamiento ni feature engineering.
- También se eliminaron de la raíz `tmp_data_summary.py`/`tmp_inspect_dataset.py` (scripts de exploración descartables que referenciaban datasets de antes del pivote a obra_v4, ya inexistentes), `requirements-lock.txt` (no usado por ningún comando del repo y corrupto en UTF-16) y `docs/~$forme_ExParcial_FGARCIA.docx` (archivo de bloqueo temporal de Word, no contenido real).

**Demo (`demo/demo_app.py`):** app Streamlit independiente para inferencia en vivo + explicaciones TreeSHAP, usada en presentaciones. Se ejecuta con `streamlit run demo/demo_app.py` desde la raíz del repo (sus rutas son relativas a la raíz, no al archivo). `MODEL_PATH` apunta a `models/obra_v4/pipeline_rf_obra_3clases_final.pkl` y `DATA_CANDIDATES` incluye `data/processed/dataset_obra_v4_model.parquet` como primera opción — verificado end-to-end (`pipe.feature_names_in_` con las 61 columnas tras anti-colinealidad, todas presentes en el dataset, `predict_proba` funcional). Es independiente del servicio FastAPI.

**Dashboard (`apps/frontend/`):** React 18 + Vite + Tailwind + recharts + lucide-react + papaparse. Arranca con `npm install && npm run dev` (puerto 5173/5174 según disponibilidad) leyendo `VITE_API_BASE` de `.env` (default `http://localhost:8000`; en Windows usar `127.0.0.1` o `localhost` según a cuál de las dos se haya bindeado `uvicorn`/`vite` — en este entorno `uvicorn` solo escucha en IPv4 y `vite` solo en IPv6, así que `localhost` y `127.0.0.1` **no son intercambiables** entre los dos servicios). Cuatro pestañas, todas contra la API real:
- **Explorar obra** (`ObraExplorer.jsx`): trae las 326 obras vía `GET /obras`, al seleccionar una pide su fila completa (`GET /obras/{id}`) y predice + explica (`POST /predict_proba` + `POST /explain`).
- **Modo manual** (`ManualWhatIf.jsx`): sliders sobre ~8 features clave (mismo criterio por palabra clave que `demo_app.py`), resto de las variables numéricas en su mediana — vía `feature_stats` (median/min/max) que ahora expone `GET /model_meta`.
- **Carga CSV** (`BatchUpload.jsx`): parsea con PapaParse, llama `POST /predict_batch`, permite descargar el CSV original + columnas de predicción.
- **Panel de métricas** (`ModelMetricsPanel.jsx`): Macro F1/Bal. Acc/Recall Extrema/Brier desde `GET /model_meta`, visible siempre arriba.

`RiskResultCard.jsx` y `ShapChart.jsx` (recharts) son compartidos entre Explorar/Manual. El backend se extendió para esto (ver abajo): `src/api/routes/obras.py`, `src/api/explain.py`, `POST /explain`, y `deps.get_dataset()`/`get_feature_stats()`.

## Docker (despliegue, arreglado 2026-06-23)

`Dockerfile.prod` ya estaba bien armado (gunicorn+uvicorn sirviendo `src.api.main:app`); lo que estaba roto era `docker-compose.dev.yml`, que apuntaba a una estructura de otro template (`./backend`, `./frontend`, módulo `api:app`, `MODEL_PATH=/app/artifacts/model.joblib`) que nunca coincidió con este repo. Se corrigió y se completó la historia de despliegue:

- **`.dockerignore`** (no existía): excluye `.venv/`, `data/`, `models/`, `notebooks/`, `node_modules/` del build context — `data/`/`models/` se montan como volumen en prod, no hace falta ni conviene copiarlos a la imagen.
- **`docker-compose.dev.yml`**: `api` corre `uvicorn --reload` montando todo el repo (`.:/app`); `web` corre `npm run dev` montando `apps/frontend`. Dos gotchas reales que se corrigieron: (1) `VITE_API_BASE` debe ser `http://localhost:8000`, no `http://api:8000` — el navegador corre en el host, no dentro de la red de Docker, así que el nombre de servicio no le resuelve; (2) `web` necesita un volumen anónimo extra en `/app/node_modules` para que el contenedor instale su propio `node_modules` Linux en vez de heredar el de Windows del host vía bind mount (binarios nativos como `esbuild` no son intercambiables entre SO).
- **`apps/frontend/Dockerfile`** (nuevo, multi-stage): build con `node:20-slim` (`npm ci && npm run build`) → sirve con `nginx:1.27-alpine`. Se usa nginx y no `vite preview` porque Vite documenta explícitamente que `preview` no está pensado para producción. `VITE_API_BASE` se pasa como build-arg porque las variables de Vite se hornean en tiempo de compilación, no de runtime — para apuntar a otra URL de API hay que reconstruir la imagen, no alcanza con cambiar una variable de entorno del contenedor ya construido.
- **`docker-compose.prod.yml`**: se agregó el servicio `web` (build de `apps/frontend/Dockerfile`, puerto 8080).
- **Sin verificar con build real**: el daemon de Docker Desktop no estaba corriendo en esta máquina durante el desarrollo; solo se validó con `docker compose -f docker-compose.dev.yml config` / `docker compose -f docker-compose.prod.yml config` (sintaxis e interpolación correctas). Falta correr `docker compose -f docker-compose.dev.yml up --build` con el daemon activo para confirmar que arma y arranca de verdad.

## Estado de la API (actualizado 2026-06-23)

La API ya sirve por defecto el modelo oficial de 3 clases y su contrato de respuesta es multi-clase (`probabilidades`/`clase_predicha`/`clase_predicha_label`/`riesgoso`), no binario. `make serve` + `make test` funcionan de punta a punta sin configurar nada adicional. `models/obra_v4/pipeline_rf_obra_v4.pkl` (el baseline de 4 clases de NB03) sigue en el repo pero no es lo que sirve la API por defecto — **no es compatible** con el meta JSON actual (espera 77 features, no 61, y no tiene `class_labels` de 3 niveles); si se quiere servir ese modelo en su lugar, hay que generarle su propio meta JSON con `class_labels` de 4 niveles y apuntar `MODEL_PATH`/`MODEL_META_PATH` a él.

Endpoints completos: `GET /health`, `GET /model_meta` (incluye `feature_stats`: median/min/max por feature numérica, usado por el dashboard), `GET /obras`, `GET /obras/{identificador_obra}`, `POST /predict_proba`, `POST /predict_batch`, `POST /explain` (SHAP vía `src/api/explain.py`, con el `TreeExplainer` cacheado por `lru_cache` — construirlo desde cero por request sería notablemente más lento dado que el RF tiene 300 árboles).

## Inconsistencias conocidas (no "arreglar" en silencio — confirmar con el usuario primero)

- `docs/Matriz_consistencia_preliminar.docx` define un plan de validación fuera de muestra (externo temporal, por grupo, backtesting, robustez sintética) que no tiene ninguna implementación todavía en `notebooks/` ni `src/`; es trabajo pendiente, no algo que se pueda asumir ya construido.
- No hay ningún script de reentrenamiento en `src/` — si se necesita reentrenar el modelo de producción, hay que hacerlo desde `notebooks/08_modelo_final_obra_v4.ipynb` (que ya guarda en la ruta correcta, `models/obra_v4/`) y regenerar a mano el meta JSON.
- El meta JSON del modelo de 3 clases (`models/obra_v4/pipeline_rf_obra_3clases_final_meta.json`) se generó a mano, no lo exporta el notebook 08. Si se reentrena el modelo y cambian las features o las métricas, hay que regenerar este archivo (o editarlo) — no se actualiza solo.
