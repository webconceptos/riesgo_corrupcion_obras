# Notebooks – Sistema de Detección de Riesgos de Corrupción

Este directorio contiene los notebooks utilizados para la construcción, análisis y modelado del sistema de detección de riesgos de corrupción en obras públicas del Perú.

El flujo sigue una lógica progresiva:

EDA → Construcción de datasets → Dataset maestro → EDA maestro → Modelo baseline

---

# Estructura de Notebooks

## 1. Análisis Exploratorio Inicial

### 01_eda_diccionarios.ipynb

Explora diccionarios de datos, tipos de variables y define el contexto del dataset.

---

##  2. Construcción de Datasets Especializados (V3)

### 02_build_dataset_obra_v3_4_etiquetas.ipynb
- Unidad: Obra + participación
- Target: y_riesgo_obra_4niveles

### 02_build_dataset_empresa_v3_4_etiquetas.ipynb
- Unidad: Empresa + participación
- Target proxy: y_riesgo_empresa

### 02_build_dataset_funcionario_v3_4_etiquetas.ipynb
- Unidad: Funcionario + obra
- Target proxy: y_riesgo_funcionario

---

##  3. Dataset Maestro

### 03_build_dataset_maestro_v2_4niveles_limpio.ipynb

Integra obra, empresa y funcionario en un solo dataset.

Unidad final:
1 fila = 1 obra

---

##  4. EDA Maestro

### 04_EDA_maestro.ipynb

Incluye:
- estadísticas descriptivas
- distribución del target
- histogramas
- boxplots
- correlaciones

---

##  5. Modelo Baseline

### 05_train_baseline_maestro_4niveles.ipynb

Modelo:
- Regresión logística multiclase

Evaluación:
- accuracy
- balanced accuracy
- macro F1
- matriz de confusión

---

#  Flujo completo

→ 01_eda_diccionarios
→ build datasets (obra, empresa, funcionario)
→ dataset maestro
→ EDA maestro
→ baseline

---

#  Estado

✔ Dataset maestro construido  
✔ EDA completo  
✔ Baseline ejecutado  

---

#  Uso

Permite reproducir el pipeline completo del proyecto y sustentar decisiones metodológicas.

