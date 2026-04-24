<#
    Script: create_sprint4_notebooks.ps1
    Proposito: Crear todos los notebooks base del Sprint 4
#>

Write-Host "`n=== Creando notebooks del Sprint 4 ===" -ForegroundColor Cyan

# Ruta base
$basePath = "notebooks/Sprint4"

# Crear carpeta si no existe
if (-not (Test-Path $basePath)) {
    New-Item -ItemType Directory -Path $basePath | Out-Null
    Write-Host "Carpeta Sprint4 creada." -ForegroundColor Yellow
}

# Lista de notebooks
$notebooks = @(
    "01_OptimizacionModelo.ipynb",
    "02_SlicesProblematcos.ipynb",
    "03_XAI_SHAP_LIME.ipynb",
    "04_InformeFinalResultados.ipynb",
    "05_PitchGeneracionMaterial.ipynb"
)

# Contenido JSON vacio minino
$emptyNotebook = @"
{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
"@

# Crear cada notebook si no existe
foreach ($nb in $notebooks) {
    $fullpath = "$basePath/$nb"

    if (-not (Test-Path $fullpath)) {
        $emptyNotebook | Out-File -Encoding ascii $fullpath
        Write-Host "Notebook creado: $nb" -ForegroundColor Green
    } else {
        Write-Host "Notebook ya existe: $nb" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Notebooks Sprint 4 listos ===" -ForegroundColor Magenta
