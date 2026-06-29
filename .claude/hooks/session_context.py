#!/usr/bin/env python3
"""SessionStart — inietta nel contesto un promemoria sintetico degli standard.

Lo stdout del hook viene aggiunto al contesto della sessione. Lo scopo e' che
Claude sviluppi sempre tenendo presenti i principi e gli standard della practice,
e sappia quali utility (slash command e subagent) ha a disposizione.

Esce sempre 0. Resta volutamente conciso per non consumare contesto inutilmente.
"""
import sys

CONTEXT = """\
# AI/ML Engineering Standards -- contesto operativo

Stai lavorando in un progetto governato dagli standard della practice
(principi P01-P10, standard S01-S23). Sviluppa sempre in conformita'.

Promemoria dei vincoli piu' rilevanti durante lo sviluppo:
- P01/S01: architettura documentata prima del codice di produzione.
- P02/S02: ogni decisione tecnica rilevante -> un ADR (docs/decisions/).
- P03/S03: notebook solo in notebooks/, mai in src/; src/ = moduli testabili.
- P04/S05: nessun secret o config hardcoded; usare .env + .env.example.
- P05/S07-S08: ambiente ricostruibile in <30 min; data/raw/ immutabile.
- P06/S10: nessuna consegna senza validation gate eseguito e documentato.
- P08/S12: commit in formato '<type>(<scope>): desc' con 'Refs: #issue'.
- S18-S23 (agentici): tool classificati READ/WRITE-REV/WRITE-IRR, HITL gate,
  behavioral eval (4 scenari), observability per-step, perimetro, cost control.

Utility disponibili in questo progetto:
- Slash command: /scaffold-project /adr /architecture-doc /runbook
  /agent-perimeter /tool-registry /handover /commit /compliance-check
- Subagent (Task tool): compliance-auditor, agentic-safety-reviewer,
  reproducibility-validator, architecture-reviewer, eval-designer

Hook attivi: protezione data/raw e .env, blocco notebook in src/, scansione
secret post-scrittura, validazione commit convention. Sono vincoli applicati
automaticamente: rispettali invece di aggirarli.
"""


def main() -> int:
    sys.stdout.write(CONTEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
