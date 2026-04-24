Write-Host '== Verificando ubicaciÃ³n actual ==' -ForegroundColor Cyan
git status
Write-Host "
== Remotos configurados ==" -ForegroundColor Cyan
git remote -v
Write-Host "
== Actualizando desde remoto ==" -ForegroundColor Cyan
git fetch --all --prune
\ = 'backup/local-' + (Get-Date -Format 'yyyyMMdd-HHmm')
Write-Host "
== Creando respaldo temporal: \ ==" -ForegroundColor Yellow
git branch \
Write-Host "
== Cambiando a rama main ==" -ForegroundColor Cyan
git checkout main
Write-Host "
== Sincronizando con origin/main ==" -ForegroundColor Cyan
git reset --hard origin/main
Write-Host "
== Limpiando archivos no rastreados ==" -ForegroundColor Cyan
git clean -fd
Write-Host "
== Estado final del repositorio ==" -ForegroundColor Green
git status
Write-Host "
Ãšltimo commit remoto:" -ForegroundColor Green
git log -1 --oneline --decorate
Write-Host "
== Verificando .env ==" -ForegroundColor Cyan
if (Test-Path '.env') {
  if (-not (Select-String -Path '.gitignore' -Pattern '^\s*\.env\s*$' -SimpleMatch -Quiet)) {
    Add-Content .gitignore '.env'
  }
  git rm --cached .env 2>\
  Write-Host 'Archivo .env excluido del versionado.' -ForegroundColor Yellow
} else {
  Write-Host 'No se encontrÃ³ .env (ok).' -ForegroundColor Green
}
Write-Host "
âœ… SincronizaciÃ³n completa. Tu copia local ahora coincide con origin/main" -ForegroundColor Green
