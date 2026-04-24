# ==========================================================
# Script maestro PowerShell: run_semana6_full.ps1
# Proyecto: Detección de Riesgos de Corrupción en Obras Públicas
# Autores: Fernando García - Hilario Aradiel
# Objetivo: Ejecutar TODO el pipeline de la Semana 6 con LOGS y manejo de errores
# ==========================================================

# === Configuración general de PowerShell ===
$ErrorActionPreference = "Stop"   # Convierte errores en "terminating" para catch
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# === Rutas de trabajo y logs ===
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$LogDir = Join-Path $Root "reports\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogDir "semana6_run_$Stamp.log"

# Transcript (log “oficial” de PowerShell)
$TranscriptFile = Join-Path $LogDir "semana6_transcript_$Stamp.log"
Start-Transcript -Path $TranscriptFile -Append | Out-Null

# === Utilidades de logging ===
function Write-Log {
    param(
        [Parameter(Mandatory=$true)][string]$Message,
        [ValidateSet('INFO','WARN','ERROR','STEP')]$Level = 'INFO'
    )
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $line = "[$ts][$Level] $Message"
    # Consola con color
    switch ($Level) {
        'INFO'  { Write-Host $line -ForegroundColor Gray }
        'WARN'  { Write-Host $line -ForegroundColor Yellow }
        'ERROR' { Write-Host $line -ForegroundColor Red }
        'STEP'  { Write-Host $line -ForegroundColor Cyan }
    }
    # Archivo
    $line | Out-File -FilePath $LogFile -Append -Encoding utf8
}

# Ejecuta un comando y loguea stdout/stderr en tiempo real
function Invoke-Step {
    param(
        [Parameter(Mandatory=$true)][string]$Title,
        [Parameter(Mandatory=$true)][string]$CommandLine,
        [switch]$StopOnError  # si se pasa, aborta en error
    )

    Write-Log "== $Title ==" STEP
    Write-Log "Comando: $CommandLine" INFO

    try {
        # Ejecuta el comando, captura salida y errores, y los duplica a log
        cmd /c $CommandLine 2>&1 | Tee-Object -FilePath $LogFile -Append
        $exit = $LASTEXITCODE

        if ($exit -ne 0) {
            Write-Log "Fallo (exitcode=$exit) en: $Title" ERROR
            if ($StopOnError) {
                throw "Paso fallido: $Title (exitcode=$exit)"
            } else {
                $script:ErrorsFound = $true
            }
        } else {
            Write-Log "OK: $Title" INFO
        }
    }
    catch {
        Write-Log "Excepción en '$Title': $($_.Exception.Message)" ERROR
        if ($StopOnError) { throw }
        else { $script:ErrorsFound = $true }
    }
    Write-Log ("-"*70) INFO
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🧠 Semana 6 – Pipeline completo con LOGS ($Stamp) " -ForegroundColor Yellow
Write-Host " Log: $LogFile" -ForegroundColor DarkGray
Write-Host " Transcript: $TranscriptFile" -ForegroundColor DarkGray
Write-Host "==========================================================" -ForegroundColor Cyan

# === 1. Construcción de datasets ===
Invoke-Step -Title "Construyendo dataset ML (build_dataset_ml.py)" `
    -CommandLine "python scripts\build_dataset_ml.py"

Invoke-Step -Title "Construyendo dataset integrado (build_dataset_integrado.py)" `
    -CommandLine "python scripts\build_dataset_integrado.py"

# === 2. Entrenamiento de modelos ===
Invoke-Step -Title "Entrenando modelos (train_models.py --folds 5)" `
    -CommandLine "python scripts\train_models.py --folds 5"

# === 3. Análisis base postentrenamiento ===
Invoke-Step -Title "Importancia de variables (plot_importance.py)" `
    -CommandLine "python scripts\plot_importance.py"

Invoke-Step -Title "Calibración (plot_calibration.py)" `
    -CommandLine "python scripts\plot_calibration.py"

Invoke-Step -Title "Curva de aprendizaje (plot_learning_curves.py)" `
    -CommandLine "python scripts\plot_learning_curves.py"

# === 4. Visualizaciones avanzadas ===
Invoke-Step -Title "Threshold PR (plot_threshold_curve.py)" `
    -CommandLine "python scripts\plot_threshold_curve.py"

Invoke-Step -Title "Correlación con target (plot_correlation_target.py)" `
    -CommandLine "python scripts\plot_correlation_target.py"

Invoke-Step -Title "Curva de validación (plot_validation_curve.py)" `
    -CommandLine "python scripts\plot_validation_curve.py"

Invoke-Step -Title "Radar de métricas (plot_radar_model.py)" `
    -CommandLine "python scripts\plot_radar_model.py"

# === 5. Interpretabilidad SHAP ===
Invoke-Step -Title "SHAP summary (plot_shap_summary.py)" `
    -CommandLine "python scripts\plot_shap_summary.py"

# === 6. Robustez y Sesgo ===
Invoke-Step -Title "Robustez (robustness_analysis.py)" `
    -CommandLine "python scripts\robustness_analysis.py"

Invoke-Step -Title "Sesgo (analyze_bias.py)" `
    -CommandLine "python scripts\analyze_bias.py"

# === 7. Reporte PDF ===
Invoke-Step -Title "Reporte ejecutivo PDF (generar_reporte_semana6.py)" `
    -CommandLine "python scripts\generar_reporte_semana6.py"

# === 8. Resumen de outputs ===
Write-Host ""
Write-Log "Verificación de outputs:" INFO
Write-Log "📁 Dataset:        data\processed\dataset_integrado.parquet" INFO
Write-Log "📊 Figuras:        reports\figures\" INFO
Write-Log "📘 Reporte PDF:    reports\Semana6_Reporte_Ejecutivo.pdf" INFO
Write-Log "🗒️ Log file:       $LogFile" INFO
Write-Log "🗒️ Transcript:     $TranscriptFile" INFO

# === 9. Push opcional a GitHub ===
try {
    $resp = Read-Host "¿Deseas subir los resultados a GitHub? (s/n)"
    if ($resp -eq "s" -or $resp -eq "S") {
        Write-Log "Subiendo cambios a GitHub (feat/semana6-modelado)..." INFO
        cmd /c "git add . 2>&1" | Tee-Object -FilePath $LogFile -Append
        cmd /c "git commit -m ""Semana 6 ✅ Pipeline completo con logs y manejo de errores""" 2>&1 | Tee-Object -FilePath $LogFile -Append
        cmd /c "git push origin feat/semana6-modelado 2>&1" | Tee-Object -FilePath $LogFile -Append
        Write-Log "✅ Push completado." INFO
    } else {
        Write-Log "Cambios NO subidos. Puedes ejecutar 'git push' manualmente." WARN
    }
}
catch {
    Write-Log "Error durante el push a GitHub: $($_.Exception.Message)" ERROR
    $script:ErrorsFound = $true
}

# === 10. Cierre ===
Stop-Transcript | Out-Null

Write-Host ""
if ($script:ErrorsFound) {
    Write-Host "⚠️  Proceso finalizado con errores. Revisa el log:" -ForegroundColor Yellow
    Write-Host $LogFile -ForegroundColor Yellow
    Write-Host "`nSugerencia: abre el log y busca '[ERROR]' o el paso que falló." -ForegroundColor DarkYellow
} else {
    Write-Host "✅ Proceso Semana 6 finalizado correctamente." -ForegroundColor Green
    Write-Host "Log: $LogFile" -ForegroundColor DarkGray
}
# Mantener la ventana visible si se ejecuta con doble clic
if ($Host.Name -eq 'ConsoleHost') {
    # no-op
} else {
    Read-Host "Presiona Enter para cerrar"
}
