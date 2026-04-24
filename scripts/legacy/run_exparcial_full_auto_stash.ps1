# ============================================
# Script: crear_ramas_parcial_auto_stash.ps1
# Autor: Fernando García - Hilario Aradiel  
# Fecha: 2025-11-12
# Objetivo: Crear ramas del Examen Parcial con
#           manejo automático de stash
# ============================================

Write-Host "=== Creación de ramas del Examen Parcial ===" -ForegroundColor Cyan

# 1. Validar si estamos dentro de un repositorio Git
if (-not (Test-Path ".git")) {
    Write-Host "Error: No se encontró un repositorio Git en este directorio." -ForegroundColor Red
    exit 1
}

# 2. Detectar si hay cambios pendientes
$changes = git status --porcelain

$stashCreated = $false

if ($changes) {
    Write-Host "Cambios sin commitear detectados. Haciendo stash automático..." -ForegroundColor Yellow

    git stash push -m "stash_auto_ramas_exparcial"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al ejecutar git stash." -ForegroundColor Red
        exit 1
    }

    $stashCreated = $true
    Write-Host "Stash creado correctamente." -ForegroundColor Green
}
else {
    Write-Host "No hay cambios pendientes. Continuando..." -ForegroundColor Green
}

# 3. Cambiar a la rama main
Write-Host "Cambiando a 'main'..." -ForegroundColor Yellow
git checkout main

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al cambiar a la rama main." -ForegroundColor Red
    exit 1
}

# 4. Traer los últimos cambios
Write-Host "Haciendo pull desde origin/main..." -ForegroundColor Yellow
git pull origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al hacer pull de main." -ForegroundColor Red
    exit 1
}

# 5. Ramas a crear
$ramas = @(
    "ExParcial-Experimentos",
    "ExParcial-IngAtributos",
    "ExParcial-ValidacionResultados"
)

foreach ($rama in $ramas) {

    Write-Host "`n--- Procesando rama: $rama ---" -ForegroundColor Cyan

    # Verificar si ya existe localmente
    $existeLocal = git branch --list $rama

    if ($existeLocal) {
        Write-Host "La rama $rama ya existe localmente. Saltando creación." -ForegroundColor Yellow
    }
    else {
        Write-Host "Creando rama local: $rama" -ForegroundColor Green
        git checkout -b $rama

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error al crear la rama $rama." -ForegroundColor Red
            exit 1
        }
    }

    # Publicar rama en remoto
    Write-Host "Publicando rama en remoto: origin/$rama" -ForegroundColor Green
    git push -u origin $rama

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al publicar la rama $rama." -ForegroundColor Red
        exit 1
    }
}

# 6. Restaurar stash si existía
if ($stashCreated) {
    Write-Host "`nRestaurando el stash previo..." -ForegroundColor Yellow
    git stash pop

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Advertencia: El stash contenía cambios en conflicto. Revise manualmente." -ForegroundColor Red
    }
    else {
        Write-Host "Stash restaurado correctamente." -ForegroundColor Green
    }
}

Write-Host "`n=== Todas las ramas fueron creadas y publicadas correctamente. ===" -ForegroundColor Cyan
