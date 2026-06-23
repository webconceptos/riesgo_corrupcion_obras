"""
Demo — Sistema de detección de riesgos de corrupción en obras públicas
==============================================================================
Inferencia REAL con el Random Forest de 3 clases entrenado (Sprint 2).

Ejecutar:
    pip install streamlit shap scikit-learn pandas numpy matplotlib joblib
    streamlit run demo_app.py

Coloca junto a este script:
  - pipeline_rf_obra_3clases_final.pkl   (modelo persistido)
  - el dataset de obras (parquet/csv) usado en NB08 (ajusta DATA_PATH abajo)

La app:
  1) carga el pipeline y el dataset,
  2) permite elegir una obra real (o ajustar manualmente sus señales),
  3) predice el nivel de riesgo y sus probabilidades,
  4) explica la predicción con TreeSHAP.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import joblib

MODEL_PATH = "models/obra_v4/pipeline_rf_obra_3clases_final.pkl"
# Rutas relativas a la raíz del repo (asume `streamlit run demo/demo_app.py` desde ahí).
DATA_CANDIDATES = [
    "data/processed/dataset_obra_v4_model.parquet",
    "dataset_obra_v4.parquet", "obra_v4.parquet", "dataset_obra.parquet",
    "dataset_obra_v4.csv", "obra_v4.csv",
]
TARGET_CANDIDATES = ["y_riesgo_obra", "nivel_riesgo", "target", "riesgo", "clase"]
CLASES = ["Bajo Riesgo", "Med/Alt Riesgosa", "Extrem. Riesgosa"]
COLORES = {"Bajo Riesgo": "#0E7C66", "Med/Alt Riesgosa": "#C77B19", "Extrem. Riesgosa": "#B23A48"}

st.set_page_config(page_title="Triaje de riesgo de corrupción en obras", layout="wide")


# ---------- carga ----------
@st.cache_resource
def load_model(path):
    return joblib.load(path)


@st.cache_data
def load_data():
    for c in DATA_CANDIDATES:
        if Path(c).exists():
            return (pd.read_parquet(c) if c.endswith("parquet") else pd.read_csv(c)), c
    return None, None


def get_feature_names(pipe):
    """Recupera los nombres de atributos esperados por el pipeline."""
    for attr in ("feature_names_in_",):
        if hasattr(pipe, attr):
            return list(getattr(pipe, attr))
    # pipeline -> primer paso suele ser el preprocesador/ColumnTransformer
    try:
        first = pipe[0] if hasattr(pipe, "__getitem__") else pipe.steps[0][1]
        if hasattr(first, "feature_names_in_"):
            return list(first.feature_names_in_)
    except Exception:
        pass
    return None


def split_estimator(pipe):
    """Devuelve (preprocesador_o_None, estimador_final)."""
    if hasattr(pipe, "steps"):
        steps = [s for _, s in pipe.steps]
        return (pipe[:-1] if len(steps) > 1 else None), steps[-1]
    return None, pipe


# ---------- UI ----------
st.markdown("##### Contraloría General de la República · Triaje con Machine Learning")
st.title("¿Qué tan riesgosa es esta obra?")
st.caption("Inferencia en vivo con el Random Forest de 3 clases (Macro F1 = 0.6469 · recall Extrema = 1.00 · n = 326).")

if not Path(MODEL_PATH).exists():
    st.error(f"No se encontró el modelo `{MODEL_PATH}`. Colócalo junto a este script.")
    st.stop()

pipe = load_model(MODEL_PATH)
df, data_file = load_data()
feat_names = get_feature_names(pipe)

if df is None:
    st.warning("No se encontró el dataset. Ajusta `DATA_CANDIDATES` en el script. "
               "Puedes seguir usando el modo manual si defines los atributos.")
if feat_names is None and df is not None:
    target = next((t for t in TARGET_CANDIDATES if t in df.columns), None)
    feat_names = [c for c in df.columns if c != target and df[c].dtype != object]

col_in, col_out = st.columns([1, 1.1], gap="large")

# ----- selección de obra -----
with col_in:
    st.subheader("Señales de la fase de Selección")
    X_row = None
    if df is not None and feat_names is not None:
        modo = st.radio("Fuente de datos", ["Elegir obra del dataset", "Ajuste manual"], horizontal=True)
        idcol = next((c for c in ["IDENTIFICADOR_OBRA", "id_obra", "obra_id"] if c in df.columns), None)

        if modo == "Elegir obra del dataset":
            if idcol:
                pick = st.selectbox("Obra", df[idcol].astype(str).tolist())
                X_row = df[df[idcol].astype(str) == pick][feat_names].head(1)
            else:
                i = st.number_input("Índice de fila", 0, len(df) - 1, 0, 1)
                X_row = df.iloc[[i]][feat_names]
            with st.expander("Ver atributos de la obra"):
                st.dataframe(X_row.T, use_container_width=True)
        else:
            st.caption("Ajusta los principales drivers; el resto toma la mediana del dataset.")
            base = df[feat_names].median(numeric_only=True)
            X_row = base.to_frame().T.copy()
            top = [f for f in feat_names if any(k in f.lower() for k in
                   ["repeticion", "procesos", "convocatorias", "participantes",
                    "control", "monto_contractual", "regional", "convenio"])][:8]
            for f in (top or feat_names[:8]):
                lo, hi = float(df[f].min()), float(df[f].max())
                X_row[f] = st.slider(f, lo, hi, float(base.get(f, lo)))
    else:
        st.info("Carga el dataset para habilitar la selección de obras.")

# ----- predicción + SHAP -----
with col_out:
    st.subheader("Resultado de la clasificación")
    if X_row is not None:
        proba = pipe.predict_proba(X_row)[0]
        idx = int(np.argmax(proba))
        lab = CLASES[idx] if idx < len(CLASES) else f"Clase {idx}"

        st.markdown(
            f"<div style='background:{COLORES.get(lab,'#eee')}22;border:1px solid {COLORES.get(lab,'#ccc')};"
            f"border-radius:12px;padding:14px 16px'>"
            f"<div style='font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:{COLORES.get(lab)}'>"
            f"Nivel de riesgo predicho</div>"
            f"<div style='font-size:30px;font-weight:800;color:{COLORES.get(lab)}'>{lab}</div>"
            f"<div style='font-weight:600;color:{COLORES.get(lab)}'>Probabilidad {proba[idx]*100:.0f}%</div></div>",
            unsafe_allow_html=True,
        )
        st.write("")
        for i, c in enumerate(CLASES[:len(proba)]):
            st.markdown(f"**{c}** — {proba[i]*100:.0f}%")
            st.progress(float(proba[i]))

        # ---- TreeSHAP ----
        st.subheader("¿Por qué? (TreeSHAP)")
        try:
            import shap
            import matplotlib.pyplot as plt
            pre, est = split_estimator(pipe)
            Xt = pre.transform(X_row) if pre is not None else X_row.values
            try:
                names = pre.get_feature_names_out()
            except Exception:
                names = feat_names
            explainer = shap.TreeExplainer(est)
            sv = explainer.shap_values(Xt)
            sv_cls = sv[idx] if isinstance(sv, list) else sv
            vals = np.array(sv_cls).reshape(-1)
            order = np.argsort(np.abs(vals))[::-1][:12]
            fig, ax = plt.subplots(figsize=(6, 4.2))
            colors = ["#B23A48" if vals[k] >= 0 else "#4F81BD" for k in order]
            ax.barh([str(names[k]) for k in order][::-1], [vals[k] for k in order][::-1], color=colors[::-1])
            ax.axvline(0, color="#999", lw=.8)
            ax.set_xlabel("Contribución SHAP a la clase predicha")
            ax.set_title(f"Top atributos — {lab}", fontsize=11)
            plt.tight_layout()
            st.pyplot(fig)
            st.caption("Rojo: empuja hacia la clase predicha · Azul: la aleja.")
        except ModuleNotFoundError:
            st.info("Instala `shap` para ver la explicación: `pip install shap`.")
        except Exception as e:
            st.warning(f"No se pudo calcular SHAP para esta entrada: {e}")
    else:
        st.info("Selecciona o define una obra para obtener la predicción.")

# ---------- desempeño ----------
st.divider()
st.subheader("Desempeño del modelo (test = 66)")
m = st.columns(5)
for c, (n, l) in zip(m, [("0.6469", "Macro F1"), ("0.6460", "Bal. Acc."),
                         ("1.00", "Recall Extrema"), ("0.1448", "Brier Extrema"),
                         ("0.297", "Gap train–val")]):
    c.metric(l, n)

st.caption(f"Modelo: `{MODEL_PATH}`" + (f" · datos: `{data_file}`" if data_file else "")
           + " · repo: github.com/webconceptos/riesgo_corrupcion_obras (rama Sprint2_Semana8)")
