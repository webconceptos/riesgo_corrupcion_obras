import argparse, json, os, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    f1_score, roc_auc_score, average_precision_score,
    precision_recall_curve, roc_curve
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
import joblib

# === Configuración general ===
DATA_PATH = Path("data/processed/dataset_integrado.parquet")
MODEL_DIR = Path("models"); MODEL_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR = Path("reports/figures"); FIG_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = Path("reports"); REPORTS_DIR.mkdir(parents=True, exist_ok=True)
TARGET = "y_riesgo"


# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



# === Importa preprocesador (ya incluye imputación) ===
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import inspect

def build_preprocessor(df):
    cat_cols = [c for c in df.columns if c != TARGET and df[c].dtype == "object"]
    num_cols = [c for c in df.columns if c != TARGET and c not in cat_cols]
    ohe_params = {"handle_unknown": "ignore"}
    if "sparse_output" in inspect.signature(OneHotEncoder).parameters:
        ohe_params["sparse_output"] = False
    else:
        ohe_params["sparse"] = False
    preproc = ColumnTransformer([
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler(with_mean=False))
        ]), num_cols),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(**ohe_params))
        ]), cat_cols)
    ])
    return preproc

def evaluate_model(pipe, X, y, folds=5):
    skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
    f1s, aucs, aps = [], [], []
    for tr, va in skf.split(X, y):
        pipe.fit(X.iloc[tr], y.iloc[tr])
        prob = pipe.predict_proba(X.iloc[va])[:, 1]
        pred = (prob >= 0.5).astype(int)
        f1s.append(f1_score(y.iloc[va], pred))
        aucs.append(roc_auc_score(y.iloc[va], prob))
        aps.append(average_precision_score(y.iloc[va], prob))
    return np.mean(f1s), np.mean(aucs), np.mean(aps)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--with-mlp", action="store_true")
    args = parser.parse_args()

    print("\n=== [1] CARGA DE DATOS ===")
    df = pd.read_parquet(DATA_PATH)
    print(f"Dataset: {df.shape[0]} filas, {df.shape[1]} columnas")
    y = df[TARGET].astype(int)
    X = df.drop(columns=[TARGET])

    preproc = build_preprocessor(df)

    # === Modelos ===
    models = {
        "logreg": LogisticRegression(max_iter=1000, class_weight="balanced", solver="lbfgs"),
        "rf": RandomForestClassifier(
            n_estimators=200, random_state=42, n_jobs=-1, class_weight="balanced_subsample"),
        "xgb": XGBClassifier(
            n_estimators=300, learning_rate=0.1, max_depth=6, subsample=0.9,
            colsample_bytree=0.9, reg_lambda=1.0, eval_metric="logloss",
            n_jobs=-1, tree_method="hist", random_state=42)
    }
    if args.with_mlp:
        models["mlp"] = MLPClassifier(hidden_layer_sizes=(64, 32), activation="relu", max_iter=300)

    results = []
    start_total = time.time()

    print("\n=== [2] ENTRENAMIENTO CRUZADO ===")
    for name, model in models.items():
        start = time.time()
        pipe = Pipeline([("prep", preproc), ("clf", model)])
        f1m, aucm, apm = evaluate_model(pipe, X, y, folds=args.folds)
        elapsed = time.time() - start
        print(f"✅ {name:7s} → F1={f1m:.3f} | ROC_AUC={aucm:.3f} | PR_AUC={apm:.3f} | Tiempo={elapsed:.1f}s")
        results.append({
            "modelo": name, "f1": f1m, "roc_auc": aucm, "pr_auc": apm,
            "tiempo_seg": elapsed, "folds": args.folds
        })

    # === [3] Comparativo y guardado ===
    df_metrics = pd.DataFrame(results)
    df_metrics["fecha"] = pd.Timestamp.now()
    out_metrics = REPORTS_DIR / "metrics_semana6.csv"

    if out_metrics.exists():
        prev = pd.read_csv(out_metrics)
        df_metrics = pd.concat([prev, df_metrics], ignore_index=True)
    df_metrics.to_csv(out_metrics, index=False)
    print(f"\n📊 Resultados guardados en {out_metrics} ({len(df_metrics)} registros totales)")

    # === [4] Selección y guardado del mejor modelo ===
    best = max(results, key=lambda d: d["f1"])
    best_name = best["modelo"]
    best_clf = models[best_name]

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    best_pipe = Pipeline([("prep", preproc), ("clf", best_clf)])
    best_pipe.fit(Xtr, ytr)
    joblib.dump(best_pipe, MODEL_DIR / "pipeline.pkl")
    json.dump(best, open(MODEL_DIR / "pipeline_meta.json", "w"), indent=2)
    print(f"🏆 Mejor modelo: {best_name.upper()} (F1={best['f1']:.3f})")
    print(f"📁 Artefactos guardados en: {MODEL_DIR}")

    print(f"\n⏱ Tiempo total: {time.time() - start_total:.1f}s")

if __name__ == "__main__":
    main()