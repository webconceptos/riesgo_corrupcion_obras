# ==========================================================
# Script: ExParcial_push.ps1
# Proyecto: Deteccion Corrupcion - Examen Parcial
# Autor: Fernando Garcia / Viernes AI
# Objetivo: Automatizar commit y push seguro hacia GitHub
# Version: FINAL-STABLE
# ==========================================================

$ErrorActionPreference = "Stop"

# ---------------------------------------
# Preparar logs
# ---------------------------------------
$LOG_DIR = "reports/logs"
if (!(Test-Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR | Out-Null
}

$STAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$LOG_FILE = "$LOG_DIR/push_exparcial_$STAMP.log"

function Log {
    param([string]$msg)
    $line = "[" + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + "] " + $msg
    Add-Content -Path $LOG_FILE -Value $line
}

function Info { param($m) Write-Host "[INFO]  $m" -ForegroundColor Green;  Log $m }
function Warn { param($m) Write-Host "[WARN]  $m" -ForegroundColor Yellow; Log $m }
function Err  { param($m) Write-Host "[ERROR] $m" -ForegroundColor Red;   Log $m }

# ---------------------------------------
# Encabezado
# ---------------------------------------
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "     ExParcial Push Script - GitHub Autopush"
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------
# Preguntar la rama a usar
# ---------------------------------------
Write-Host "Ingrese la rama destino (ejemplo: ExParcial_Experimentos):"
$BRANCH = Read-Host "Rama"

if ([string]::IsNullOrWhiteSpace($BRANCH)) {
    Err "No se ingreso una rama. Abortando."
    exit 1
}

Info ("Rama seleccionada: " + $BRANCH)

# ---------------------------------------
# Verificar si la rama existe
# ---------------------------------------
try {
    $branches = git branch --list $BRANCH
    if ($branches.Length -eq 0) {
        Warn ("La rama " + $BRANCH + " no existe localmente.")
        Write-Host "Desea crearla? (s/n):"
        $opt = Read-Host
        if ($opt -match "^[sS]$") {
            git checkout -b $BRANCH | Out-Null
            Info ("Rama creada: " + $BRANCH)
        }
        else {
            Err "Operacion cancelada."
            exit 1
        }
    }
}
catch {
    Err ("Error verificando existencia de rama: " + $_.Exception.Message)
    exit 1
}

# ---------------------------------------
# Cambiar a la rama
# ---------------------------------------
try {
    git checkout $BRANCH | Out-Null
    Info ("Cambiado a la rama " + $BRANCH)
}
catch {
    Err ("ERROR cambiando a la rama {0}: {1}" -f $BRANCH, $_.Exception.Message)
    exit 1
}

# ---------------------------------------
# Preguntar mensaje de commit
# ---------------------------------------
Write-Host ""
Write-Host "Escriba el mensaje de commit:"
$MSG = Read-Host "Commit message"

if ([string]::IsNullOrWhiteSpace($MSG)) {
    $MSG = "Actualizacion automatica ExParcial - " + $STAMP
    Info ("Mensaje vacio. Usando mensaje por defecto: " + $MSG)
}

# ---------------------------------------
# Confirmacion
# ---------------------------------------
Write-Host ""
Write-Host "======================================="
Write-Host "Resumen:"
Write-Host "  Rama:   $BRANCH"
Write-Host "  Commit: $MSG"
Write-Host "======================================="
Write-Host ""

$confirm = Read-Host "Desea continuar? (s/n)"
if ($confirm -notmatch "^[sS]$") {
    Warn "Operacion cancelada por el usuario."
    exit 0
}

# ---------------------------------------
# Ejecutar git add/commit/push
# ---------------------------------------
try {
    Info "Agregando cambios..."
    git add . | Out-Null

    Info "Creando commit..."
    git commit -m "$MSG" | Out-Null

    Info "Enviando a GitHub..."
    git push origin $BRANCH | Out-Null

    Info "Push completado correctamente."
}
catch {
    Err ("Error durante push: " + $_.Exception.Message)
    exit 1
}

# ---------------------------------------
# Fin
# ---------------------------------------
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Info "Proceso finalizado."
Info ("Log disponible en: " + $LOG_FILE)
Write-Host "==========================================================" -ForegroundColor Cyan
