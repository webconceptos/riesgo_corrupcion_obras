# ===============================================================
# clean_reports.ps1 — Limpieza de reportes previos
# Autor: Fernando García - Hilario Aradiel
# Fecha: 2025-11-12
# ===============================================================

Write-Host "=== Limpiando reportes previos ===" -ForegroundColor Cyan

$paths = @(
    "reports/tablas",
    "reports/logs",
    "reports/graficos"
)

foreach ($p in $paths) {
    if (Test-Path $p) {
        Get-ChildItem -Path $p -Recurse | Remove-Item -Force
        Write-Host "Carpeta limpiada: $p" -ForegroundColor Yellow
    }
}

Write-Host "=== Limpieza completada ===" -ForegroundColor Green
