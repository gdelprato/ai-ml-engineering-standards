# Changelog

Tutte le modifiche significative a questo repository sono documentate in questo file.

Il formato segue [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Il versioning segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Tooling **autonomo e ad hoc** per applicare gli standard con **Gemini CLI** e
  **GitHub Copilot**, accanto a quello esistente per Claude Code (`.claude/`,
  invariato). Ogni cartella è indipendente: nessuna dipendenza condivisa tra i
  tool.
  - `.gemini/`: hook self-contained (`BeforeTool`/`AfterTool`), `settings.json`,
    slash command `.toml` e personas di review; contesto in `GEMINI.md`.
  - `.github/`: hook self-contained (`PreToolUse`/`PostToolUse`), prompt files,
    chat modes e contesto in `copilot-instructions.md`.

## [1.0.0] — YYYY-MM-DD

### Added

- Principi fondamentali (P01–P10)
- Standard per Architettura e Decisioni (S01–S02)
- Standard per Qualità del Codice (S03–S06)
- Standard per Riproducibilità e Validazione (S07–S10)
- Standard per Gestione del Lavoro (S11–S14)
- Standard per Consegna (S15–S17)
- Standard per Sistemi Agentici (S18–S23)
- Pratiche per tutte le sei aree con livelli Minimo, Consigliato, Avanzato
- Template: ADR, Architecture Document, Runbook, Handover Checklist, Agent Perimeter
