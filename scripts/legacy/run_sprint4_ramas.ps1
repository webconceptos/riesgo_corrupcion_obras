<#
    Script: run_sprint4.ps1
    Proposito: Crear y publicar todas las ramas del Sprint 4
#>

Write-Host "`n=== Sprint 4: Creacion de Ramas ===" -ForegroundColor Cyan

# 1. Validar Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git no esta instalado. Abortando." -ForegroundColor Red
    exit 1
}

# 2. Validar repositorio
if (-not (Test-Path ".git")) {
    Write-Host "No estas dentro de un repositorio Git." -ForegroundColor Red
    exit 1
}

# 3. Actualizar rama main
Write-Host "`n--- Actualizando rama main ---" -ForegroundColor Yellow
git checkout main
git pull origin main

# 4. Lista de ramas Sprint 4
$sprint4Branches = @(
    "Sprint4-Optimizacion",
    "Sprint4-XAI",
    "Sprint4-Slices",
    "Sprint4-InformeFinal",
    "Sprint4-Pitch"
)

# 5. Funcion para crear y publicar ramas
function Create-And-PublishBranch {
    param (
        [string]$branchName
    )

    Write-Host "`n--- Procesando rama: $branchName ---" -ForegroundColor Green
    
    git checkout -b $branchName
    git push -u origin $branchName

    Write-Host "Rama $branchName creada y publicada correctamente." -ForegroundColor Cyan
}

# 6. Crear todas las ramas
foreach ($branch in $sprint4Branches) {
    Create-And-PublishBranch -branchName $branch
}

Write-Host "`n=== Todas las ramas del Sprint 4 han sido creadas exitosamente ===" -ForegroundColor Magenta
