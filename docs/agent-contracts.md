# Contratti degli agenti e degli strumenti
| Agente | Input | Responsabilità | Output |
|---|---|---|---|
| Planner | Missione, vincoli; evidenze in ripianificazione | Diagnosi e piano | Testo operativo |
| Resolver | Piano del Planner | Selezione ed esecuzione tool autorizzati | Resoconto operativo |
| Verifier | Resoconto del Resolver | Test indipendente | Esito narrativo e osservazione verify |
| Orchestratore | Stato, output e risultati | Routing, limiti, approvazioni, terminazione | Stato e eventi |
Il piano è testo libero, non un contratto JSON validato. Il ruolo viene imposto dal backend. Ogni chiamata include il system prompt del ruolo e i messaggi di quella fase. Il passaggio di ruolo sostituisce i messaggi con il contesto trasferito. Le evidenze restano persistenti e vengono reinviate in caso di ripianificazione.
## Tool
| Nome | Planner | Resolver | Verifier | Effetto |
|---|---|---|---|---|
| knowledge | sì | no | no | Cause sintetiche codificate in Python |
| account | sì | sì | no | locked |
| session | sì | sì | no | valid |
| service | sì | sì | sì | online, active_users |
| unlock | no | sì | no | Sblocca dopo approvazione |
| refresh_session | no | sì | no | Rende valida la sessione se account sbloccato |
| restart | no | sì | no | Sempre negato dalla policy del POC |
| verify | no | no | sì | login e continuity |
Gli argomenti sono oggetti vuoti: il laboratorio ha un solo utente target. Il modello produce la richiesta function call; Python esegue il tool. L'autorizzazione è applicata anche lato server.
## Condizioni di successo
login = account non bloccato AND sessione valida AND CRM online. continuity = interruptions uguale a zero. L'orchestratore richiede una chiamata verify nella fase corrente e ricalcola i due booleani. Non si fida della sola risposta testuale del Verifier.
## Approvazione
unlock su account bloccato sospende il processo; il docente approva o rifiuta. Il rifiuto conclude in ESCALATED. L'approvazione non riprende automaticamente il loop della UI: premere Esegui fase per continuare.
## Estensioni
Per un sistema reale: output strutturati validati, argomenti tool con schema rigoroso e validazione, autenticazione e autorizzazioni indipendenti, idempotenza, audit, gestione robusta dei timeout, isolamento delle missioni, valutazioni automatiche e controlli sul contenuto non attendibile.
