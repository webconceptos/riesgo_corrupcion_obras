"""
Curvas PR y ROC del modelo final.
"""
import argparse, json
from pathlib import Path
import pandas as pd, joblib, matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, roc_curve, average_precision_score, roc_auc_score

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/processed/dataset_obras.parquet")
    args = ap.parse_args()

    model = joblib.load("models/pipeline.pkl")
    meta = json.loads(Path("models/pipeline_meta.json").read_text())
    df = pd.read_parquet(args.data)
    y = df["y_riesgo"].astype(int)
    X = df.drop(columns=["y_riesgo"])
    prob = model.predict_proba(X)[:,1]
    prec, rec, _ = precision_recall_curve(y, prob)
    fpr, tpr, _ = roc_curve(y, prob)

    plt.figure(); plt.plot(rec, prec)
    plt.xlabel("Recall"); plt.ylabel("Precision")
    plt.title(f"PR (AP={average_precision_score(y, prob):.3f})")
    plt.tight_layout(); plt.savefig("reports/figures/sem6_best_pr.png", dpi=150)

    plt.figure(); plt.plot(fpr, tpr)
    plt.xlabel("FPR"); plt.ylabel("TPR")
    plt.title(f"ROC (AUC={roc_auc_score(y, prob):.3f})")
    plt.tight_layout(); plt.savefig("reports/figures/sem6_best_roc.png", dpi=150)
    print("Curvas guardadas en reports/figures/")

if __name__ == "__main__":
    main()
