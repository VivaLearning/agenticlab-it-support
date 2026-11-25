$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
& .\.venv\Scripts\python.exe -c "from dotenv import load_dotenv; load_dotenv(); import os, psycopg; from pathlib import Path; c=psycopg.connect(os.environ['DATABASE_URL']); c.execute(Path('database/schema.sql').read_text()); c.commit(); c.close()"
if ($LASTEXITCODE -ne 0) { throw "Database initialization failed" }
& .\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8765
