"""
Script: app_predict.py
Autor: Fernando García - Hilario Aradiel
Objetivo: Aplicación Streamlit para predicción de riesgo en obras.
"""

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Detector de Riesgo de Corrupción", page_icon="🧠")

st.title("🧠 Sistema de Detección de Riesgo de Corrupción")
st.write("Sube un archivo CSV con datos de obras públicas para estimar su nivel de riesgo.")

pipe = joblib.load("models/pipeline.pkl")
file = st.file_uploader("📂 Cargar archivo CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    preds = pipe.predict_proba(df)[:, 1]
    df["Prob_Riesgo"] = preds
    df["Nivel_Riesgo"] = pd.cut(preds, bins=[0,0.33,0.66,1],
                                labels=["Bajo","Medio","Alto"])
    st.dataframe(df.head(10))
    st.download_button("⬇️ Descargar resultados", df.to_csv(index=False), file_name="predicciones_riesgo.csv")
