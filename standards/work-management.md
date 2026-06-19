# Standard — Gestione del Lavoro

Gli standard di questa sezione definiscono i criteri minimi verificabili per tracking dei task, convenzioni di commit, branch strategy e definition of done. Derivano dai principi [P07](../principles/principles.md#p07--ogni-task-è-esplicito-tracciato-e-collegato-al-suo-contesto), [P08](../principles/principles.md#p08--il-codice-è-sempre-collegato-a-un-task) e [P09](../principles/principles.md#p09--il-workflow-di-sviluppo-è-definito-e-condiviso).

Per le pratiche di implementazione vedere [practices/work-management.md](../practices/work-management.md).

---

## S11 — Issue Tracking

**Ogni attività di sviluppo esiste come issue prima di essere iniziata.**

### Requisiti minimi

- Ogni progetto ha un sistema di tracking attivo — GitLab Issues come default
- Ogni attività di sviluppo — feature, bug, spike, refactor, eval — è un'issue prima di essere iniziata
- Ogni issue include: titolo chiaro, descrizione del problema o obiettivo, criterio di completamento
- Lo stato del progetto è leggibile dal sistema senza dover interrogare i membri del team
- La board ha stati espliciti — minimo: Backlog, In Progress, In Review, Done

### Criterio di accettazione

> Aprendo la board del progetto, è possibile capire lo stato reale del lavoro senza chiedere a nessuno.

### Non accettabile

- Task gestiti in chat, email o a memoria
- Issue create dopo che il lavoro è già stato iniziato
- Board non aggiornata che non riflette lo stato reale

---

## S12 — Commit Convention

**Ogni commit ha un messaggio strutturato con riferimento al task collegato.**

### Formato obbligatorio

```
<type>(<scope>): <descrizione breve>

<corpo opzionale>

Refs: #<issue-number>
```

### Tipi ammessi

| Tipo | Quando usarlo |
|---|---|
| `feat` | Nuova funzionalità |
| `fix` | Correzione di bug |
| `refactor` | Refactoring senza cambiamento di comportamento |
| `test` | Aggiunta o modifica di test |
| `docs` | Modifiche alla documentazione |
| `chore` | Manutenzione, aggiornamento dipendenze |
| `eval` | Aggiunta o modifica di eval LLM/agentiche |

### Esempi

```
feat(agent): add tool call retry logic with exponential backoff

Refs: #42

fix(data): correct null handling in preprocessing pipeline

Refs: #67

docs(architecture): update diagram to reflect new tool registry

Refs: #51
```

### Criterio di accettazione

> Da qualsiasi commit è possibile risalire all'issue che lo ha generato e capire il perché della modifica.

### Non accettabile

- Commit senza riferimento a un'issue
- Messaggi generici: "fix", "update", "wip", "misc"
- Commit che mixano modifiche non correlate

---

## S13 — Branch Strategy

**Esiste una branch strategy esplicita. Nessun lavoro diretto su `main`.**

### Struttura obbligatoria

| Branch | Descrizione | Regole |
|---|---|---|
| `main` | Branch principale — sempre stabile e deployabile | Nessun commit diretto. Merge solo da `develop` tramite MR approvata. |
| `develop` | Branch di integrazione | Merge da feature branch tramite MR. |
| `feature/<issue-id>-<nome>` | Branch di sviluppo per singolo task | Creata da `develop`. Merge su `develop` tramite MR. |
| `fix/<issue-id>-<nome>` | Branch per bug fix | Creata da `develop` o `main`. Merge tramite MR. |

### Esempi di naming

```
feature/42-agent-retry-logic
fix/67-null-handling-preprocessing
refactor/51-tool-registry-structure
```

### Regole non negoziabili

- Nessun commit diretto su `main`
- Ogni merge su `main` richiede una Merge Request approvata
- Le branch vengono cancellate dopo il merge
- Branch protection rules attive su GitLab per `main`

### Criterio di accettazione

> La storia di `main` contiene solo merge commit da MR approvate. Nessun commit diretto.

---

## S14 — Definition of Done

**Ogni progetto ha una Definition of Done esplicita e condivisa.**

### Requisiti minimi della DoD

Un task è Done quando soddisfa tutti questi criteri:

```
□ Codice revisionato e approvato da almeno un altro membro del team
□ Test pertinenti scritti e passanti — unit e/o integration a seconda del task
□ Documentazione aggiornata se il task introduce o modifica comportamento pubblico
□ Nessun warning o errore di linting
□ Issue collegata aggiornata e chiusa
□ Branch cancellata dopo il merge
```

### Estensione per task ML/AI

```
□ Esperimento tracciato con parametri e metriche (se task di modeling)
□ Eval aggiornata se il task modifica comportamento del modello o dell'agente
□ Validation gate eseguito e documentato (se task impatta il sistema in produzione)
```

### Posizione nel repository

```
docs/definition-of-done.md
```

### Criterio di accettazione

> Nessun task viene marcato Done senza che tutti i criteri della DoD siano verificati. La DoD è applicata sistematicamente, non a discrezione del singolo.

---

## Checklist di conformità

Prima della consegna, verificare:

```
□ GitLab Issues attivo con tutti i task tracciati (S11)
□ Board aggiornata e che riflette lo stato reale (S11)
□ Tutti i commit seguono la convention con riferimento all'issue (S12)
□ Branch strategy rispettata — nessun commit diretto su main (S13)
□ Branch protection rules attive su GitLab (S13)
□ docs/definition-of-done.md esiste ed è stato applicato (S14)
```
