<#
    Script: run_sprint4.ps1
    Proposito: Ejecutar el pipeline Sprint 4 usando Papermill
    NOTA: El entorno YA debe estar activado antes de llamar este script.
#>

Write-Host "`n=== Ejecutando Pipeline Sprint 4 ===" -ForegroundColor Cyan

# 1. Mostrar entorno actual
Write-Host "`nEntorno ya activado. Continuando..." -ForegroundColor Yellow

# 2. Ejecutar pipeline Python
Write-Host "`nEjecutando pipeline papermill..." -ForegroundColor Yellow
python run_sprint4_pipeline.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Pipeline Sprint 4 COMPLETADO con exito ===" -ForegroundColor Green
} else {
    Write-Host "`nERROR: Hubo un fallo ejecutando el pipeline." -ForegroundColor Red
}
