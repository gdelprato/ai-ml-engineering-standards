# Perimetro Operativo — [Nome Agente]

**Versione:** x.x.x
**Ultima modifica:** YYYY-MM-DD
**Autore:** [nome]
**Sistema di riferimento:** [nome sistema]

---

## In scope

Task che il sistema supporta esplicitamente.

| # | Task | Descrizione | Criterio di completamento |
|---|---|---|---|
| 1 | [nome task] | Cosa fa | Come si verifica che sia fatto correttamente |
| 2 | ... | ... | ... |

---

## Out of scope

Task che il sistema NON supporta. Esplicito e non negoziabile.

| # | Task | Motivo dell'esclusione |
|---|---|---|
| 1 | [nome task] | Perché non è supportato |
| 2 | ... | ... |

---

## Comportamento fuori perimetro

### Risposta standard

Quando il sistema riceve una richiesta fuori scope, risponde sempre con:

> "[Testo esatto della risposta standard — non delegato all'LLM]"

### Escalation path

Cosa succede dopo la risposta standard:

- Logging della richiesta fuori scope con categoria
- [Notifica / redirect / nessuna azione aggiuntiva]
- Canale di escalation per l'utente: [specificare]

---

## Edge cases documentati

Casi limite con comportamento atteso esplicito.

| Caso | Input esempio | Comportamento atteso |
|---|---|---|
| Input vuoto | "" | [comportamento] |
| Input molto lungo | > N caratteri | [comportamento] |
| Input ambiguo tra scope e out-of-scope | [esempio] | [comportamento] |
| Input in lingua non supportata | [esempio] | [comportamento] |

---

## Limiti operativi

Vincoli tecnici che definiscono i limiti di operatività del sistema.

| Parametro | Valore | Note |
|---|---|---|
| Lunghezza massima input | N caratteri | |
| Timeout per task | N secondi | |
| Max step per esecuzione | N | Vedere cost control |
| Lingue supportate | [lista] | |

---

## Monitoring fuori perimetro

Le richieste fuori perimetro vengono loggate con:

```json
{
  "event": "out_of_scope_request",
  "request_category": "[categoria identificata]",
  "request_preview": "[primi 100 caratteri]",
  "timestamp": "ISO8601"
}
```

Questo log è la fonte primaria per la review periodica del perimetro.

---

## Review del perimetro

Il perimetro viene rivisto ogni trimestre sulla base dei dati di produzione.

| Data review | Modifiche | Autore |
|---|---|---|
| YYYY-MM-DD | Versione iniziale | [nome] |
