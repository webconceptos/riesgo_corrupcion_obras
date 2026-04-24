# 🏛️ Proyecto: Sistema de Detección de Riesgos de Corrupción en Obras Públicas

**Universidad Nacional de Ingeniería – Maestría en Inteligencia Artificial**  
**Autor:** Fernando García - Aradiel Hilario
**Versión:** 1.0 – Octubre 2025  
**Repositorio:** [webconceptos/Deteccion_Corrupcion](https://github.com/webconceptos/Deteccion_Corrupcion)

---

## 🎯 Propósito

Implementar un sistema predictivo que, utilizando **Machine Learning**, identifique **obras públicas con riesgo potencial de corrupción** en el Perú.  
El sistema integra datos de obras, empresas y funcionarios para generar un **índice de riesgo** que apoye la toma de decisiones.

---

## 🧩 Componentes Principales

| Componente | Descripción |
|-------------|-------------|
| **Ingesta de datos** | Recolección desde OSCE, MEF, SEACE y Contraloría. |
| **Preprocesamiento** | Limpieza, codificación y normalización. |
| **Modelo ML** | RandomForest / XGBoost con métrica PR-AUC. |
| **API FastAPI** | Servicio REST `/predict_proba`, `/health`, `/model_meta`. |
| **CI/CD** | GitHub Actions (lint + test + smoke). |
| **Docker** | Despliegue productivo con Gunicorn + Uvicorn. |

---

## ⚙️ Flujo del Sistema

```
Fuentes Públicas
   │
   ▼
Preprocesamiento → Entrenamiento → Exportación → API REST → Despliegue Docker
```

---

## 🚀 API – Ejemplo de Predicción

**POST /predict_proba**
```json
{
  "filas": [{"monto_total": 1200000, "departamento": "LIMA", "empresa": "XYZ SAC"}]
}
```
**Respuesta**
```json
{
  "resultados": [{"proba": 0.78, "threshold": 0.62, "riesgoso": true}]
}
```

---

## 📊 Resultados del Modelo

| Métrica | Valor |
|----------|--------|
| ROC-AUC | 0.83 |
| PR-AUC | 0.79 |
| F1-Score | 0.70 |

---

## 🧪 Calidad y Seguridad

- **Ruff:** Linting automático.  
- **PyTest:** Pruebas unitarias.  
- **CI/CD:** Verificación automática en cada push.  
- **Docker:** Ejecución segura con usuario no root.  

---

## 🧭 Próximos Pasos

- [ ] Interpretabilidad SHAP (`/explain`)  
- [ ] Calibración de probabilidades  
- [ ] Dashboard React para visualización  
- [ ] Registro de modelos (MLflow)

---

## 🧑‍💻 Autor y Licencia

**Fernando García Aradiel- Hilario Aradiel **
📧 fgarcia@webconceptos.com  
**Licencia:** MIT License © 2025

> *“Prevenir la corrupción es posible cuando los datos hablan con inteligencia.”*
