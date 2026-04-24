#!/bin/bash
# ==========================================================
# Script maestro Bash: run_semana6_full.sh
# Proyecto: Detección de Riesgos de Corrupción en Obras Públicas
# Autores: Fernando García - Hilario Aradiel
# Objetivo: Ejecutar TODO el pipeline de la Semana 6 con logs y control de errores
# ==========================================================

# === Configuración general ===
set -e  # detiene en comandos críticos, pero con control manual
timestamp=$(date +"%Y%m%d_%H%M%S")
log_dir="reports/logs"
log_file="$log_dir/semana6_run_${timestamp}.log"
mkdir -p "$log_dir"

echo "==========================================================" | tee -a "$log_file"
echo " 🧠 Semana 6 – Pipeline completo de modelado predictivo" | tee -a "$log_file"
echo " Log: $log_file" | tee -a "$log_file"
echo "==========================================================" | tee -a "$log_file"
sleep 1

# === Funciones ===
log_step() { echo -e "\n[$(date '+%H:%M:%S')] ▶️  $1" | tee -a "$log_file"; }
log_ok()   { echo "✅ $1" | tee -a "$log_file"; }
log_warn() { echo "⚠️  $1" | tee -a "$log_file"; }
log_err()  { echo "❌ $1" | tee -a "$log_file"; }

run_cmd() {
    local title="$1"
    local cmd="$2"
    log_step "$title"
    echo "Comando: $cmd" >> "$log_file"
    eval "$cmd" >> "$log_file" 2>&1
    local status=$?
    if [ $status -eq 0 ]; then
        log_ok "Completado: $title"
    else
        log_err "Error en: $title (código $status)"
        echo "[ERROR] $title (exitcode $status)" >> "$log_file"
        ERRORS=true
    fi
}

# === 1. Construcción de datasets ===
run_cmd "📦 [1/9] Construyendo datasets..." \
    "python scripts/build_dataset_ml.py && python scripts/build_dataset_integrado.py"
sleep 1

# === 2. Entrenamiento de modelos ===
run_cmd "🤖 [2/9] Entrenando modelos..." \
    "python scripts/train_models.py --folds 5"
sleep 1

# === 3. Análisis postentrenamiento ===
run_cmd "📈 [3/9] Analizando resultados y métricas..." \
    "python scripts/plot_importance.py && python scripts/plot_calibration.py && python scripts/plot_learning_curves.py"
sleep 1

# === 4. Visualizaciones avanzadas ===
run_cmd "📊 [4/9] Creando visualizaciones adicionales..." \
    "python scripts/plot_threshold_curve.py && python scripts/plot_correlation_target.py && python scripts/plot_validation_curve.py && python scripts/plot_radar_model.py"
sleep 1

# === 5. Interpretabilidad SHAP ===
run_cmd "🔍 [5/9] Interpretabilidad con SHAP..." \
    "python scripts/plot_shap_summary.py"
sleep 1

# === 6. Evaluación de robustez y sesgo ===
run_cmd "🧩 [6/9] Evaluando robustez y sesgo..." \
    "python scripts/robustness_analysis.py && python scripts/analyze_bias.py"
sleep 1

# === 7. Generación de reporte PDF ===
run_cmd "📄 [7/9] Generando reporte ejecutivo..." \
    "python scripts/generar_reporte_semana6.py"
sleep 1

# === 8. Resumen final ===
echo -e "\n==========================================================" | tee -a "$log_file"
echo "✅ [8/9] Verificación de resultados:" | tee -a "$log_file"
echo "📁 Dataset:        data/processed/dataset_integrado.parquet" | tee -a "$log_file"
echo "📊 Figuras:        reports/figures/" | tee -a "$log_file"
echo "📘 Reporte PDF:    reports/Semana6_Reporte_Ejecutivo.pdf" | tee -a "$log_file"
echo "🗒️  Log:           $log_file" | tee -a "$log_file"
sleep 1

# === 9. Subida opcional a GitHub ===
read -p "¿Deseas subir los resultados a GitHub? (s/n): " RESP
if [[ "$RESP" =~ ^[sS]$ ]]; then
    run_cmd "🚀 Subiendo cambios a GitHub..." \
        "git add . && git commit -m 'Semana 6 ✅ Pipeline completo con logs y control de errores' && git push origin feat/semana6-modelado"
else
    log_warn "Cambios NO subidos. Puedes ejecutar 'git push' manualmente más tarde."
fi

echo "==========================================================" | tee -a "$log_file"
if [ "$ERRORS" = true ]; then
    echo "⚠️  Proceso finalizado con errores. Revisa el log: $log_file" | tee -a "$log_file"
else
    echo "🏁 Proceso Semana 6 finalizado exitosamente." | tee -a "$log_file"
fi
echo "Autor: Fernando García - Hilario Aradiel" | tee -a "$log_file"
echo "==========================================================" | tee -a "$log_file"
