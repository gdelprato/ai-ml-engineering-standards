# GitHub Copilot Utilities — AI/ML Engineering Standards

Utility **ad hoc per GitHub Copilot** che applicano e fanno rispettare gli
standard della practice (principi P01–P10, standard S01–S23) durante lo sviluppo.

Sono **autonome**: tutto ciò che serve è in `.github/` (parti elencate sotto).
Nessuna dipendenza da altri tool o da altre cartelle.

## Cosa contiene

```
.github/
├── copilot-instructions.md   # contesto di progetto (sempre applicato)
├── prompts/                  # prompt files (.prompt.md) → /<nome> in chat
├── chatmodes/                # chat modes (.chatmode.md) → personas di review
└── hooks/                    # vincoli automatici (PreToolUse / PostToolUse)
```

## Contesto

`copilot-instructions.md` è caricato automaticamente da Copilot in ogni richiesta
nel repository: contiene i principi/standard e l'elenco delle utility.

## Prompt files — scaffolding conforme

In `prompts/*.prompt.md`, invocabili con `/<nome>` (VS Code / Visual Studio /
JetBrains): `/scaffold-project`, `/architecture-doc`, `/adr`, `/runbook`,
`/agent-perimeter`, `/tool-registry`, `/handover`, `/commit`,
`/compliance-check`.

## Chat modes — personas di review

In `chatmodes/*.chatmode.md`: `compliance-auditor`, `agentic-safety-reviewer`,
`reproducibility-validator`, `architecture-reviewer`, `eval-designer`.

## Hooks — vincoli automatici

Configurati in `hooks/standards.json` (Copilot agent hooks, **public preview**).
In Python 3, nessuna dipendenza esterna, ogni hook è self-contained.

| Hook | Evento | Cosa fa | Standard |
|---|---|---|---|
| `guard_paths.py` | `PreToolUse` | Blocca scritture in `data/raw/`, `.env`, notebook in `src/` | S03, S04, S05, S08 |
| `check_commit.py` | `PreToolUse` | Valida la commit convention sui `git commit` | S12 |
| `scan_secrets.py` | `PostToolUse` | Scansiona secret hardcoded nei file appena scritti | S05 |

Gli hook `PreToolUse` sono **fail-closed**: in caso di blocco escono con codice 2
e scrivono la motivazione su stderr (un errore dell'hook nega l'azione). I tre
script si auto-filtrano in base al tipo di azione, quindi sono registrati senza
matcher.

> Nota: gli agent hooks di Copilot sono in public preview e i nomi degli eventi
> possono differire leggermente tra le superfici (VS Code Chat vs coding agent).
> Verifica `hooks/standards.json` per la tua versione se gli hook non scattano.

## Come usarle in un nuovo progetto

1. Copia in `.github/` del progetto: `copilot-instructions.md`, `prompts/`,
   `chatmodes/`, `hooks/`.
2. Copilot caricherà automaticamente le istruzioni; i prompt files e le chat
   modes saranno disponibili in chat, gli hook attivi sulle tool call.

## Requisiti

- `python3` nel PATH (hook; nessuna libreria esterna).
- Agent hooks di Copilot abilitati nel tuo client/repository.
