# Glossario
| Termine | Definizione nel laboratorio |
|---|---|
| LLM | Modello linguistico che produce testo o richieste tool |
| Agent | Ruolo specializzato con istruzioni, contesto e tool |
| Goal | Risultato da ottenere |
| Constraint | Condizione da rispettare durante la missione |
| Planner | Agente di diagnosi e pianificazione |
| Resolver | Agente di esecuzione |
| Verifier | Agente di verifica indipendente |
| Orchestrator | Codice che controlla stato, routing e arresto |
| Handoff | Trasferimento del controllo e del contesto a un agente |
| Tool calling | Richiesta strutturata di invocazione di una funzione |
| Observation | Risultato restituito da un tool |
| Step | Singola chiamata LLM e possibile tool |
| Phase | Sequenza di step dello stesso agente |
| Iteration | Ciclo di pianificazione, risoluzione e verifica |
| Replanning | Nuovo piano basato sulle evidenze di un fallimento |
| Shared state | Informazioni persistenti gestite dall'orchestratore |
| Context | Informazioni effettivamente inviate al modello |
| Guardrail | Controllo che limita comportamenti o azioni |
| Human-in-the-loop | Decisione umana richiesta prima di un intervento |
| Least privilege | Minimo insieme di permessi necessario |
| Blast radius | Perimetro potenziale dell'impatto di un intervento |
| Escalation | Arresto senza successo e necessità di intervento esterno |
| Trace | Cronologia delle operazioni osservabili |
| Token | Unità di elaborazione del modello |
| TPM / RPM | Limiti di token e richieste per minuto |
| JSONB | Tipo PostgreSQL per documenti JSON |
| RBAC | Controllo accessi basato su ruoli |
| MCP | Protocollo per collegare strumenti e contesto; non implementato nel POC |
