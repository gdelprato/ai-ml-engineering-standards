# Enterprise Grade

Il livello Enterprise Grade si applica a sistemi critici per il business, ad alta scalabilità, con requisiti di governance, compliance o autonomia agentiva. Include tutti gli standard Production Ready e aggiunge i requisiti necessari per operare a livello enterprise.

---

## Definizione

> Un progetto Enterprise Grade garantisce che il sistema sia **governabile, auditabile e sostenibile** a scala organizzativa, con osservabilità completa, gestione esplicita dell'autonomia agentiva e controllo dei costi.

---

## Prerequisito

**Tutti i criteri Production Ready — e quindi Foundation — devono essere soddisfatti prima di verificare i criteri Enterprise Grade.**

---

## Checklist di conformità

*In aggiunta a tutti i criteri Production Ready.*

### Osservabilità avanzata

```
□ S16 avanzato — Metriche di business monitorate in produzione
                  Criterio: almeno un KPI di business correlato alle metriche tecniche

□ SLO definiti e monitorati
   Criterio: Service Level Objectives documentati, misurati e comunicati al cliente
   Posizione: docs/slo.md
```

### Model governance

```
□ S09 avanzato — Model registry con promozione controllata
                  Tool: MLflow Model Registry
                  Criterio: ogni modello in produzione è registrato con versione,
                            provenienza e criteri di promozione documentati

□ Security e compliance documentate
   Criterio: documento esplicito su gestione dati sensibili, superfici di attacco
             e conformità ai requisiti del cliente
   Posizione: docs/security.md
```

### Sistemi agentici
*Applicabile solo a progetti con componenti agentiche. Obbligatorio se il sistema include agenti LLM.*

```
□ S18 — Tool safety classification completa
         Criterio: ogni tool classificato READ / WRITE-REV / WRITE-IRR
                   con vincoli implementati nel codice
         Posizione: docs/tools-registry.md

□ S19 — Human-in-the-loop gates espliciti e implementati nel codice
         Criterio: gate documentati nel diagramma e verificabili nel codice
                   senza interpretazione

□ S20 — Behavioral eval suite completa con i quattro scenari obbligatori
         Criterio: suite eseguita prima di ogni deploy senza regressioni
         Posizione: tests/evals/

□ S21 — Agentic observability completa — ogni step, tool call, token e costo tracciati
         Criterio: qualsiasi esecuzione ricostruibile step by step post-hoc

□ S22 — Perimeter definition esplicita con comportamento fuori scope implementato nel codice
         Posizione: docs/agent-perimeter.md

□ S23 — Cost control con budget per esecuzione e meccanismo di interruzione
         Criterio: nessuna esecuzione può superare il budget senza essere interrotta
```

---

## Artefatti obbligatori

*In aggiunta agli artefatti Production Ready.*

| Artefatto | Posizione | Standard | Condizione |
|---|---|---|---|
| SLO document | `docs/slo.md` | SLO | Sempre |
| Security document | `docs/security.md` | Compliance | Sempre |
| Tools registry | `docs/tools-registry.md` | S18 | Solo sistemi agentici |
| Agent perimeter | `docs/agent-perimeter.md` | S22 | Solo sistemi agentici |
| Agentic eval suite | `tests/evals/` | S20 | Solo sistemi agentici |

---

## Criteri di esclusione

Un progetto **non è Enterprise Grade** se anche uno solo di questi è vero:

- Nessuna metrica di business monitorata in produzione
- SLO non definiti o non misurati
- Nessun model registry per modelli in produzione
- Security e compliance non documentate
- Per sistemi agentici: tool non classificati per safety
- Per sistemi agentici: gate human-in-the-loop delegati alla logica dell'LLM
- Per sistemi agentici: nessuna behavioral eval suite
- Per sistemi agentici: esecuzioni senza budget e meccanismo di interruzione

---

## Nota sui sistemi agentici

Gli standard S18–S23 sono **obbligatori** per qualsiasi sistema con componenti agentiche a livello Enterprise Grade. Non sono opzionali anche se il sistema è considerato "a basso rischio".

La classificazione di rischio di un sistema agentico non è una valutazione soggettiva — è determinata dalla presenza di tool WRITE-IRR e dalla conseguente irreversibilità di alcune azioni. Se il sistema ha tool irreversibili, gli standard agentici si applicano integralmente.

---

## Riferimenti

- Standard dettagliati: [`standards/`](../standards/)
- Pratiche di implementazione: [`practices/`](../practices/)
- Livello inferiore: [`levels/production-ready.md`](production-ready.md)
