# Installazione locale — Windows
## Prerequisiti
Git, PowerShell 7, Python 3.11+, PostgreSQL locale, Azure CLI e una sottoscrizione Azure con un deployment chat compatibile con function calling. Il collaudo iniziale ha utilizzato Python 3.13.2 e PostgreSQL 18.4.
## Download e dipendenze
Eseguire ogni comando su una singola riga.
```powershell
git clone -b feature/gh600-poc https://github.com/VivaLearning/agenticlab-it-support.git
cd agenticlab-it-support
pwsh -File scripts/setup.ps1
```
Lo script crea .venv, installa requirements.txt e copia .env.example in .env solo se assente. Non crea risorse cloud.
## Database dedicato
Creare un database vuoto agenticlab tramite pgAdmin oppure:
```powershell
psql -h localhost -U postgres -d postgres -c "CREATE DATABASE agenticlab;"
```
Non usare database di produzione. Per il laboratorio è possibile usare un utente dedicato proprietario del solo database invece di postgres.
## Configurazione
```powershell
code .env
```
```ini
DATABASE_URL=postgresql://postgres:CHANGE_ME@localhost:5432/agenticlab
AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=agenticlab-model
AZURE_OPENAI_API_VERSION=2024-10-21
MAX_TOKENS=20000
```
Sostituire i placeholder. Codificare in percent-encoding i caratteri riservati della password nella URI. Non pubblicare .env. Verificare git check-ignore .env prima di aggiungere file.
## Verifiche
```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -c "from dotenv import load_dotenv; load_dotenv(); import os, psycopg; c=psycopg.connect(os.environ['DATABASE_URL']); print(c.execute('SELECT current_database(), current_user').fetchone()); c.close()"
```
I due test di dominio non richiedono Azure o PostgreSQL. La seconda verifica controlla la connessione reale.
## Avvio
Configurare prima Azure come descritto in [azure-setup.md](azure-setup.md).
```powershell
pwsh -File scripts/start.ps1
```
Lo script crea le tre tabelle se mancanti e avvia Uvicorn su 127.0.0.1:8765. Aprire http://127.0.0.1:8765; OpenAPI/Swagger su /docs. Nessuna installazione Node.js necessaria.
## Aggiornamento
Interrompere Uvicorn con Ctrl+C, eseguire git pull e avviare nuovamente scripts/start.ps1. Ricaricare il browser con Ctrl+F5. Avviare una nuova missione. Non è necessario ricreare il database o il file .env.
## Sicurezza locale
Non esporre il server sulla rete: non dispone di autenticazione web. Il database conserva output e trace: usare soltanto dati sintetici. Non condividere screenshot contenenti credenziali.
