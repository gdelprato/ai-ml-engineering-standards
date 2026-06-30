#!/usr/bin/env python3
"""Gemini CLI — AfterTool: scansione di secret hardcoded dopo una scrittura (S05).

Adattatore sottile sul core condiviso `tools/standards_core`. Dopo che un file e'
stato scritto, lo rilegge da disco e cerca credenziali/valori sensibili
hardcoded; se ne trova esce con codice 2 e segnala il problema su stderr.
"""
import json
import os
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
    cwd = payload.get("cwd") or os.getcwd()
    abs_path = rules.resolve_path(tool_input, cwd)
    if not abs_path:
        return 0

    report = rules.scan_secrets(abs_path, cwd)
    if report:
        sys.stderr.write(report + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
