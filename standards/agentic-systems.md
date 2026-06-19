# Standard — Sistemi Agentici

Gli standard di questa sezione si applicano esclusivamente a sistemi agentici — sistemi in cui uno o più agenti LLM prendono decisioni e compiono azioni autonome. Integrano gli standard generali e non li sostituiscono.

I sistemi agentici richiedono standard specifici per tre caratteristiche che li differenziano da tutti gli altri sistemi:

- **Autonomia** — l'agente prende decisioni senza approvazione umana ad ogni step
- **Irreversibilità** — alcune azioni agentiche non sono annullabili
- **Non determinismo composto** — gli errori si compongono in modo non lineare su catene di azioni multiple

Per le pratiche di implementazione vedere [practices/agentic-systems.md](../practices/agentic-systems.md).

---

## S18 — Tool Safety Definition

**Ogni tool accessibile all'agente è classificato per impatto e reversibilità.**

### Classificazione obbligatoria

| Classe | Descrizione | Esempi | Vincoli |
|---|---|---|---|
| **READ** | Operazioni di sola lettura — nessun effetto collaterale | Query database, lettura file, ricerca | Nessun vincolo aggiuntivo |
| **WRITE-REV** | Scrittura reversibile — l'azione può essere annullata | Aggiornamento record, creazione ticket | Logging obbligatorio di ogni esecuzione |
| **WRITE-IRR** | Scrittura irreversibile — l'azione non può essere annullata | Invio email, eliminazione record, chiamate API esterne con effetti permanenti | Human-in-the-loop obbligatorio in produzione |

### Requisiti minimi

- Esiste un registro dei tool in `docs/tools-registry.md`
- Ogni tool ha una classificazione esplicita
- I tool WRITE-IRR non sono eseguibili senza vincoli espliciti nel codice
- Ogni tool call è loggata con parametri di input e risultato

### Criterio di accettazione

> Dato qualsiasi tool del sistema, la sua classificazione di sicurezza è documentata e i vincoli corrispondenti sono implementati nel codice, non affidati alla logica dell'LLM.

### Posizione nel repository

```
docs/tools-registry.md
```

---

## S19 — Human-in-the-Loop Gates

**I punti di approvazione umana sono definiti esplicitamente e implementati nel codice.**

### Requisiti minimi

- Esiste un diagramma del flusso agentico con i gate di approvazione esplicitamente marcati
- I gate sono implementati come logica esplicita nel codice — non delegati alla decisione dell'LLM
- In fase di deploy iniziale, tutti i tool WRITE-IRR richiedono conferma umana prima dell'esecuzione
- Ogni approvazione o rifiuto umano è tracciato con timestamp e identità dell'approvatore

### Principio di gradual autonomy

L'autonomia si guadagna empiricamente:

1. **Deploy iniziale** — approvazione umana su tutte le azioni WRITE-REV e WRITE-IRR
2. **Dopo validazione** — rimozione dei gate su WRITE-REV solo dopo documentazione empirica del comportamento corretto
3. **Autonomia completa** — solo su classi di azioni con track record documentato di comportamento corretto

La rimozione di un gate richiede un ADR con evidenza empirica a supporto.

### Criterio di accettazione

> Il diagramma del flusso agentico mostra esplicitamente tutti i gate. I gate sono verificabili nel codice senza interpretazione.

---

## S20 — Agentic Behavioral Eval

**I sistemi agentici hanno una suite di eval comportamentale specifica.**

### Requisiti minimi

La suite di eval copre obbligatoriamente questi quattro scenari:

| Scenario | Descrizione | Criterio |
|---|---|---|
| **Task completion** | Casi d'uso rappresentativi del perimetro dichiarato | L'agente completa il task correttamente con il numero atteso di step |
| **Failure handling** | Failure modes noti — tool non disponibile, risposta inattesa, timeout | L'agente gestisce il failure in modo controllato senza comportamenti anomali |
| **Out-of-scope** | Richieste fuori dal perimetro dichiarato | L'agente rifiuta o escala correttamente senza tentare di eseguire |
| **Ambiguous input** | Input ambigui o incompleti | L'agente chiede chiarimento invece di assumere e procedere |

### Requisiti aggiuntivi

- La suite è eseguita prima di ogni deploy
- I risultati sono documentati e confrontabili tra versioni
- Una regressione su qualsiasi scenario blocca il deploy

### Criterio di accettazione

> Esiste una suite di eval in `tests/evals/` con scenari documentati per tutti e quattro i tipi. I risultati dell'ultima esecuzione sono disponibili e mostrano nessuna regressione rispetto alla versione precedente.

### Posizione nel repository

```
tests/evals/
```

---

## S21 — Agentic Observability

**Ogni esecuzione agentiva è tracciata completamente — ogni step, ogni tool call, ogni decisione.**

### Requisiti minimi

Per ogni esecuzione agentiva sono tracciati obbligatoriamente:

```
- ID univoco dell'esecuzione
- Timestamp di inizio e fine
- Input ricevuto
- Sequenza di step con:
  - Tipo di step (reasoning, tool call, response)
  - Input del step
  - Output del step
  - Tool chiamato (se applicabile) con parametri e risultato
  - Token consumati nel step
  - Latenza del step
- Costo totale stimato dell'esecuzione (token + chiamate API)
- Risultato finale — successo, fallimento parziale, fallimento totale
- Motivo del fallimento se applicabile
```

### Criterio di accettazione

> Dato qualsiasi task completato o fallito, è possibile ricostruire esattamente cosa ha fatto l'agente step by step, quanto è costato e dove ha fallito, senza dover rieseguire il task.

### Non accettabile

- Logging solo del risultato finale senza traccia degli step intermedi
- Costo non monitorato
- Impossibilità di debugging post-hoc senza riesecuzione

---

## S22 — Perimeter Definition

**Ogni sistema agentico ha un perimetro di competenza esplicito e documentato.**

### Requisiti minimi

Il documento di perimetro definisce obbligatoriamente:

- **In scope** — lista esplicita dei task che il sistema supporta
- **Out of scope** — lista esplicita dei task che il sistema non supporta
- **Comportamento fuori perimetro** — risposta standard definita, non delegata all'LLM
- **Escalation path** — cosa succede quando un task è fuori scope, chi viene notificato

### Requisiti aggiuntivi

- Esistono test espliciti per le richieste fuori perimetro
- Il comportamento fuori perimetro è monitorato in produzione — le richieste fuori scope sono un segnale di gap nel perimetro dichiarato

### Criterio di accettazione

> Dato qualsiasi input fuori dal perimetro dichiarato, il sistema risponde in modo predefinito e documentato. Il comportamento è verificabile tramite test, non tramite osservazione manuale.

### Posizione nel repository

```
docs/agent-perimeter.md
```

Il template si trova in [templates/agent-perimeter.md](../templates/agent-perimeter.md).

---

## S23 — Cost Control

**I sistemi agentici hanno budget espliciti per esecuzione e meccanismi di interruzione.**

### Requisiti minimi

- Budget per esecuzione definito esplicitamente — massimo token, massimo tool calls, massimo step
- Meccanismo di interruzione implementato nel codice — quando il budget viene superato il sistema si interrompe in modo controllato, non continua indefinitamente
- Costo per task loggato per ogni esecuzione
- Alert configurato quando il costo medio per task supera una soglia definita

### Valori di default consigliati

| Parametro | Default consigliato | Note |
|---|---|---|
| Max steps per task | 10 | Aumentare solo con giustificazione documentata |
| Max tool calls per task | 15 | Include retry |
| Max token per task | Da definire per caso d'uso | Basato su analisi del task tipico |
| Alert threshold | 2x costo medio baseline | Calcolato dopo prima settimana in produzione |

### Criterio di accettazione

> Nessuna esecuzione agentiva può superare il budget definito senza essere interrotta. Il superamento del budget genera un log di WARNING con dettaglio degli step eseguiti.

### Non accettabile

- Nessun limite di step o token per esecuzione
- Costo non monitorato in produzione
- Interruzione per budget non implementata nel codice

---

## Checklist di conformità — Sistemi Agentici

Prima della consegna, verificare in aggiunta agli standard generali:

```
□ docs/tools-registry.md esiste con classificazione di sicurezza per ogni tool (S18)
□ Tool WRITE-IRR hanno vincoli espliciti implementati nel codice (S18)
□ Diagramma del flusso agentico con gate esplicitamente marcati (S19)
□ Gate implementati come logica esplicita, non delegati all'LLM (S19)
□ Suite di eval comportamentale in tests/evals/ con i quattro scenari obbligatori (S20)
□ Eval eseguita e risultati documentati senza regressioni (S20)
□ Ogni esecuzione agentiva traccia step, tool calls, token e costo (S21)
□ docs/agent-perimeter.md esiste con in-scope, out-of-scope e escalation path (S22)
□ Test espliciti per richieste fuori perimetro (S22)
□ Budget per esecuzione definito e meccanismo di interruzione implementato (S23)
□ Alert su costo configurato (S23)
```
