"""
07_locust_loadtest.py
---------------------
Script del Sprint 4 que define una prueba de carga usando LOCUST.

Permite enviar múltiples peticiones a la API de inferencia
(ej. FastAPI -> /predict), midiendo:

- tiempos de respuesta (latencia real de API)
- throughput (requests per second)
- estabilidad bajo carga
- errores en inferencia

Este script se integra con tu backend real del repositorio.

Uso:

locust -f scripts/Sprint4/07_locust_loadtest.py --host=http://localhost:8000 ^
    --data-csv data/processed/dataset_modelado.csv

Luego abre:
http://localhost:8089
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import List, Dict

import pandas as pd
from locust import HttpUser, between, task, events

# =============================================================
# Cargar datos de prueba para enviar como JSON a la API
# =============================================================

DATA_CACHE: List[Dict] | None = None


def load_samples(csv_path: str, max_samples: int = 1000) -> List[Dict]:
    """
    Carga ejemplos del dataset para generar payloads realistas.
    """
    global DATA_CACHE
    if DATA_CACHE is not None:
        return DATA_CACHE

    df = pd.read_csv(csv_path)

    # Tomar solo algunos para no sobrecargar la memoria
    if len(df) > max_samples:
        df = df.sample(max_samples, random_state=42)

    # Convertir a dict (uno por fila)
    DATA_CACHE = df.to_dict(orient="records")

    return DATA_CACHE


# =============================================================
# Clase de comportamiento del usuario LOCUST
# =============================================================

class PredictUser(HttpUser):
    """
    Simula un usuario que llama a /predict en tu API.

    Cada usuario:
    - Espera entre 0.1 y 1 segundo entre llamadas.
    - Toma un registro aleatorio del CSV.
    - Dispara un POST a /predict.
    """

    wait_time = between(0.1, 1.0)

    def on_start(self):
        csv_path = self.environment.parsed_options.data_csv
        self.samples = load_samples(csv_path)

    @task
    def predict(self):
        if not self.samples:
            return

        row = random.choice(self.samples)
        payload = {"features": row}

        with self.client.post(
            "/predict",
            json=payload,
            name="predict",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Error {response.status_code}")
            else:
                response.success()


# =============================================================
# Hook para recibir parámetros desde CLI
# =============================================================

def on_locust_init(environment, **_kwargs):
    """
    Inyecta parámetros CLI personalizados.
    """
    parser = environment.parsed_options


# Registrar opción CLI
def add_locust_options(parser):
    parser.add_argument(
        "--data-csv",
        required=True,
        help="Dataset CSV que se usará para generar payloads /predict."
    )


# Registrar
events.init.add_listener(on_locust_init)
events.init_command_line_parser.add_listener(add_locust_options)

