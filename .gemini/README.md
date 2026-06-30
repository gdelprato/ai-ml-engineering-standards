# Gemini CLI Utilities — AI/ML Engineering Standards

Utility per **Gemini CLI** che applicano e fanno rispettare gli standard della
practice (principi P01–P10, standard S01–S23) durante lo sviluppo. Sono il
gemello delle utility in [`.claude/`](../.claude/README.md), adattate al
contratto di Gemini CLI.

La conformità non dipende dalla disciplina del singolo: è guidata dal contesto
(`GEMINI.md`) e in parte **applicata automaticamente** dagli hook.

## Cosa contiene

```
.gemini/
├── settings.json        # registra gli hook (BeforeTool / AfterTool)
├── hooks/               # adattatori sottili sul core condiviso
└── commands/            # slash command (.toml) + review/ (personas)
GEMINI.md                # contesto di progetto (sempre caricato)
tools/standards_core/    # logica delle regole (condivisa, NON duplicata)
```

> **Dipendenza importante:** gli hook importano `tools/standards_core`. Quando
> copi questo tooling in un progetto, copia **sia `.gemini/` sia `tools/`** (e
> `GEMINI.md`). Gli hook risolvono il core relativamente alla propria posizione,
> quindi funzionano da qualunque `cwd`.

## Hooks — vincoli automatici

Configurati in `settings.json`, in Python 3 (nessuna dipendenza esterna).

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

Gemini CLI non ha subagent nativi: le personas dei subagent di Claude sono
esposte come comandi namespaced in `commands/review/`.

| Comando | Quando usarlo | Standard |
|---|---|---|
| `/review:compliance-auditor` | Audit completo prima della consegna | S01–S23 |
| `/review:agentic-safety-reviewer` | Sistemi con agent/tool prima della produzione | S18–S23 |
| `/review:reproducibility-validator` | "Si fa girare da zero in <30 min?" | S04, S05, S07, S08 |
| `/review:architecture-reviewer` | Prima di scrivere codice; review architettura/ADR | S01, S02 |
| `/review:eval-designer` | Progettare/rivedere eval e validation gate | S10, S20 |

## Rigenerazione

Comandi e personas sono **generati** dall'unica fonte `.claude/` per non
divergere. Dopo aver modificato un file in `.claude/commands/` o
`.claude/agents/`, rigenera con:

```
python3 tools/gen_agent_tooling.py
```

I file generati portano un banner `GENERATO da ...`: non modificarli a mano.

## Requisiti

- `python3` nel PATH (hook; nessuna libreria esterna).
- Hook di Gemini CLI abilitati (default dalla v0.26.0).
