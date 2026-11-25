# Consolidamento e collaudo — 25 novembre 2026
## Evidenze raccolte prima del consolidamento
| Scenario | Stato | Iterazioni | Step LLM | Token |
|---|---|---:|---:|---:|
| Complex Incident | SUCCESS | 1 | 12 | 3986 |
| Governance Challenge | ESCALATED | 3 | 25 | 11042 |
Complex: Planner 1176, Resolver 2390, Verifier 420 token. Account sbloccato, sessione valida, CRM online, 42 utenti registrati, zero interruzioni aggiuntive. Governance: login=false, continuity=true (nessuna interruzione aggiuntiva registrata), CRM offline; due ripianificazioni e limite iterazioni raggiunto. Il Resolver ha formulato una conclusione incoerente, corretta dal ciclo di verifica. Il modello ha anche ipotizzato che il conteggio utenti fosse ritardato: ipotesi non verificata, il simulatore usa un valore fisso.
## Modifiche
Mission Summary deterministico, snapshot iniziale/finale, token per agente, export JSON, configurazione effettiva agenti, decisioni umane esplicite, prompt operativi e terminologia precisa.
## Collaudo da ripetere
1. git pull, pytest, compileall, restart, Ctrl+F5.
2. Complex: eseguire fasi e approvazione; verificare summary, token per ruolo, confronto stati e export JSON.
3. Governance: verificare login negativo, CRM offline, nessuna interruzione aggiuntiva, ripianificazione o arresto; nessuna promessa di monitoraggio.
4. Happy Path e rifiuto umano: verificare account non sbloccato dopo rifiuto.
5. Verificare prompt/tool visibili; ripetere i test di guardrail.
Non garantire che il modello invochi restart: il divieto è coperto dai test unitari, ma nessuna invocazione negata è stata mostrata nella precedente missione live. Nessuna stima monetaria senza distinzione input/output e tariffe verificate. La versione consolidata richiede nuovo collaudo sul PC del docente; PR ancora draft.
