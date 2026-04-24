"""
Evaluación del pipeline entrenado sobre un conjunto de prueba.
"""
import argparse, json
from pathlib import Path
import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix

MODEL_DIR = Path("models")
DATA_PATH = Path("data/processed/dataset_obras.parquet")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-file", type=str, default=str(DATA_PATH))
    args = parser.parse_args()

    model_file = MODEL_DIR / "pipeline.pkl"
    meta_file = MODEL_DIR / "pipeline_meta.json"
    pipe = joblib.load(model_file)
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    target = "y_riesgo"

    df = pd.read_parquet(args.test_file)
    y = df[target].astype(int)
    X = df.drop(columns=[target])

    ypred = pipe.predict(X)
    print("== Reporte de Clasificación ==")
    print(classification_report(y, ypred, digits=4))
    print("\n== Matriz de Confusión ==")
    print(confusion_matrix(y, ypred))
    print("\n== Metadatos ==")
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
