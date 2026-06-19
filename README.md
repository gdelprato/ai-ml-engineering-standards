# AI/ML Engineering Standards

> **"Come facciamo questo progetto in modo che sia riproducibile, consegnabile, manutenibile e valutabile — indipendentemente da chi lo fa?"**

Questo repository definisce il modello di lavoro ufficiale della practice per lo sviluppo di soluzioni AI, ML e sistemi agentici. Non è documentazione opzionale. È il riferimento normativo per ogni progetto.

---

## Struttura del modello

Il modello è organizzato in tre livelli gerarchici:

| Livello | Cosa definisce | File |
|---|---|---|
| **Principi** | Il perché — valori fondamentali non negoziabili | `principles/` |
| **Standard** | Il cosa — criteri verificabili per ogni progetto | `standards/` |
| **Pratiche** | Il come — implementazioni concrete con livelli di maturità | `practices/` |

I principi sono stabili nel tempo. Gli standard sono indipendenti dai tool. Le pratiche evolvono con il contesto e la tecnologia.

---

## Indice

### Principi
- [Principi fondamentali](principles/principles.md)

### Standard
- [Architettura e decisioni](standards/architecture.md)
- [Qualità del codice](standards/code-quality.md)
- [Riproducibilità e validazione](standards/reproducibility.md)
- [Gestione del lavoro](standards/work-management.md)
- [Consegna](standards/delivery.md)
- [Sistemi agentici](standards/agentic-systems.md)

### Pratiche
- [Architettura e decisioni](practices/architecture.md)
- [Qualità del codice](practices/code-quality.md)
- [Riproducibilità e validazione](practices/reproducibility.md)
- [Gestione del lavoro](practices/work-management.md)
- [Consegna](practices/delivery.md)
- [Sistemi agentici](practices/agentic-systems.md)

### Template
- [ADR — Architecture Decision Record](templates/adr-template.md)
- [Architecture Document](templates/architecture-template.md)
- [Runbook](templates/runbook-template.md)
- [Handover Checklist](templates/handover-checklist.md)
- [Agent Perimeter Definition](templates/agent-perimeter.md)

---

## Dominio di applicazione

Questi standard si applicano a tutti i progetti della practice, senza eccezioni:

- **ML classico** — modelli predittivi, classificazione, regressione, forecasting
- **LLM e GenAI** — RAG, fine-tuning, prompt engineering, chatbot
- **Sistemi agentici** — agent, multi-agent, tool use, workflow autonomi

---

## Livelli di maturità

Ogni pratica è definita su tre livelli:

| Livello | Descrizione |
|---|---|
| **Minimo** | Non negoziabile. Obbligatorio su ogni progetto prima della consegna. |
| **Consigliato** | Target standard per progetti in produzione. |
| **Avanzato** | Obiettivo di maturità della practice nel medio termine. |

Il livello minimo non è un punto di partenza — è il requisito di accettazione. Un progetto che non soddisfa tutti i minimi non è pronto per la consegna.

---

## Governance

| Attributo | Valore |
|---|---|
| **Owner** | Practice Lead |
| **Review cadence** | Trimestrale |
| **Versioning** | Semantic versioning — vedere [CHANGELOG](CHANGELOG.md) |
| **Contributi** | Pull request con ADR allegato per ogni modifica strutturale |

---

## Versione corrente

`v1.0.0` — vedere [CHANGELOG](CHANGELOG.md) per la storia delle modifiche.
