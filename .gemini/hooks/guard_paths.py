#!/usr/bin/env python3
"""Gemini CLI — BeforeTool: applica i vincoli strutturali sulle scritture.

Adattatore sottile sul core condiviso `tools/standards_core`. Blocca scritture
che violano S08 (data/raw immutabile), S04/S05 (.env), S03 (notebook in src/).

Contratto Gemini: riceve il payload JSON su stdin (campi tool_name, tool_input,
cwd). Per bloccare esce con codice 2 e scrive la motivazione su stderr; negli
altri casi esce 0.
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

    reason = rules.check_write_violation(abs_path, cwd, os.path.exists(abs_path))
    if reason:
        sys.stderr.write(reason + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
