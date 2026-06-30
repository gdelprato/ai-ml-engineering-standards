#!/usr/bin/env python3
"""Gemini CLI — BeforeTool (run_shell_command): valida la commit convention (S12).

Adattatore sottile sul core condiviso `tools/standards_core`. Intercetta i
`git commit` e verifica che il subject segua `<type>(<scope>): descrizione`.
Il riferimento all'issue e' raccomandato ma non bloccante.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from standards_core import rules  # noqa: E402


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    command = rules.resolve_command(tool_input)
    if not command:
        return 0

    status, message = rules.check_commit(command)
    if status == "block":
        sys.stderr.write(message + "\n")
        return 2
    if status == "warn":
        sys.stderr.write(message + "\n")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
