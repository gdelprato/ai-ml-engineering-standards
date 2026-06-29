# CLAUDE.md

Questo repository definisce il **modello operativo della practice AI/ML
Engineering**: principi (P01–P10), standard verificabili (S01–S23) e pratiche con
livelli di maturità (Foundation, Production-Ready, Enterprise-Grade).

## Natura del repository

È un repository **normativo**, non un'applicazione. Contiene documentazione
strutturata in `principles/`, `standards/`, `practices/`, `levels/`, `templates/`.
Le modifiche strutturali richiedono un ADR allegato (vedere [README](README.md) §
Governance).

## Tooling per Claude Code

La cartella `.claude/` contiene utility che applicano questi standard quando si
sviluppa un progetto reale. Sono progettate per essere **copiate nella radice di
un progetto** della practice. Vedere [.claude/README.md](.claude/README.md).

- **Hook** (vincoli automatici): protezione di `data/raw/` e `.env`, blocco dei
  notebook in `src/`, scansione di secret hardcoded, validazione della commit
  convention.
- **Subagent**: `compliance-auditor`, `agentic-safety-reviewer`,
  `reproducibility-validator`, `architecture-reviewer`, `eval-designer`.
- **Slash command**: `/scaffold-project`, `/architecture-doc`, `/adr`, `/runbook`,
  `/agent-perimeter`, `/tool-registry`, `/handover`, `/commit`, `/compliance-check`.

## Convenzioni di lavoro su questo repo

- **Commit** in formato `<type>(<scope>): descrizione` (S12); tipi ammessi:
  `feat fix refactor test docs chore eval`. Il hook `check_commit.py` lo verifica.
- **Documentazione in italiano**, coerente con il resto del repository.
- Quando si modifica o aggiunge contenuto normativo, mantenere i riferimenti
  incrociati tra principi, standard e pratiche allineati.
