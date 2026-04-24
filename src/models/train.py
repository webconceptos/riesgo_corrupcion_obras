import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


SUPPORTED_MODELS = ["rf", "xgb", "lgbm"]
RANDOM_STATE = 42


def get_model(kind: str):
    if kind == "rf":
        return RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    if kind == "xgb":
        return XGBClassifier(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )

    if kind == "lgbm":
        return LGBMClassifier(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=-1,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    raise ValueError(f"Modelo no soportado: {kind}")


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el dataset: {path}")

    if path.suffix == ".parquet":
        return pd.read_parquet(path)

    if path.suffix == ".csv":
        return pd.read_csv(path)

    raise ValueError("Formato no soportado. Usa .csv o .parquet")


def main():
    parser = argparse.ArgumentParser(
        description="Entrenamiento del modelo baseline de riesgo de corrupción."
    )
    parser.add_argument("--input", required=True, help="Ruta al dataset (.csv o .parquet)")
    parser.add_argument("--target", required=True, help="Nombre de la columna objetivo")
    parser.add_argument("--model", default="rf", choices=SUPPORTED_MODELS)
    parser.add_argument("--out", default="models/production/pipeline.pkl")
    parser.add_argument("--meta-out", default="models/production/pipeline_meta.json")
    args = parser.parse_args()

    input_path = Path(args.input)
    model_path = Path(args.out)
    meta_path = Path(args.meta_out)

    df = load_dataset(input_path)

    if args.target not in df.columns:
        raise ValueError(f"La columna target '{args.target}' no existe en el dataset.")

    y = df[args.target].astype(int)
    X = df.drop(columns=[args.target])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    model = get_model(args.model)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1] # type: ignore
        roc_auc = roc_auc_score(y_test, y_proba)
    else:
        y_proba = None
        roc_auc = None

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc,
    }

    print(classification_report(y_test, y_pred, digits=4))
    print("Métricas:", metrics)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)

    metadata = {
        "model_type": args.model,
        "model_path": str(model_path),
        "target": args.target,
        "features": list(X.columns),
        "threshold": 0.5,
        "random_state": RANDOM_STATE,
        "test_size": 0.2,
        "metrics": metrics,
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"Modelo guardado en: {model_path}")
    print(f"Metadata guardada en: {meta_path}")


if __name__ == "__main__":
    main()