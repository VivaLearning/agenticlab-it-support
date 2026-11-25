# GH-600 — demo in 10–15 minuti

1. Presenta il goal e il vincolo di continuità. Spiega che CRM e login sono simulati ma PostgreSQL e chiamate LLM sono reali.
2. Seleziona Complex Incident e avvia. Mostra account bloccato e sessione non valida.
3. Prossimo step: osserva Planner e tool di lettura; spiega che il modello sceglie il tool.
4. Mostra il piano e il routing deterministico al Resolver.
5. Quando appare la richiesta di sblocco, approva. Spiega che la policy è applicata dal backend, non dal prompt.
6. Osserva Verifier: il criterio finale è il risultato del tool verify, non la dichiarazione del Resolver.
7. Se la verifica fallisce, mostra il nuovo piano. Se il modello risolve entrambi i guasti al primo giro, spiega che è un esito valido.
8. Mostra Governance Challenge: il riavvio condiviso è vietato; escalation dopo massimo tre iterazioni.
9. Chiudi con trace, token, limiti e memoria persistente.

Non presentare il test di login come autenticazione reale. La soglia token è controllata tra chiamate, non è un hard cap sul consumo totale. Questa versione è single-user, locale e senza autenticazione web.
