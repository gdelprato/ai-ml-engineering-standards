# GEMINI.md

Questo repository definisce il **modello operativo della practice AI/ML
Engineering**: principi (P01–P10), standard verificabili (S01–S23) e pratiche con
livelli di maturità (Foundation, Production-Ready, Enterprise-Grade).

> Contesto di progetto per **Gemini CLI**. Il tooling che lo accompagna
> (`.gemini/`) è autonomo e specifico per Gemini: non dipende da altri tool.

## Natura del repository

È un repository **normativo**, non un'applicazione. Contiene documentazione
strutturata in `principles/`, `standards/`, `practices/`, `levels/`, `templates/`.
Le modifiche strutturali richiedono un ADR allegato (vedere [README](README.md) §
Governance).

## Contesto operativo — sviluppa sempre in conformità

Promemoria dei vincoli più rilevanti durante lo sviluppo:
- **P01/S01**: architettura documentata prima del codice di produzione.
- **P02/S02**: ogni decisione tecnica rilevante → un ADR (`docs/decisions/`).
- **P03/S03**: notebook solo in `notebooks/`, mai in `src/`; `src/` = moduli testabili.
- **P04/S05**: nessun secret o config hardcoded; usare `.env` + `.env.example`.
- **P05/S07-S08**: ambiente ricostruibile in <30 min; `data/raw/` immutabile.
- **P06/S10**: nessuna consegna senza validation gate eseguito e documentato.
- **P08/S12**: commit in formato `<type>(<scope>): desc` con `Refs: #issue`.
- **S18-S23** (agentici): tool classificati READ/WRITE-REV/WRITE-IRR, HITL gate,
  behavioral eval (4 scenari), observability per-step, perimetro, cost control.

## Tooling per Gemini CLI

La cartella `.gemini/` contiene le utility (autonome) che applicano questi
standard. Sono pensate per essere **copiate nella radice di un progetto** della
practice insieme a questo `GEMINI.md`. Vedere [.gemini/README.md](.gemini/README.md).

- **Hook** (vincoli automatici, in `.gemini/settings.json`): protezione di
  `data/raw/` e `.env`, blocco dei notebook in `src/`, scansione di secret
  hardcoded, validazione della commit convention. Sono applicati su
  `BeforeTool`/`AfterTool`: rispettali invece di aggirarli.
- **Slash command**: `/scaffold-project`, `/architecture-doc`, `/adr`,
  `/runbook`, `/agent-perimeter`, `/tool-registry`, `/handover`, `/commit`,
  `/compliance-check`.
- **Personas di review** (comandi namespaced `review:`):
  `/review:compliance-auditor`, `/review:agentic-safety-reviewer`,
  `/review:reproducibility-validator`, `/review:architecture-reviewer`,
  `/review:eval-designer`.

## Convenzioni di lavoro su questo repo

- **Commit** in formato `<type>(<scope>): descrizione` (S12); tipi ammessi:
  `feat fix refactor test docs chore eval`. L'hook lo verifica.
- **Documentazione in italiano**, coerente con il resto del repository.
- Quando si modifica o aggiunge contenuto normativo, mantenere i riferimenti
  incrociati tra principi, standard e pratiche allineati.
