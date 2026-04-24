import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib

# Directorios
os.makedirs("reports/graficos", exist_ok=True)
os.makedirs("reports/tablas",   exist_ok=True)

# -------------------------------------------------------
# 1. Resultados de modelos
# -------------------------------------------------------
df = pd.read_csv("reports/tablas/resultados_modelos_parcial.csv")

plt.figure(figsize=(6,4))
sns.barplot(data=df, x="modelo", y="f1")
plt.title("F1 por modelo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/graficos/experimentos_f1.png")
plt.close()

plt.figure(figsize=(6,4))
sns.barplot(data=df, x="modelo", y="recall")
plt.title("Recall por modelo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/graficos/experimentos_recall.png")
plt.close()

plt.figure(figsize=(6,4))
sns.barplot(data=df, x="modelo", y="roc_auc")
plt.title("ROC-AUC por modelo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/graficos/experimentos_rocauc.png")
plt.close()

# -------------------------------------------------------
# 2. Ablation Study
# -------------------------------------------------------
df_ab = pd.read_csv("reports/tablas/ablation_results.csv")

plt.figure(figsize=(6,4))
sns.barplot(data=df_ab, x="config", y="f1_mean")
plt.title("Ablation - F1 por configuracion")
plt.tight_layout()
plt.savefig("reports/graficos/ablation_f1.png")
plt.close()

plt.figure(figsize=(6,4))
sns.barplot(data=df_ab, x="config", y="recall_mean")
plt.title("Ablation - Recall por configuracion")
plt.tight_layout()
plt.savefig("reports/graficos/ablation_recall.png")
plt.close()

plt.figure(figsize=(6,4))
sns.barplot(data=df_ab, x="config", y="roc_auc_mean")
plt.title("Ablation - ROC-AUC por configuracion")
plt.tight_layout()
plt.savefig("reports/graficos/ablation_rocauc.png")
plt.close()

# -------------------------------------------------------
# 3. XAI - SHAP
# -------------------------------------------------------
df_data = pd.read_parquet("data/processed/dataset_parcial_features.parquet")

num = [
    "TIEMPO_ABSOLUCION_CONSULTAS", "TIEMPO_PRESENTACION_OFERTAS",
    "MONTO_CONTRACTUAL","MONTO_REFERENCIAL","MONTO_OFERTADO_PROMEDIO",
    "MONTO_OFERTADO","TOTALPROCESOSPARTICIPANTES","DIAS_PLAZO",
    "TOTAL_CONTROL_PREVIO","TOTAL_CONTROL_SIMULTANEO","TOTAL_CONTROL_POSTERIOR",
    "PLANIFICADO","REAL","ANHO","MES"
]

cat = [
    "SECTOR","DEPARTAMENTO","NIVEL_GOBIERNO","OBJETO_PROCESO",
    "METODO_CONTRATACION","ESTADO_OBRA","ETAPA",
    "IND_INTERVENSION","IND_RESIDENTE","IND_MONTO_ADELANTO_MATERIALES",
    "IND_MONTO_ADELANTO_DIRECTO"
]

X = df_data[num + cat]
y = df_data["y_riesgo"]

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

num_pipe = Pipeline([
    ("imp", SimpleImputer(strategy="constant", fill_value=0)),
    ("sc", StandardScaler())
])

cat_pipe = Pipeline([
    ("imp", SimpleImputer(strategy="most_frequent")),
    ("ohe", OneHotEncoder(handle_unknown="ignore"))
])

pre = ColumnTransformer([
    ("num", num_pipe, num),
    ("cat", cat_pipe, cat)
])

model = RandomForestClassifier(
    n_estimators=300,
    n_jobs=-1,
    random_state=42,
    class_weight="balanced"
)

pipe = Pipeline([
    ("pre", pre),
    ("model", model)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

pipe.fit(X_train, y_train)

X_train_t = pipe.named_steps["pre"].transform(X_train)
if hasattr(X_train_t, "toarray"):
    X_train_t = X_train_t.toarray()

explainer = shap.TreeExplainer(pipe.named_steps["model"])
shap_vals = explainer.shap_values(X_train_t)

shap.summary_plot(shap_vals[1], show=False)
plt.savefig("reports/graficos/xai_shap_summary.png", bbox_inches="tight")
plt.close()

shap.summary_plot(shap_vals[1], plot_type="bar", show=False)
plt.savefig("reports/graficos/xai_shap_bar.png", bbox_inches="tight")
plt.close()

# Top 20 SHAP CSV
sh = pd.DataFrame({
    "feature": pre.get_feature_names_out(),
    "importance": abs(shap_vals[1]).mean(axis=0)
}).sort_values("importance", ascending=False).head(20)

sh.to_csv("reports/tablas/importancia_variables_shap_top20.csv", index=False)

# -------------------------------------------------------
# 4. EDA Profesional
# -------------------------------------------------------

plt.figure(figsize=(5,4))
sns.countplot(data=df_data, x="y_riesgo")
plt.title("Distribucion de y_riesgo")
plt.savefig("reports/graficos/eda_y_riesgo.png")
plt.close()

desc = df_data.describe(include="all")
desc.to_csv("reports/tablas/estadisticos_descriptivos.csv")

print("Evidencias generadas correctamente.")
