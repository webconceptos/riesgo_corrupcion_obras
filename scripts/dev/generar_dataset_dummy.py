# scripts/generar_dataset_dummy.py
import pandas as pd
import numpy as np
from pathlib import Path

# Dataset simulado con 300 registros
n = 300
df = pd.DataFrame({
    "monto_contrato": np.random.randint(100000, 5000000, n),
    "plazo_dias": np.random.randint(30, 900, n),
    "ampliaciones": np.random.randint(0, 5, n),
    "empresa_reincidente": np.random.choice([0, 1], n),
    "porcentaje_avance_devengado": np.random.uniform(0, 1, n),
    "departamento": np.random.choice(["LIMA","CUSCO","PIURA","LORETO","PUNO"], n),
    "tipo_obra": np.random.choice(["Carretera","Colegio","Hospital","Puente"], n),
    "y_riesgo": np.random.choice([0, 1], n, p=[0.7, 0.3])
})

path = Path("data/processed")
path.mkdir(parents=True, exist_ok=True)
df.to_parquet(path / "dataset_obras.parquet", index=False)

print("✅ Dataset de prueba generado en data/processed/dataset_obras.parquet")
print(df.head())
