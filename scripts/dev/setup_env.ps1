<# PowerShell setup for Windows
Usage:
  pwsh -File scripts/setup_env.ps1
  .\env\Scripts\Activate.ps1   # activate
  python -m ipykernel install --user --name env --display-name "Python (env)"
#>

param(
  [string]$PythonBin = "python"
)

$ErrorActionPreference = "Stop"
$envDir = "env"

Write-Host "[1/5] Checking Python..."
& $PythonBin --version

Write-Host "[2/5] Creating virtual environment at .\${envDir}"
& $PythonBin -m venv $envDir

Write-Host "[3/5] Activating virtual environment"
$activate = ".\${envDir}\Scripts\Activate.ps1"
. $activate

Write-Host "[4/5] Upgrading pip & base tools"
python -m pip install --upgrade pip setuptools wheel

Write-Host "[5/5] Installing project requirements"
if (Test-Path "requirements.txt") {
  pip install -r requirements.txt
} else {
  Write-Warning "requirements.txt not found. Installing minimal scientific stack..."
  pip install pandas numpy scikit-learn matplotlib pyarrow fastparquet jupyter ipykernel
}

# Optional: Jupyter kernel
python -m ipykernel install --user --name env --display-name "Python (env)"

Write-Host "✅ Done. Activate with:  .\${envDir}\Activate.ps1"
