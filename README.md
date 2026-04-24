# 🧠 Detección de Riesgos de Corrupción en Obras Públicas

Sistema basado en Machine Learning para identificar riesgos potenciales de corrupción en proyectos de inversión pública en el Perú.

## 🎯 Objetivo

- Integrar múltiples fuentes de datos
- Construir variables relevantes
- Entrenar modelos predictivos
- Evaluar riesgos de corrupción
- Exponer resultados mediante una API

## ⚙️ Instalación

```bash
git clone https://github.com/webconceptos/Deteccion_Corrupcion.git
cd Deteccion_Corrupcion
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 🔐 Configuración

Crear archivo `.env` basado en `.env.example`

## 🤖 Entrenamiento

```bash
python src/models/train.py --input data/processed/dataset_modelado.parquet --target target_column
```

## 🚀 API

```bash
uvicorn src.api.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## 🧪 Tests

```bash
pytest -q
```

## 👤 Autor

Fernando García
