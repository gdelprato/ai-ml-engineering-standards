# Runbook — [Nome Sistema]

**Versione sistema:** x.x.x
**Ultimo aggiornamento:** YYYY-MM-DD
**Owner:** [nome o team]
**Canale di supporto:** [canale — Slack, email, ticket system]

---

## Prerequisiti operativi

Cosa deve essere disponibile prima di operare il sistema.

- Accessi richiesti: [lista]
- Tool richiesti: [lista]
- Documentazione correlata: [link]

---

## Avvio del sistema

### Ambiente di produzione

```bash
# Comandi esatti copia-incollabili
```

### Verifica avvio corretto

Come verificare che il sistema sia partito correttamente.

**Output atteso:**

```
[output che indica stato healthy]
```

**Output che indica problema:**

```
[output che indica stato unhealthy — procedere al troubleshooting]
```

---

## Verifica operatività

Come verificare che il sistema stia funzionando correttamente durante l'operazione normale.

```bash
# Comando di health check
```

**Risposta attesa:**

```json
{
  "status": "healthy",
  "...": "..."
}
```

---

## Aggiornamento

### Pre-aggiornamento

- [ ] Verificare che il sistema sia in stato healthy
- [ ] Notificare gli utenti se l'aggiornamento comporta downtime
- [ ] Creare backup se applicabile

### Procedura di aggiornamento

```bash
# Step 1
# Step 2
# Step 3
```

### Verifica post-aggiornamento

```bash
# Verificare che il sistema sia tornato healthy
```

### Rollback

Se l'aggiornamento fallisce:

```bash
# Procedura di rollback
```

---

## Troubleshooting

### [Problema 1 — titolo descrittivo]

**Sintomo:** Come si manifesta. Cosa vede l'utente o l'operatore.

**Causa probabile:** Perché succede tipicamente.

**Risoluzione:**

```bash
# Comandi per diagnosticare
# Comandi per risolvere
```

**Se non risolto:** Procedere a [Problema correlato] o escalare a [contatto].

---

### [Problema 2 — titolo descrittivo]

**Sintomo:** ...

**Causa probabile:** ...

**Risoluzione:**

```bash
# ...
```

---

### [Problema 3 — titolo descrittivo]

**Sintomo:** ...

**Causa probabile:** ...

**Risoluzione:**

```bash
# ...
```

---

## Monitoraggio

### Metriche chiave

| Metrica | Valore normale | Soglia di alert | Azione |
|---|---|---|---|
| Metrica A | [range] | [soglia] | [cosa fare] |
| Metrica B | [range] | [soglia] | [cosa fare] |

### Dashboard

[Link alla dashboard operativa se disponibile]

---

## Escalation

| Situazione | Contatto | Canale | SLA risposta |
|---|---|---|---|
| Failure critico | [nome] | [canale] | [tempo] |
| Degradazione performance | [nome] | [canale] | [tempo] |
| Domanda operativa | [nome] | [canale] | [tempo] |

---

## Changelog runbook

| Data | Modifica | Autore |
|---|---|---|
| YYYY-MM-DD | Versione iniziale | [nome] |
