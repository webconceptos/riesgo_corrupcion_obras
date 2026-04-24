Write-Host "Iniciando prueba" -ForegroundColor Cyan

$branches = @("a","b","c")

foreach ($b in $branches) {
    Write-Host "Procesando rama: $b"
}

Write-Host "Fin de prueba" -ForegroundColor Green
