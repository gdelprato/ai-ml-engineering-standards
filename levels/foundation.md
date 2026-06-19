# Foundation

Il livello Foundation definisce gli standard minimi non negoziabili per ogni progetto della practice, indipendentemente da dimensione, durata o tipologia.

Un progetto che non soddisfa tutti i criteri Foundation non è pronto per la consegna.

---

## Definizione

> Un progetto Foundation garantisce che il lavoro sia **riproducibile, tracciabile e consegnabile** da qualsiasi membro del team, indipendentemente da chi lo ha sviluppato.

---

## Checklist di conformità

### Architettura

```
□ S01 — Architecture document esistente e aggiornato prima di scrivere codice di produzione
         Posizione: docs/architecture.md
         Criterio: un ingegnere non coinvolto descrive correttamente il sistema dopo la lettura
```

### Qualità del codice

```
□ S03 — Repository structure conforme allo standard
         Criterio: struttura verificata rispetto a standards/code-quality.md#s03

□ S04 — Dependency management con versioni esplicite e lock file committato
         Criterio: ambiente ricostruibile con un singolo comando

□ S05 — Configuration management — nessun valore hardcoded, nessun secret committato
         Criterio: scansione automatica non rileva secret. .env.example completo
```

### Gestione del lavoro

```
□ S11 — Issue tracking attivo — ogni task esiste come issue prima di essere iniziato
         Criterio: stato del progetto leggibile dalla board senza interrogare il team

□ S12 — Commit convention rispettata su tutti i commit
         Criterio: ogni commit ha tipo, scope, descrizione e riferimento all'issue

□ S13 — Branch strategy rispettata — nessun commit diretto su main
         Criterio: storia di main contiene solo merge da MR approvate

□ S14 — Definition of Done esistente e applicata
         Posizione: docs/definition-of-done.md
```

### Consegna

```
□ S15 — Runbook completo e testato
         Posizione: docs/runbook.md
         Criterio: operatore non coinvolto riesce a gestire il sistema seguendo solo il runbook

□ S17 — Handover checklist completata e firmata prima della consegna finale
         Posizione: docs/handover-checklist.md
```

---

## Artefatti obbligatori

| Artefatto | Posizione | Standard |
|---|---|---|
| Architecture document | `docs/architecture.md` | S01 |
| Repository structure | Root del progetto | S03 |
| Lock file dipendenze | Root del progetto | S04 |
| `.env.example` | Root del progetto | S05 |
| Definition of Done | `docs/definition-of-done.md` | S14 |
| Runbook | `docs/runbook.md` | S15 |
| Handover checklist | `docs/handover-checklist.md` | S17 |

---

## Criteri di esclusione

Un progetto **non è Foundation** se anche uno solo di questi è vero:

- Non esiste un architecture document al momento della consegna
- Il repository contiene secret o valori hardcoded
- I task non sono tracciati in un sistema di issue tracking
- Il runbook non è stato testato da persona non coinvolta nel progetto
- La handover checklist non è stata completata e firmata

---

## Riferimenti

- Standard dettagliati: [`standards/`](../standards/)
- Pratiche di implementazione: [`practices/`](../practices/)
- Template: [`templates/`](../templates/)
