# ===============================================================
# ExParcial_setup_env.ps1 (Versión corregida)
# Objetivo: Instalar dependencias del Parcial sin depender de pip.exe
# Autor: Fernando García - Hilario Aradiel
# Fecha: 2025-11-12
# ===============================================================

Write-Host "=== Instalando dependencias del Parcial ===" -ForegroundColor Cyan

# 1. Verificar ruta del Python en uso
Write-Host "Python detectado en:" -ForegroundColor Yellow
python --version
where python

# 2. Actualizar pip usando python -m pip
Write-Host "`nActualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# 3. Instalar dependencias usando python -m pip
Write-Host "`nInstalando paquetes..." -ForegroundColor Yellow

python -m pip install `
    pandas `
    numpy `
    seaborn `
    matplotlib `
    scikit-learn `
    xgboost `
    papermill `
    shap `
    jupyter `
    pyarrow `
    fastparquet

if ($LASTEXITCODE -eq 0) {
    Write-Host "=== Instalación completada con éxito ===" -ForegroundColor Green
} else {
    Write-Host "Error durante la instalación de dependencias." -ForegroundColor Red
}
