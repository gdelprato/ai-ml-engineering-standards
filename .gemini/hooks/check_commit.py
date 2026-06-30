#!/usr/bin/env python3
"""Gemini CLI — BeforeTool (run_shell_command): valida la commit convention (S12).

Hook autonomo (nessuna dipendenza esterna): intercetta i `git commit` e verifica
che il subject segua `<type>(<scope>): descrizione` con type ammesso. Il
riferimento all'issue (Refs: #N) e' raccomandato ma non bloccante. Se il
messaggio non e' estraibile in modo affidabile, lascia procedere.

Contratto Gemini CLI: payload JSON su stdin (tool_input.command). Per bloccare
esce 2 con la motivazione su stderr.
"""
import json
import re
import shlex
import sys

VALID_TYPES = {"feat", "fix", "refactor", "test", "docs", "chore", "eval"}
GENERIC = {"wip", "update", "fix", "misc", "stuff", "changes", "tmp", "test", "."}
SUBJECT_RE = re.compile(
    r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s+(?P<desc>.+)$"
)


def _extract_commit_messages(command: str):
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None

    joined = " ".join(tokens)
    if "git" not in tokens or "commit" not in tokens:
        return None
    if not re.search(r"\bgit\b.*\bcommit\b", joined):
        return None
    if "$(" in command or "`" in command or "<<" in command:
        return None

    messages = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in ("-m", "--message") and i + 1 < len(tokens):
            messages.append(tokens[i + 1])
            i += 2
            continue
        if tok.startswith("-m") and len(tok) > 2:
            messages.append(tok[2:])
        elif tok.startswith("--message="):
            messages.append(tok.split("=", 1)[1])
        elif tok in ("-F", "--file", "--amend", "--no-edit"):
            return None
        i += 1

    return messages or None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    command = tool_input.get("command") or tool_input.get("cmd") or ""
    if not command:
        return 0

    messages = _extract_commit_messages(command)
    if not messages:
        return 0

    subject = messages[0].strip().splitlines()[0].strip()

    if subject.lower() in GENERIC:
        sys.stderr.write(
            f"COMMIT BLOCCATO (S12 - Commit Convention): messaggio generico "
            f"'{subject}'. Usa il formato '<type>(<scope>): descrizione' con un "
            "messaggio che spieghi il perche' della modifica.\n"
        )
        return 2

    m = SUBJECT_RE.match(subject)
    if not m:
        sys.stderr.write(
            "COMMIT BLOCCATO (S12 - Commit Convention): il subject non rispetta "
            "il formato.\n"
            "  Atteso:  <type>(<scope>): descrizione breve\n"
            "  Esempio: feat(agent): add tool call retry with backoff\n"
            f"  Tipi ammessi: {', '.join(sorted(VALID_TYPES))}\n"
        )
        return 2

    ctype = m.group("type")
    if ctype not in VALID_TYPES:
        sys.stderr.write(
            f"COMMIT BLOCCATO (S12 - Commit Convention): type '{ctype}' non "
            f"ammesso. Usa uno tra: {', '.join(sorted(VALID_TYPES))}.\n"
        )
        return 2

    full = "\n".join(messages)
    if not re.search(r"(?i)(refs|closes|fixes)\s*:?\s*#\d+", full):
        sys.stderr.write(
            "[avviso S12] Commit senza riferimento all'issue (es. 'Refs: #42'). "
            "Ogni commit dovrebbe essere collegato a un task (P08). Procedo "
            "comunque.\n"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
