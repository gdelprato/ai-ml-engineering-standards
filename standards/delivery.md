# Standard — Consegna

Gli standard di questa sezione definiscono i criteri minimi verificabili per documentazione operativa, osservabilità e processo di handover. Derivano dal principio [P10](../principles/principles.md#p10--la-consegna-è-un-sistema-non-un-artefatto).

Per le pratiche di implementazione vedere [practices/delivery.md](../practices/delivery.md).

---

## S15 — Runbook

**Ogni sistema consegnato ha un runbook operativo completo.**

### Requisiti minimi

Il runbook risponde obbligatoriamente a queste domande:

- Come si avvia il sistema
- Come si verifica che il sistema stia funzionando correttamente
- Come si esegue un aggiornamento
- Cosa fare quando qualcosa va storto — almeno i tre failure modes più probabili con procedura di risoluzione
- Chi contattare e come in caso di incident

### Criterio di accettazione

> Un operatore che non ha mai visto il sistema riesce ad avviarlo, verificarne il funzionamento e gestire un failure comune seguendo solo il runbook, senza contattare il team di sviluppo.

### Posizione nel repository

```
docs/runbook.md
```

### Non accettabile

- Runbook generico non specifico al sistema consegnato
- Runbook non testato da chi non ha lavorato al progetto
- Procedure di troubleshooting assenti o non verificate

---

## S16 — Observability Minimum

**Ogni sistema in produzione ha logging strutturato, metriche di base e alerting su failure critici.**

### Requisiti minimi

**Logging**
- Logging strutturato — formato JSON, non stringhe libere
- Log levels coerenti e usati correttamente — DEBUG, INFO, WARNING, ERROR, CRITICAL
- Ogni evento critico del sistema genera un log con contesto sufficiente per il debugging
- Nessuna informazione sensibile nei log — PII, credenziali, dati riservati

**Metriche**
- Latenza delle operazioni principali monitorata
- Tasso di errore monitorato
- Almeno una metrica di business rilevante per il cliente monitorata

**Alerting**
- Alert attivo su failure critici — il sistema notifica proattivamente, non aspetta che qualcuno se ne accorga
- Soglie di alert documentate e giustificate
- Destinatari degli alert definiti esplicitamente

### Criterio di accettazione

> Dato un failure critico avvenuto in produzione, è possibile identificare cosa è successo, quando e perché leggendo i log. Gli alert hanno notificato il problema prima che il cliente lo segnalasse.

### Non accettabile

- Logging solo su stdout senza struttura
- Nessun alerting su failure critici
- Metriche solo tecniche senza correlazione con il valore di business

---

## S17 — Handover Checklist

**Prima di ogni consegna finale esiste una handover checklist completata e firmata.**

### Checklist obbligatoria

```
SISTEMA
□ Ambiente di produzione funzionante e verificato
□ Tutti i test passanti — risultati documentati
□ Validation gate eseguito e documentato
□ Performance in linea con i criteri di accettazione definiti a inizio progetto

DOCUMENTAZIONE
□ Architecture document aggiornato e accurato
□ Runbook completo e testato
□ ADR aggiornati
□ Definition of Done verificata su tutti i task

ACCESSI E CREDENZIALI
□ Accessi al sistema trasferiti al cliente
□ Credenziali e secret trasferiti in modo sicuro
□ Accessi del team di sviluppo rimossi o documentati

TRASFERIMENTO DI CONOSCENZA
□ Sessione di walkthrough completata con il cliente
□ Documentazione operativa consegnata e revisionata con il cliente
□ Domande aperte del cliente risolte o documentate

POST-CONSEGNA
□ Piano di supporto post-consegna definito e comunicato
□ Canale di escalation definito
□ Periodo di hypercare definito se applicabile
```

### Criterio di accettazione

> La checklist è completata, ogni voce è verificata, e il cliente ha firmato il documento di accettazione prima che il progetto venga considerato chiuso.

### Posizione nel repository

```
docs/handover-checklist.md
```

Il template si trova in [templates/handover-checklist.md](../templates/handover-checklist.md).

---

## Checklist di conformità

Prima della consegna, verificare:

```
□ docs/runbook.md esiste, è completo e testato (S15)
□ Logging strutturato attivo su tutti i componenti critici (S16)
□ Alert configurati su failure critici (S16)
□ Almeno una metrica di business monitorata (S16)
□ Handover checklist completata e firmata (S17)
□ Sessione di walkthrough completata con il cliente (S17)
```
