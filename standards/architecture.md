# Standard — Architettura e Decisioni

Gli standard di questa sezione definiscono i criteri minimi verificabili per architettura e tracciabilità delle decisioni tecniche. Derivano dai principi [P01](../principles/principles.md#p01--larchitettura-prima-del-codice) e [P02](../principles/principles.md#p02--ogni-decisione-tecnica-è-tracciata).

Per le pratiche di implementazione vedere [practices/architecture.md](../practices/architecture.md).

---

## S01 — Architecture Document

**In ogni progetto esiste un documento di architettura aggiornato.**

### Requisiti minimi

- Descrive i componenti principali del sistema e le loro responsabilità
- Descrive i flussi di dati e le integrazioni esterne
- Documenta i vincoli tecnici principali
- È aggiornato — riflette lo stato reale del sistema, non l'intenzione iniziale
- È leggibile da un membro del team non coinvolto nel progetto

### Criterio di accettazione

> Un ingegnere che non ha lavorato al progetto è in grado di descrivere correttamente l'architettura del sistema dopo aver letto il documento, senza aver visto il codice.

### Posizione nel repository

```
docs/architecture.md
```

### Stato obbligatorio

**Obbligatorio prima di scrivere codice di produzione.** Non è documentazione da aggiungere a fine progetto.

---

## S02 — Architecture Decision Records

**Ogni decisione tecnica rilevante è documentata come ADR.**

### Requisiti minimi

- Esiste almeno un ADR per ogni decisione che sarebbe costosa da invertire
- Ogni ADR include: contesto, decisione, alternative considerate, conseguenze
- Gli ADR sono scritti prima di implementare la decisione, non dopo
- Gli ADR non vengono modificati retroattivamente — le revisioni generano nuovi ADR

### Soglia di rilevanza

Una decisione richiede un ADR se soddisfa almeno uno di questi criteri:

- Impatta l'architettura complessiva del sistema
- Introduce una dipendenza esterna significativa
- Sceglie un approccio tra alternative tecnicamente equivalenti
- Ha conseguenze difficilmente reversibili
- Potrebbe essere messa in discussione in futuro senza contesto

### Criterio di accettazione

> Data una qualsiasi decisione architetturale rilevante del progetto, esiste un ADR che spiega perché è stata presa quella decisione e non un'alternativa.

### Posizione nel repository

```
docs/decisions/ADR-NNN-titolo-decisione.md
```

### Stato obbligatorio

**Obbligatorio.** Minimo un ADR per progetto. Nessun limite massimo.

---

## Checklist di conformità

Prima della consegna, verificare:

```
□ docs/architecture.md esiste ed è aggiornato
□ docs/architecture.md descrive componenti, flussi e vincoli
□ docs/decisions/ contiene almeno un ADR
□ Ogni decisione rilevante ha un ADR corrispondente
□ Gli ADR sono stati scritti prima dell'implementazione
```
