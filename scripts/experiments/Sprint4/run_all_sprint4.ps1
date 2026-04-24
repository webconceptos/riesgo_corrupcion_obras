# ==============================================================
# Script: run_all_sprint4.ps1
# Autor: Fer + Viernes
# Uso: Ejecuta todo el pipeline del Sprint 4
# ==============================================================

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host ""
Write-Host "============================================================"
Write-Host "        INICIANDO PIPELINE COMPLETO SPRINT 4"
Write-Host "============================================================"
Write-Host ""

# --------------------------------------------------------------
# Helper para ejecutar pasos
# --------------------------------------------------------------
function Run-Step {
    param (
        [string] $title,
        [string] $command
    )

    Write-Host ""
    Write-Host "[*] Ejecutando: $title" -ForegroundColor Yellow
    Write-Host "    Command: $command" -ForegroundColor DarkGray

    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        iex $command
        $sw.Stop()

        Write-Host "[OK] $title completado en $($sw.Elapsed.TotalSeconds) segundos" -ForegroundColor Green
    }
    catch {
        Write-Host ""
        Write-Host "[ERROR] Fallo en etapa: $title" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
}

# --------------------------------------------------------------
# Activar entorno virtual si existe
# --------------------------------------------------------------
$venv = "$root/../../env/Scripts/Activate.ps1"
if (Test-Path $venv) {
    Write-Host "[*] Activando entorno virtual..." -ForegroundColor Yellow
    . $venv
}

Write-Host ""
Write-Host "[INFO] Directorio Sprint4: $root" -ForegroundColor Cyan

# --------------------------------------------------------------
# 01 – Baseline inference
# --------------------------------------------------------------
Run-Step "01 - Inferencia baseline" "python `"$root/01_run_inference_baseline.py`""

# --------------------------------------------------------------
# 02 – Modelo actual inference
# --------------------------------------------------------------
Run-Step "02 - Inferencia modelo actual" "python `"$root/02_run_inference_model_actual.py`""

# --------------------------------------------------------------
# 03 – Export ONNX
# --------------------------------------------------------------
Run-Step "03 - Exportacion ONNX" "python `"$root/03_export_to_onnx.py`""

# --------------------------------------------------------------
# 04 – Latencia CPU
# --------------------------------------------------------------
Run-Step "04 - Latencia CPU" "python `"$root/04_latency_cpu.py`""

# --------------------------------------------------------------
# 05 – Latencia ONNX
# --------------------------------------------------------------
Run-Step "05 - Latencia ONNX" "python `"$root/05_latency_onnx.py`""

# --------------------------------------------------------------
# 06 – Latencia TensorRT (si aplica)
# --------------------------------------------------------------
if (Test-Path "$root/06_latency_tensorrt.py") {
    Run-Step "06 - Latencia TensorRT" "python `"$root/06_latency_tensorrt.py`""
}
else {
    Write-Host "[INFO] TensorRT no disponible. Saltando etapa." -ForegroundColor DarkYellow
}

# --------------------------------------------------------------
# 07 – Locust load test
# --------------------------------------------------------------
if (Test-Path "$root/07_locust_loadtest.py") {
    Run-Step "07 - Locust load test" "python `"$root/07_locust_loadtest.py`""
}
else {
    Write-Host "[INFO] No existe archivo locust_loadtest. Etapa omitida." -ForegroundColor DarkYellow
}

# --------------------------------------------------------------
# 08 – Evaluación de percepción
# --------------------------------------------------------------
if (Test-Path "$root/08_evaluacion_percepcion.py") {
    Run-Step "08 - Evaluacion percepcion" "python `"$root/08_evaluacion_percepcion.py`""
}
else {
    Write-Host "[INFO] No existe 08_evaluacion_percepcion.py" -ForegroundColor DarkYellow
}

# --------------------------------------------------------------
# 09 – Generar informe Sprint 4
# --------------------------------------------------------------
Run-Step "09 - Generar informe Sprint 4" "python `"$root/09_generar_reporte_sprint4.py`""

Write-Host ""
Write-Host "============================================================"
Write-Host "   PIPELINE SPRINT 4 COMPLETADO EXITOSAMENTE"
Write-Host "============================================================"
Write-Host ""
