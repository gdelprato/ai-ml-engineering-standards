# Pratiche — Consegna

Questa sezione definisce come implementare gli standard [S15](../standards/delivery.md#s15--runbook), [S16](../standards/delivery.md#s16--observability-minimum) e [S17](../standards/delivery.md#s17--handover-checklist).

---

## P15 — Runbook

### Minimo

File `docs/runbook.md` basato sul template in [templates/runbook-template.md](../templates/runbook-template.md).

**Sezioni obbligatorie:**

```markdown
# Runbook — [Nome Sistema]

**Versione:** x.x.x
**Ultimo aggiornamento:** YYYY-MM-DD
**Owner:** [nome o team]

## Avvio del sistema

Prerequisiti, comandi di avvio, verifica che il sistema sia operativo.

## Verifica operatività

Come verificare che il sistema stia funzionando correttamente.
Quale output o risposta indica stato healthy.

## Aggiornamento

Come eseguire un aggiornamento. Step-by-step, incluso rollback.

## Troubleshooting

### [Problema 1 — titolo descrittivo]
**Sintomo:** come si manifesta
**Causa probabile:** perché succede
**Risoluzione:** step per risolvere

### [Problema 2]
...

## Escalation

A chi rivolgersi se il problema non si risolve con questo runbook.
Canale di contatto e tempi di risposta attesi.
```

**Verifica obbligatoria:** il runbook viene testato da un membro del team che non ha lavorato al progetto prima della consegna.

### Consigliato

- Sezione di troubleshooting popolata con problemi reali incontrati durante lo sviluppo e il testing
- Comandi copia-incollabili — nessun comando che richiede interpretazione
- Sezione changelog del runbook — quando è stato aggiornato e perché

### Avanzato

- Runbook come documento vivo aggiornato obbligatoriamente dopo ogni incident
- Runbook review periodica per verificare accuratezza con il sistema reale

---

## P16 — Observability

### Minimo

**Logging strutturato con `structlog`:**

```python
import structlog

log = structlog.get_logger()

# Configurazione obbligatoria all'avvio
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# Utilizzo corretto
log.info(
    "ticket_processed",
    ticket_id=ticket_id,
    priority=priority,
    duration_ms=duration,
    model_version="v2.1",
)

log.error(
    "tool_call_failed",
    tool_name="update_ticket",
    error_type=type(e).__name__,
    ticket_id=ticket_id,
    attempt=attempt,
)
```

**Log levels — utilizzo corretto:**

| Level | Quando usarlo |
|---|---|
| DEBUG | Informazioni di debugging — non in produzione |
| INFO | Eventi normali del flusso operativo |
| WARNING | Situazione inattesa ma gestita — il sistema continua |
| ERROR | Errore che impatta un'operazione specifica |
| CRITICAL | Errore che impatta il funzionamento del sistema |

**Informazioni vietate nei log:**

- PII — nomi, email, numeri di telefono, indirizzi
- Credenziali — password, token, chiavi API
- Dati sensibili di business non necessari al debugging

### Consigliato

**Metriche con Prometheus:**

```python
from prometheus_client import Counter, Histogram, start_http_server

# Definizione metriche
TICKETS_PROCESSED = Counter(
    "tickets_processed_total",
    "Numero totale di ticket processati",
    ["status", "priority"],
)

PROCESSING_DURATION = Histogram(
    "ticket_processing_duration_seconds",
    "Durata del processing dei ticket",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
)

# Utilizzo
TICKETS_PROCESSED.labels(status="success", priority="high").inc()

with PROCESSING_DURATION.time():
    result = process_ticket(ticket)
```

- Dashboard Grafana con almeno: tasso di successo, latenza p50/p95/p99, volume per unità di tempo
- Alert su: tasso di errore > soglia, latenza p95 > soglia, volume anomalo

### Avanzato

- Distributed tracing con OpenTelemetry per sistemi multi-componente
- Anomaly detection automatica su metriche chiave
- SLO (Service Level Objectives) definiti e monitorati

---

## P17 — Handover

### Minimo

Utilizzare il template in [templates/handover-checklist.md](../templates/handover-checklist.md).

**Processo di handover in tre step:**

**Step 1 — Preparazione (1 settimana prima)**
- Completare tutta la documentazione
- Testare il runbook su ambiente pulito
- Preparare i materiali per la sessione di walkthrough

**Step 2 — Walkthrough con il cliente**
- Presentare l'architettura del sistema
- Eseguire il runbook insieme al cliente
- Rispondere alle domande tecniche
- Identificare e documentare le domande aperte

**Step 3 — Sign-off formale**
- Completare la checklist di handover
- Ottenere firma del cliente sul documento di accettazione
- Trasferire accessi e credenziali
- Definire il periodo di hypercare e il canale di supporto

### Consigliato

- Periodo di hypercare di almeno 2 settimane post-consegna con SLA definito
- Sessione di retrospettiva post-consegna per identificare miglioramenti al processo

### Avanzato

- Metrica di time-to-autonomy — tempo che il cliente impiega per operare il sistema senza supporto
- Feedback strutturato del cliente usato come input per aggiornare gli standard
