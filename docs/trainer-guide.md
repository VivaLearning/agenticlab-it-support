# Manuale Trainer — GH-600, demo AgenticLab

## Obiettivo e durata
Demo frontale di 10–15 minuti. Nessuna domanda agli studenti e nessun laboratorio durante il webinar. Il docente guida l'esecuzione, usa le pause per spiegare i concetti e non mostra credenziali o dati personali. Il materiale è integrativo, non ufficiale Microsoft.

## Preparazione prima della diretta
- Avviare PostgreSQL e FastAPI, verificare il login Azure e il deployment.
- Eseguire pytest e uno smoke test LLM.
- Provare Happy Path e Complex Incident prima della registrazione.
- Aprire http://127.0.0.1:8765 e impostare uno zoom leggibile.
- Tenere disponibile questo copione e la trace di una prova riuscita come riferimento, dichiarandola tale in caso di problemi live.
- Non mostrare .env, terminali con credenziali o informazioni riservate.

## Copione operativo

| Tempo | Azione del docente | Concetto |
|---|---|---|
| 0–2 min | Seleziona Complex Incident e Avvia / Reset | Goal, constraint, ambiente simulato |
| 2–5 min | Esegui fase — Planner | Planning, function calling, osservazioni |
| 5–7 min | Esegui fase — Resolver, fino alla pausa | Tool execution, guardrails, HITL |
| 7–9 min | Approva, poi Esegui fase — Resolver | Intervento autorizzato e handoff |
| 9–12 min | Esegui fase — Verifier | Verifica indipendente, success criteria |
| 12–15 min | Eventuale ripianificazione o riepilogo | Feedback loop, limiti, trace, token |

### 1. Missione
Dire: «L'utente assegna un risultato, non una procedura. Deve riottenere accesso al CRM senza interrompere gli altri utenti. CRM, account e sessione sono simulati; PostgreSQL e Azure OpenAI sono reali.»
Mostrare Step 0, Token 0, Planner selezionato. Il codice determina il ruolo iniziale. Il modello non conosce ancora lo stato dell'ambiente.

### 2. Planner
Premere Esegui fase. Durante l'elaborazione dire: «Il modello decide quali strumenti consultare. Non esegue direttamente il database: il backend carica lo stato, controlla il tool e restituisce l'osservazione.»
Alla pausa mostrare gli eventi della fase, le evidenze e il piano. Spiegare che il numero di chiamate e l'ordine dei tool non sono prestabiliti.
Mostrare Planner → Resolver: la regola è deterministica, il piano è prodotto dal modello. Non confondere routing con scelta del tool.

### 3. Resolver
Premere Esegui fase. Mostrare le operazioni consentite. Se appare l'approvazione: «Il modello ha richiesto una modifica, ma non può autorizzarsi da solo. Il backend sospende il processo prima di modificare lo stato.»
Premere Approva. Mostrare il risultato di unlock e la modifica dell'ambiente. Premere nuovamente Esegui fase per continuare. La sessione individuale potrebbe dover essere rigenerata. La pausa di routing indica Resolver → Verifier.

### 4. Verifier
Premere Esegui fase. Dire: «Non ci basta che il Resolver dichiari di aver risolto. Il Verifier invoca verify e il codice controlla accesso e continuità.»
Mostrare login e continuity. Se SUCCESS, mostrare lo stato finale e i token. Se la verifica fallisce, spiegare il routing verso Planner e ripetere le fasi entro il tempo disponibile. Non promettere una ripianificazione obbligatoria: il modello può identificare entrambe le anomalie subito.

### 5. Chiusura
Dire: «Il comportamento agentico è la scelta di azioni sulla base delle osservazioni. L'orchestrazione deterministica governa la collaborazione, le autorizzazioni e le condizioni di arresto. L'autonomia non elimina il controllo.»
Mostrare trace, numero di step, iterazioni e token. I token sono riportati dal provider; non rappresentano il costo monetario. Il budget è una soglia tra chiamate.

## Varianti
- Happy Path: riduce la complessità e il rischio di tempi lunghi.
- Governance Challenge: CRM offline; restart vietato; mostra escalation o limite raggiunto. Non garantire che il modello scelga restart.
- Rifiuta: mostra che l'account non viene sbloccato e la missione si arresta.

## Gestione della diretta
Usare Esegui fase come modalità principale. Prossimo step serve per approfondire una singola inferenza. Automatico mostra autonomia ma non offre pause di handoff. Pausa esecuzione ferma nuove richieste, non cancella quella già in corso. Dopo approvazione premere Esegui fase di nuovo. Se Azure non risponde o il modello si prolunga, interrompere l'avanzamento e spiegare gli eventi già osservati; non presentare una prova precedente come live.

## Limiti da dichiarare
Login e CRM sono simulati; la knowledge base è sintetica; gli agenti condividono un deployment; il piano è testo libero; il sistema è locale single-user. Il backend impone i permessi, non ruoli PostgreSQL distinti. Nessun MCP o RAG vettoriale. Il POC non è un prodotto enterprise.

## Consolidated dashboard
After each phase, use Mission Summary to distinguish login, CRM availability and absence of additional recorded interruptions. Expand Before & After and Token per agente. In Configurazione degli agenti show the actual prompts and tool catalog; export JSON before resetting. The prompt discourages conversational questions and unsupported monitoring claims. Re-test after updating. ESCALATED does not notify anyone automatically.
