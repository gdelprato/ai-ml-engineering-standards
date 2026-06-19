# Production Ready

Il livello Production Ready si applica a tutti i sistemi che vengono deployati in produzione con utenti reali. Include tutti gli standard Foundation e aggiunge i requisiti necessari per operare un sistema in modo affidabile e sostenibile nel tempo.

---

## Definizione

> Un progetto Production Ready garantisce che il sistema sia **validato, osservabile e operabile** in produzione, con qualità del codice verificata automaticamente e riproducibilità completa di ambienti, dati ed esperimenti.

---

## Prerequisito

**Tutti i criteri Foundation devono essere soddisfatti prima di verificare i criteri Production Ready.**

---

## Checklist di conformità

*In aggiunta a tutti i criteri Foundation.*

### Architettura

```
□ S02 — ADR per ogni decisione tecnica rilevante
         Posizione: docs/decisions/
         Criterio: ogni decisione costosa da invertire ha un ADR con contesto e alternative
```

### Qualità del codice

```
□ S06 — Code quality automatizzata con pre-commit hooks attivi
         Criterio: impossibile committare codice non conforme a linting e formatting
```

### Riproducibilità

```
□ S07 — Environment reproducibility verificata da persona non coinvolta nel progetto
         Criterio: setup completato in meno di 30 minuti seguendo solo il README

□ S08 — Data reproducibility — raw immutabile, trasformazioni come codice versionato
         Criterio: training rieseguibile con risultati comparabili da qualsiasi membro del team

□ S09 — Experiment tracking attivo su tutti gli esperimenti rilevanti
         Tool: MLflow
         Criterio: ogni decisione di modello è giustificata da un run tracciato con parametri e metriche

□ S10 — Validation gates con criteri di accettazione definiti prima dell'inizio del progetto
         Criterio: report di validazione documentato e firmato prima di ogni deploy
```

### Consegna

```
□ S16 — Logging strutturato attivo su tutti i componenti critici
         Criterio: dato un failure, causa e contesto identificabili dai log senza riesecuzione

□ S16 — Alerting configurato su failure critici
         Criterio: il sistema notifica proattivamente prima che il cliente segnali il problema
```

---

## Artefatti obbligatori

*In aggiunta agli artefatti Foundation.*

| Artefatto | Posizione | Standard |
|---|---|---|
| ADR (almeno uno) | `docs/decisions/` | S02 |
| Pre-commit config | `.pre-commit-config.yaml` | S06 |
| Acceptance criteria | `docs/acceptance-criteria.md` | S10 |
| Validation report | `docs/validation-report-YYYY-MM-DD.md` | S10 |

---

## Criteri di esclusione

Un progetto **non è Production Ready** se anche uno solo di questi è vero:

- Nessun ADR per decisioni architetturali rilevanti
- Pre-commit hooks non configurati o disabilitati
- Setup non verificato da persona non coinvolta nel progetto
- Dati raw modificati manualmente
- Nessun experiment tracking su progetti di modeling
- Criteri di accettazione non definiti prima dell'inizio del progetto
- Nessun logging strutturato sui componenti critici
- Nessun alerting su failure critici

---

## Riferimenti

- Standard dettagliati: [`standards/`](../standards/)
- Pratiche di implementazione: [`practices/`](../practices/)
- Livello inferiore: [`levels/foundation.md`](foundation.md)
- Livello superiore: [`levels/enterprise-grade.md`](enterprise-grade.md)

