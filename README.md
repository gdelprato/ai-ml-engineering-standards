# AI/ML Engineering Standards

Questo repository definisce il modello operativo ufficiale della practice per lo sviluppo di soluzioni AI, ML e sistemi agentici. Non è documentazione opzionale: è il riferimento normativo per ogni progetto.

---

## Obiettivo

Garantire che ogni progetto della practice — indipendentemente da chi lo sviluppa, dalla tecnologia usata o dalla durata — sia **riproducibile**, **consegnabile**, **manutenibile** e **valutabile**.

Il problema che questo repository risolve è strutturale: senza standard condivisi, la qualità dipende dalle persone, non dal processo. I progetti diventano difficili da trasferire, da manutenere e da consegnare al cliente in modo autonomo.

La risposta è un sistema in tre livelli — principi, standard, pratiche — che separa il *perché* (valori stabili), il *cosa* (criteri verificabili), e il *come* (implementazioni concrete).

---

## Struttura del modello

```
ai-ml-engineering-standards/
├── principles/          # Il perché — valori fondamentali non negoziabili
├── standards/           # Il cosa — criteri verificabili per ogni progetto
├── practices/           # Il come — implementazioni concrete con livelli di maturità
├── levels/              # Checklist di conformità per livello di maturità
└── templates/           # Template pronti all'uso (ADR, architettura, runbook, ecc.)
```

| Livello | Cosa definisce | Stabilità |
|---|---|---|
| **Principi** | Valori fondamentali da cui derivano tutti gli standard | Stabile nel tempo |
| **Standard** | Criteri verificabili, indipendenti dai tool | Evolve lentamente |
| **Pratiche** | Implementazioni concrete con livelli di maturità | Evolve con la tecnologia |

---

## Principi fondamentali

Il modello si basa su 10 principi (P01–P10), ognuno con un criterio verificabile:

| Principio | Sintesi |
|---|---|
| P01 — Architettura prima del codice | Ogni soluzione ha un documento di architettura prima che venga scritto codice di produzione |
| P02 — Decisioni tracciate | Ogni scelta tecnica rilevante è documentata con contesto, alternative e motivazione |
| P03 — Esplorazione vs produzione | I notebook non vanno mai in produzione; il codice di produzione è strutturato e testabile |
| P04 — Configurazione separata | Nessun valore di ambiente o credenziale è hardcoded nel codice |
| P05 — Riproducibilità | Qualsiasi membro del team può ricreare ambiente e risultati in meno di 30 minuti |
| P06 — Validazione esplicita | Nessun sistema va in produzione senza criteri di accettazione misurabili |
| P07 — Task espliciti | Ogni attività esiste come task tracciato prima di essere iniziata |
| P08 — Codice collegato a task | Da ogni commit si risale al task che lo ha generato |
| P09 — Workflow condiviso | Il processo da requisito a produzione è documentato e seguito da tutti |
| P10 — Consegna come sistema | Una consegna include documentazione operativa, criteri di monitoraggio e istruzioni di manutenzione |

---

## Standard e pratiche

Gli standard coprono sei aree, con 23 criteri totali (S01–S23):

| Area | Standard | Pratiche |
|---|---|---|
| Architettura e decisioni | [standards/architecture.md](standards/architecture.md) | [practices/architecture.md](practices/architecture.md) |
| Qualità del codice | [standards/code-quality.md](standards/code-quality.md) | [practices/code-quality.md](practices/code-quality.md) |
| Riproducibilità e validazione | [standards/reproducibility.md](standards/reproducibility.md) | [practices/reproducibility.md](practices/reproducibility.md) |
| Gestione del lavoro | [standards/work-management.md](standards/work-management.md) | [practices/work-management.md](practices/work-management.md) |
| Consegna | [standards/delivery.md](standards/delivery.md) | [practices/delivery.md](practices/delivery.md) |
| Sistemi agentici | [standards/agentic-systems.md](standards/agentic-systems.md) | [practices/agentic-systems.md](practices/agentic-systems.md) |

Gli standard per i sistemi agentici (S18–S23) trattano i requisiti specifici di autonomia, irreversibilità e non determinismo composto che differenziano gli agent da tutti gli altri sistemi.

---

## Livelli di maturità

Ogni pratica è definita su tre livelli progressivi:

| Livello | Descrizione | File |
|---|---|---|
| **Foundation** | Non negoziabile. Obbligatorio su ogni progetto prima della consegna. | [levels/foundation.md](levels/foundation.md) |
| **Production-Ready** | Target standard per progetti in produzione. | [levels/production-ready.md](levels/production-ready.md) |
| **Enterprise-Grade** | Obiettivo di maturità della practice nel medio termine. | [levels/enterprise-grade.md](levels/enterprise-grade.md) |

Il livello Foundation non è un punto di partenza — è il requisito di accettazione. Un progetto che non soddisfa tutti i criteri Foundation non è pronto per la consegna.

---

## Template

| Template | Scopo |
|---|---|
| [ADR](templates/adr-template.md) | Documentare una decisione architetturale |
| [Architecture Document](templates/architecture-template.md) | Descrivere la struttura e le scelte di un sistema |
| [Runbook](templates/runbook-template.md) | Istruzioni operative per deploy, monitoring e incident |
| [Handover Checklist](templates/handover-checklist.md) | Verifica che un progetto sia consegnabile |
| [Agent Perimeter](templates/agent-perimeter.md) | Definire il perimetro di autonomia di un sistema agentico |

---

## Dominio di applicazione

Questi standard si applicano a tutti i progetti della practice, senza eccezioni:

- **ML classico** — modelli predittivi, classificazione, regressione, forecasting
- **LLM e GenAI** — RAG, fine-tuning, prompt engineering, chatbot
- **Sistemi agentici** — agent, multi-agent, tool use, workflow autonomi

---

## Governance

| Attributo | Valore |
|---|---|
| **Owner** | Practice Lead |
| **Review cadence** | Trimestrale |
| **Versioning** | Semantic versioning — vedere [CHANGELOG](CHANGELOG.md) |
| **Contributi** | Pull request con ADR allegato per ogni modifica strutturale |

**Versione corrente:** `v1.0.0` — vedere [CHANGELOG](CHANGELOG.md) per la storia delle modifiche.

---

## Indice di navigazione

### Principi
- [Principi fondamentali (P01–P10)](principles/principles.md)

### Standard
- [Architettura e decisioni (S01–S02)](standards/architecture.md)
- [Qualità del codice (S03–S06)](standards/code-quality.md)
- [Riproducibilità e validazione (S07–S10)](standards/reproducibility.md)
- [Gestione del lavoro (S11–S14)](standards/work-management.md)
- [Consegna (S15–S17)](standards/delivery.md)
- [Sistemi agentici (S18–S23)](standards/agentic-systems.md)

### Pratiche
- [Architettura e decisioni](practices/architecture.md)
- [Qualità del codice](practices/code-quality.md)
- [Riproducibilità e validazione](practices/reproducibility.md)
- [Gestione del lavoro](practices/work-management.md)
- [Consegna](practices/delivery.md)
- [Sistemi agentici](practices/agentic-systems.md)

### Livelli di maturità
- [Foundation](levels/foundation.md)
- [Production-Ready](levels/production-ready.md)
- [Enterprise-Grade](levels/enterprise-grade.md)

### Template
- [ADR — Architecture Decision Record](templates/adr-template.md)
- [Architecture Document](templates/architecture-template.md)
- [Runbook](templates/runbook-template.md)
- [Handover Checklist](templates/handover-checklist.md)
- [Agent Perimeter Definition](templates/agent-perimeter.md)
