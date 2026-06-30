# Gemini CLI Utilities — AI/ML Engineering Standards

Utility **ad hoc per Gemini CLI** che applicano e fanno rispettare gli standard
della practice (principi P01–P10, standard S01–S23) durante lo sviluppo.

Sono **autonome**: tutto ciò che serve è in questa cartella `.gemini/` (più il
contesto `GEMINI.md` alla radice). Nessuna dipendenza da altri tool o da altre
cartelle. La conformità non dipende dalla disciplina del singolo: è guidata dal
contesto e in parte **applicata automaticamente** dagli hook.

## Cosa contiene

```
.gemini/
├── settings.json        # registra gli hook (BeforeTool / AfterTool)
├── hooks/               # vincoli automatici, script Python autonomi
└── commands/            # slash command (.toml) + review/ (personas)
GEMINI.md                # contesto di progetto (sempre caricato)
```

## Hooks — vincoli automatici

Configurati in `settings.json`, in Python 3 (nessuna dipendenza esterna, ogni
hook è self-contained).

| Hook | Evento | Cosa fa | Standard |
|---|---|---|---|
| `guard_paths.py` | `BeforeTool` (write) | Blocca scritture in `data/raw/`, `.env`, notebook in `src/` | S03, S04, S05, S08 |
| `check_commit.py` | `BeforeTool` (`run_shell_command`) | Valida la commit convention sui `git commit` | S12 |
| `scan_secrets.py` | `AfterTool` (write) | Scansiona secret hardcoded nei file appena scritti | S05 |

I blocchi escono con codice 2 e scrivono la motivazione su stderr (Gemini la
mostra all'agente). Gli avvisi non bloccanti escono 0. La scansione ignora i
placeholder evidenti (`your_`, `os.environ`, `${...}`, `.env.example`, ...).

## Slash command

Definiti in `commands/*.toml`. Invocabili in chat con `/<nome>`.

| Comando | Cosa genera | Standard |
|---|---|---|
| `/scaffold-project` | Struttura repo standard | S03 |
| `/architecture-doc` | `docs/architecture.md` | S01 |
| `/adr` | Nuovo ADR numerato | S02 |
| `/runbook` | `docs/runbook.md` | S15 |
| `/agent-perimeter` | `docs/agent-perimeter.md` | S22 |
| `/tool-registry` | `docs/tools-registry.md` | S18 |
| `/handover` | `docs/handover-checklist.md` | S17 |
| `/commit` | Commit conforme | S12 |
| `/compliance-check` | Audit rapido + livello | S01–S23 |

## Personas di review

Gemini CLI non ha subagent nativi: le personas di review sono esposte come
comandi namespaced in `commands/review/`.

| Comando | Quando usarlo | Standard |
|---|---|---|
| `/review:compliance-auditor` | Audit completo prima della consegna | S01–S23 |
| `/review:agentic-safety-reviewer` | Sistemi con agent/tool prima della produzione | S18–S23 |
| `/review:reproducibility-validator` | "Si fa girare da zero in <30 min?" | S04, S05, S07, S08 |
| `/review:architecture-reviewer` | Prima di scrivere codice; review architettura/ADR | S01, S02 |
| `/review:eval-designer` | Progettare/rivedere eval e validation gate | S10, S20 |

## Come usarle in un nuovo progetto

1. Copia `.gemini/` e `GEMINI.md` nella radice del progetto.
2. Apri il progetto con Gemini CLI: `GEMINI.md` carica il contesto e gli hook in
   `settings.json` diventano attivi.
3. Parti da `/architecture-doc` (P01: architettura prima del codice), poi
   `/scaffold-project`, e procedi. Prima della consegna lancia
   `/compliance-check` o `/review:compliance-auditor`.

## Requisiti

- `python3` nel PATH (hook; nessuna libreria esterna).
- Hook di Gemini CLI abilitati (default dalla v0.26.0).
