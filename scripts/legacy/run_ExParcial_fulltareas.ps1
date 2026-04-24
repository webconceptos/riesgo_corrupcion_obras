# ==========================================================
# ExParcial Multi-Thread Pipeline (VERSIÓN FINAL FUNCIONAL)
# ==========================================================

$ErrorActionPreference = "Stop"

# -----------------------------
# Preparar logs
# -----------------------------
$LOG_DIR = Join-Path $PSScriptRoot "reports/logs"
if (!(Test-Path $LOG_DIR)) { New-Item -ItemType Directory -Path $LOG_DIR | Out-Null }

$STAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$MASTER_LOG = Join-Path $LOG_DIR "run_ExParcial_$STAMP.log"

function LogMaster {
    param([string]$Text)
    Add-Content -Path $MASTER_LOG -Value "[$(Get-Date)] $Text"
}

function Sec { param([string]$t)
    Write-Host ""
    Write-Host "=========================================================="
    Write-Host $t
    Write-Host "=========================================================="
}

function Info { param([string]$t) Write-Host "[INFO] $t" }
function ErrMsg { param([string]$t) Write-Host "[ERR ] $t" }

# -----------------------------
# Inicio
# -----------------------------
Sec "ExParcial Multi-Thread Pipeline"
LogMaster "Inicio pipeline"

# -----------------------------
# Verificar papermill
# -----------------------------
try {
    papermill --version *> $null
} catch {
    ErrMsg "Papermill no está disponible."
    exit 1
}
Info "papermill OK"
LogMaster "papermill OK"

# -----------------------------
# Rutas absolutas
# -----------------------------
$ROOT = $PSScriptRoot

$Tasks = @(
    @{ Name="ExParcial_IngAtributos";         In="$ROOT/notebooks/ExParcial_IngAtributos.ipynb";         Out="$ROOT/notebooks/out_ExParcial_IngAtributos.ipynb" },
    @{ Name="ExParcial_Experimentos";         In="$ROOT/notebooks/ExParcial_Experimentos.ipynb";         Out="$ROOT/notebooks/out_ExParcial_Experimentos.ipynb" },
    @{ Name="ExParcial_ValidacionResultados"; In="$ROOT/notebooks/ExParcial_ValidacionResultados.ipynb"; Out="$ROOT/notebooks/out_ExParcial_ValidacionResultados.ipynb" },
    @{ Name="ExParcial_AblationStudy";        In="$ROOT/notebooks/ExParcial_AblationStudy.ipynb";        Out="$ROOT/notebooks/out_ExParcial_AblationStudy.ipynb" },
    @{ Name="ExParcial_XAI";                  In="$ROOT/notebooks/ExParcial_XAI.ipynb";                  Out="$ROOT/notebooks/out_ExParcial_XAI.ipynb" },
    @{ Name="ExParcial_EDA_Profesional";      In="$ROOT/notebooks/ExParcial_EDA_Profesional.ipynb";      Out="$ROOT/notebooks/out_ExParcial_EDA_Profesional.ipynb" }
)

# -----------------------------
# Lanzar trabajos en paralelo
# -----------------------------
$Jobs = @()
foreach ($t in $Tasks) {

    Sec "Lanzando hilo: $($t.Name)"
    LogMaster "Lanzando hilo: $($t.Name)"

    $Jobs += Start-Job -ScriptBlock {
        param($Name, $InFile, $OutFile, $MasterLog, $RootFolder)

        $localLog = Join-Path $RootFolder "reports/logs/log_$Name.log"

        try {
            papermill $InFile $OutFile --log-output *> $localLog
            
            Add-Content -Path $MasterLog -Value "[OK] $Name"
            Write-Output 0
        }
        catch {
            Add-Content -Path $MasterLog -Value "[ERROR] $Name : $($_.Exception.Message)"
            Write-Output 1
        }

    } -ArgumentList $t.Name, $t.In, $t.Out, $MASTER_LOG, $ROOT
}

# -----------------------------
# Esperar finalización
# -----------------------------
Sec "Esperando finalización de hilos..."
Wait-Job -Job $Jobs | Out-Null

# -----------------------------
# Evaluar resultados
# -----------------------------
$Failures = @()

foreach ($job in $Jobs) {
    $code = Receive-Job $job
    if ($code -ne 0) {
        $Failures += $job.Id
    }
}

# -----------------------------
# Resumen final
# -----------------------------
Sec "Resumen Final"

if ($Failures.Count -eq 0) {
    Info "Todos los notebooks completados con éxito"
    LogMaster "Pipeline completado sin errores"
}
else {
    ErrMsg "Notebook con error:"
    foreach ($id in $Failures) {
        ErrMsg " - JobId $id"
    }
    LogMaster "Pipeline finalizado con errores"
}

Info "Log maestro: $MASTER_LOG"
Info "Pipeline finalizado"
