import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = Path(os.getenv("DATASET_PATH", "data/processed/dataset_modelado.parquet"))
MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/production/pipeline.pkl"))
MODEL_META_PATH = Path(os.getenv("MODEL_META_PATH", "models/production/pipeline_meta.json"))
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
