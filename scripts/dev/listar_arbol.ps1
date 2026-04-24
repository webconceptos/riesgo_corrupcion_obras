Param(
    [string]$Path = "."
)

# Validar directorio
if (-not (Test-Path $Path)) {
    Write-Host "❌ Error: '$Path' no existe." -ForegroundColor Red
    exit
}

$fullPath = (Resolve-Path $Path).Path
Write-Host "📁 Listando estructura tipo árbol para: $fullPath"
Write-Host "--------------------------------------------------"

# Función recursiva para imprimir árbol
function Show-Tree {
    param (
        [string]$CurrentPath,
        [string]$Prefix = ""
    )

    # Obtener subdirectorios y archivos
    $items = Get-ChildItem -LiteralPath $CurrentPath

    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $isLast = ($i -eq $items.Count - 1)

        if ($isLast) {
            Write-Host "$Prefix└── $($item.Name)"
            $nextPrefix = "$Prefix    "
        } else {
            Write-Host "$Prefix├── $($item.Name)"
            $nextPrefix = "$Prefix│   "
        }

        # Si es directorio, continuar recursión
        if ($item.PSIsContainer) {
            Show-Tree -CurrentPath $item.FullName -Prefix $nextPrefix
        }
    }
}

# Ejecutar árbol desde la raíz indicada
Show-Tree -CurrentPath $fullPath
