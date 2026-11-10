param([string]$Version = "0.006")
$ErrorActionPreference = "Stop"
$py = ".\dtf_env\Scripts\python.exe"
if (-not (Test-Path $py)) { throw "dtf_env not found" }
& $py -m PyInstaller --noconsole --onefile --name "Espadan-DTF-Studio" --paths "." --distpath "dist" --workpath "build" --specpath "build" --clean main.py
if ($LASTEXITCODE -ne 0) { throw "Build failed" }
Write-Host "Built: dist\Espadan-DTF-Studio.exe"
