# Handover Checklist — [Nome Progetto]

**Data consegna:** YYYY-MM-DD
**Versione sistema:** x.x.x
**Team di sviluppo:** [nomi]
**Referente cliente:** [nome]

---

## SISTEMA

### Ambiente di produzione

```
□ Ambiente di produzione funzionante e verificato
□ Health check eseguito e documentato
□ Performance in linea con i criteri di accettazione definiti a inizio progetto
□ Tutti i test passanti — risultati allegati
□ Validation gate eseguito — report allegato
```

**Note:**

---

### Qualità e validazione

```
□ Suite di test completa eseguita — risultati: PASS / FAIL
□ Nessuna regressione rispetto alla baseline
□ Criteri di accettazione verificati — vedere docs/acceptance-criteria.md
□ Behavioral eval eseguita (se sistema LLM/agentico) — risultati allegati
```

**Note:**

---

## DOCUMENTAZIONE

```
□ docs/architecture.md aggiornato e accurato
□ docs/runbook.md completo e testato da persona non coinvolta nel progetto
□ docs/decisions/ contiene tutti gli ADR rilevanti
□ docs/definition-of-done.md presente
□ README.md aggiornato con istruzioni di setup verificate
```

**Note:**

---

## ACCESSI E CREDENZIALI

```
□ Accessi all'ambiente di produzione trasferiti al cliente
□ Credenziali e secret trasferiti tramite canale sicuro (non email, non chat)
□ .env.example completo e documentato
□ Accessi del team di sviluppo: rimossi / documentati con scadenza
□ Repository trasferito o accesso configurato correttamente
```

**Dettaglio accessi trasferiti:**

| Sistema | Accesso | Trasferito a | Data |
|---|---|---|---|
| ... | ... | ... | ... |

---

## TRASFERIMENTO DI CONOSCENZA

```
□ Sessione di walkthrough architetturale completata con il cliente
□ Sessione di walkthrough del runbook completata con il cliente
□ Domande aperte del cliente risolte o documentate
□ Documentazione consegnata e revisionata insieme al cliente
```

**Domande aperte al momento della consegna:**

| # | Domanda | Owner | Scadenza |
|---|---|---|---|
| 1 | ... | ... | ... |

---

## POST-CONSEGNA

```
□ Periodo di hypercare definito: dal ______ al ______
□ SLA del periodo di hypercare comunicato al cliente
□ Canale di supporto post-consegna definito: ______
□ Procedura di escalation comunicata al cliente
```

---

## SIGN-OFF

### Team di sviluppo

La presente checklist è stata completata. Il sistema soddisfa tutti i criteri di accettazione definiti a inizio progetto.

| Nome | Ruolo | Firma | Data |
|---|---|---|---|
| | | | |

### Cliente

Ho ricevuto la documentazione, gli accessi e la sessione di walkthrough. Il sistema è stato consegnato in conformità ai criteri di accettazione concordati.

| Nome | Ruolo | Firma | Data |
|---|---|---|---|
| | | | |

---

## ALLEGATI

- [ ] Report di validazione: `docs/validation-report-YYYY-MM-DD.md`
- [ ] Report eval (se applicabile): `tests/evals/reports/eval-report-YYYY-MM-DD.json`
- [ ] Documento di accettazione firmato
