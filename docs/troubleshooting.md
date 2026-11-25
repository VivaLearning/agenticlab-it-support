# Troubleshooting
| Sintomo | Controllo |
|---|---|
| Python non trovato | python --version; verificare PATH |
| ImportError | Rieseguire scripts/setup.ps1 e usare .venv |
| PostgreSQL connection refused | Servizio, host, porta 5432 |
| Password authentication failed | Credenziali locali e URI encoding |
| Database does not exist | Creare agenticlab |
| Azure CLI duplicate accounts | az logout; az account clear; login con tenant esplicito |
| Azure 401 | Login e catena DefaultAzureCredential |
| Azure 403 | Ruolo Cognitive Services OpenAI User e propagazione |
| Azure 404 | Endpoint, deployment name e API version |
| Azure 429 | Quota, TPM/RPM, ridurre frequenza; non confondere con budget |
| Port 8765 in use | Arrestare il processo precedente |
| UI vecchia | git pull, riavvio server, Ctrl+F5 |
| ERROR nella missione | Consultare trace e terminale; avviare nuova missione dopo correzione |
| Fase non prosegue | Controllare stato: approvazione, escalation, limite, errore |
## Verifiche rapide
```powershell
git branch
git status --short
git check-ignore .env
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall -q backend
az account show -o table
```
Non copiare password o token nei ticket. Il browser mostra il tipo di eccezione LLM, non necessariamente i dettagli del provider; ripetere lo smoke test CLI per una diagnosi più precisa. Un risultato diverso nell'ordine dei tool non è automaticamente un bug. Se una fase si prolunga, usare Pausa esecuzione e mostrare la trace.
