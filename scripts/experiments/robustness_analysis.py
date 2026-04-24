"""
Evaluamos la robustez del modelo mediante remuestreo bootstrap.
"""
import numpy as np, pandas as pd, joblib
from sklearn.metrics import f1_score, roc_auc_score, average_precision_score
from sklearn.utils import resample
from pathlib import Path

pipe = joblib.load("models/pipeline.pkl")
df = pd.read_parquet("data/processed/dataset_integrado.parquet")
X, y = df.drop(columns=["y_riesgo"]), df["y_riesgo"]

N = 50
f1s, aucs, prs = [], [], []
for i in range(N):
    Xb, yb = resample(X, y, replace=True, random_state=i)
    prob = pipe.predict_proba(Xb)[:, 1]
    pred = (prob > 0.5).astype(int)
    f1s.append(f1_score(yb, pred))
    aucs.append(roc_auc_score(yb, prob))
    prs.append(average_precision_score(yb, prob))

df_rob = pd.DataFrame({"F1": f1s, "ROC-AUC": aucs, "PR-AUC": prs})
df_rob.to_csv("reports/robustness_metrics.csv", index=False)
print(df_rob.describe().T)
