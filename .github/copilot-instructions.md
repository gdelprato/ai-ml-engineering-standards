# GitHub Copilot — istruzioni di repository

Questo repository definisce il **modello operativo della practice AI/ML
Engineering**: principi (P01–P10), standard verificabili (S01–S23) e pratiche con
livelli di maturità (Foundation, Production-Ready, Enterprise-Grade).

> File gemello di [CLAUDE.md](../CLAUDE.md) e [GEMINI.md](../GEMINI.md): stesso
> contenuto normativo, adattato a GitHub Copilot. La fonte unica del tooling
> resta `.claude/`; le utility di Copilot sono generate da
> `tools/gen_agent_tooling.py`.

## Natura del repository

È un repository **normativo**, non un'applicazione. Contiene documentazione
strutturata in `principles/`, `standards/`, `practices/`, `levels/`, `templates/`.
Le modifiche strutturali richiedono un ADR allegato (vedere README § Governance).

## Contesto operativo — sviluppa sempre in conformità

- **P01/S01**: architettura documentata prima del codice di produzione.
- **P02/S02**: ogni decisione tecnica rilevante → un ADR (`docs/decisions/`).
- **P03/S03**: notebook solo in `notebooks/`, mai in `src/`; `src/` = moduli testabili.
- **P04/S05**: nessun secret o config hardcoded; usare `.env` + `.env.example`.
- **P05/S07-S08**: ambiente ricostruibile in <30 min; `data/raw/` immutabile.
- **P06/S10**: nessuna consegna senza validation gate eseguito e documentato.
- **P08/S12**: commit in formato `<type>(<scope>): desc` con `Refs: #issue`;
  tipi ammessi: `feat fix refactor test docs chore eval`.
- **S18-S23** (agentici): tool classificati READ/WRITE-REV/WRITE-IRR, HITL gate,
  behavioral eval (4 scenari), observability per-step, perimetro, cost control.

## Tooling per Copilot

- **Prompt files** (`.github/prompts/*.prompt.md`) — invocabili con `/<nome>` in
  chat: `/scaffold-project`, `/architecture-doc`, `/adr`, `/runbook`,
  `/agent-perimeter`, `/tool-registry`, `/handover`, `/commit`,
  `/compliance-check`.
- **Chat modes** (`.github/chatmodes/*.chatmode.md`) — personas di review:
  `compliance-auditor`, `agentic-safety-reviewer`, `reproducibility-validator`,
  `architecture-reviewer`, `eval-designer`.
- **Hook** (`.github/hooks/`) — vincoli automatici applicati su
  `PreToolUse`/`PostToolUse` (public preview): protezione `data/raw/` e `.env`,
  blocco notebook in `src/`, scansione secret, validazione commit. Dipendono da
  `tools/standards_core/`.

Documentazione in italiano, coerente con il resto del repository. Mantieni
allineati i riferimenti incrociati tra principi, standard e pratiche.
