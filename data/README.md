# Data Directory – Sistema de Detección de Riesgos de Corrupción

Este directorio contiene la **arquitectura completa de datos** del sistema de detección de riesgos de corrupción en obras públicas del Perú.

A diferencia de versiones iniciales, el proyecto ha evolucionado hacia un enfoque **multi-actor**, integrando información de:

- Obras públicas
- Empresas contratistas
- Funcionarios públicos

---

# 🧠 Arquitectura de Datos

El sistema sigue una arquitectura en capas:

FUENTES → DATASETS ESPECIALIZADOS → DATASET MAESTRO → MODELOS

---

# 📂 Estructura del directorio

data/
├── raw/                  # Fuentes originales (trazabilidad)
├── external/             # Datos por dominio (obra, empresa, funcionario)
├── interim/              # Transformaciones intermedias
├── processed/            # ⭐ Datasets finales para modelado
├── datasets.json         # Metadatos de ingesta
└── README.md             # Este archivo

---

# 🔄 Evolución del Proyecto

## Versión inicial
- Dataset único integrado
- Bajo desempeño (problemas de desbalance y pérdida de granularidad)

## Versión actual (V3)
Se implementa un enfoque **multi-dataset especializado**:

dataset_obras_v3
dataset_empresa_v3
dataset_funcionario_v3
dataset_maestro_v2

---

# ⭐ DATASETS FINALES (processed/)

## 1️⃣ Dataset de Obras

Archivo:
dataset_obras_v3_4niveles_participante.parquet

Unidad de análisis:
Obra + participación (granular)

Target:
y_riesgo_obra_4niveles

Valores:
0: Sin riesgo
1: Bajo
2: Medio
3: Alto / Extremo

---

## 2️⃣ Dataset de Empresas

Archivo:
dataset_empresa_v3_4niveles.parquet

Unidad de análisis:
Empresa + participación en procesos

Target (proxy):
y_riesgo_empresa

Construido a partir de:
- sanciones
- inhabilitaciones
- penalidades
- responsabilidades

Nota:
No existe etiqueta oficial → se construye un indicador proxy.

---

## 3️⃣ Dataset de Funcionarios

Archivo:
dataset_funcionario_v3_4niveles_model.parquet

Unidad de análisis:
Funcionario + vínculo con obra

Target (proxy):
y_riesgo_funcionario

Basado en:
- responsabilidades
- sanciones administrativas
- sanciones penales

---

## 4️⃣ Dataset Maestro ⭐

Archivo:
dataset_maestro_v2_4niveles.parquet

Unidad de análisis final:
1 fila = 1 OBRA (IDENTIFICADOR_OBRA)

Integración:
OBRA + EMPRESA (agregado) + FUNCIONARIO (agregado)

---

# 🎯 Target final

y_riesgo_obra_4niveles

---

# ⚙️ Estrategia de Modelado

## 🔹 Modelo Maestro
Input:
- features obra
- features empresa
- features funcionario

Output:
- riesgo total de obra

---

## 🔹 Modelos Especializados
Modelo Obra
Modelo Empresa
Modelo Funcionario

Salida:
- riesgo_obra
- riesgo_empresa
- riesgo_funcionario

---

## 🔹 Arquitectura Híbrida (Recomendada)
Modelos especializados → Modelo maestro

Permite:
- Interpretabilidad por actor
- Decisión consolidada

---

# ⚠️ Riesgos de Datos Identificados

## 1. Desbalance de clases
Solución: redefinición a 4 niveles

## 2. Data Leakage
Se eliminaron variables como:
- RIESGO_OBRA
- RIESGO_DESCRIPCION_OBRA

## 3. Granularidad
Problema inicial:
1 fila = 1 obra

Solución:
obra + participante / empresa / funcionario

## 4. Integración de llaves
Problema:
CODIGO_OBRA ≠ IDENTIFICADOR_OBRA

Solución:
mapeo explícito entre llaves

---

# 📊 Calidad del Dataset

Obra: alto  
Empresa: medio (proxy)  
Funcionario: medio (proxy)  
Maestro: alto  

---

# 🔁 Reproducibilidad

notebooks/
├── build_dataset_obras_v3
├── build_dataset_empresa_v3
├── build_dataset_funcionario_v3
└── build_dataset_maestro_v2

---

# 🚀 Estado actual

✔ Dataset maestro funcional  
✔ Integración multi-actor  
✔ Targets definidos  
✔ Baseline listo  
✔ Arquitectura escalable  

---

# 🎓 Uso para Tesis

Permite:
- detectar riesgo de corrupción en obras
- identificar actores de riesgo
- priorizar intervenciones
- explicar el origen del riesgo

---

# 🧠 Nota final

Este proyecto evoluciona hacia un modelo **multi-actor e integrado**, alineado con sistemas modernos de detección de fraude y corrupción.
