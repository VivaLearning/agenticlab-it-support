$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
if (!(Test-Path .env)) { Copy-Item .env.example .env }
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "venv failed" }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "pip failed" }
Write-Host "Edit .env, create the dedicated PostgreSQL database agenticlab, then run scripts/start.ps1"
