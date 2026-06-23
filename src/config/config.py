import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = Path(os.getenv("DATASET_PATH", "data/processed/dataset_obra_v4_model.parquet"))
MODEL_PATH = Path(
    os.getenv("MODEL_PATH", "models/obra_v4/pipeline_rf_obra_3clases_final.pkl")
)
MODEL_META_PATH = Path(
    os.getenv("MODEL_META_PATH", "models/obra_v4/pipeline_rf_obra_3clases_final_meta.json")
)
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
