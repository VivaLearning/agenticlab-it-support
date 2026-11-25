# Scenari e criteri di collaudo
| Scenario | Account bloccato | Sessione valida | CRM online | Utenti | Interruzioni |
|---|---|---|---|---|---|
| happy | true | true | true | 42 | 0 |
| complex | true | false | true | 42 | 0 |
| governance | true | false | false | 42 | 0 |
## Happy Path
Avvia, esegui Planner, esegui Resolver fino all'approvazione, approva e riprendi, esegui Verifier. Atteso SUCCESS se il modello seleziona gli strumenti necessari e verify conferma entrambe le condizioni.
## Complex Incident
Scenario principale. Evidenziare due anomalie e il rischio di un intervento globale. Se il primo piano è incompleto, il Verifier dovrebbe rilevare login=false e l'orchestratore ripianificare. Se il piano iniziale è completo, non forzare la ripianificazione: è un risultato valido.
## Governance Challenge
CRM offline. Il tool restart restituisce DENIED indipendentemente dall'approvazione. Nessun tool può riportare il CRM online. Non attendersi SUCCESS. Possibili escalation, limite step/token o errore. Non è garantito che il modello tenti restart.
## Rifiuto umano
In Happy o Complex, quando appare unlock, premere Rifiuta. Atteso ESCALATED, account ancora bloccato. Il rifiuto conclude la missione.
## Checklist di accettazione
- Un click Esegui fase non attiva la fase successiva.
- Il cambio agente mostra from/to e la ragione deterministica.
- L'approvazione interrompe fase e automatico.
- Durante l'elaborazione i pulsanti di avanzamento sono disabilitati.
- Stop impedisce nuove richieste ma non annulla quella in corso.
- Verify deve essere invocato per SUCCESS; login e continuity devono essere true.
- Reset crea una nuova missione e azzera i contatori visualizzati.
- I token provengono dalle risposte LLM, non sono valori simulati.
- Nessuna azione modifica un CRM reale.
Registrare esito, scenario e trace. I test unitari coprono soltanto il dominio; questa checklist richiede il browser e l'integrazione reale.
