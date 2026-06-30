#!/usr/bin/env python3
"""GitHub Copilot — PostToolUse: scansione di secret hardcoded dopo scrittura (S05).

Hook autonomo (nessuna dipendenza esterna): dopo che un file e' stato scritto, lo
rilegge da disco e cerca credenziali/valori sensibili hardcoded. Se ne trova,
esce con codice 2 e segnala il problema su stderr; i placeholder evidenti
(your_, ${...}, os.environ, ...) e i file di esempio sono ignorati.
"""
import json
import os
import re
import sys

PATTERNS = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("OpenAI/Anthropic-style key", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[0-9A-Za-z]{30,}")),
    (
        "Private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    ),
    (
        "Credenziale assegnata inline",
        re.compile(
            r"(?i)(?:api[_-]?key|secret|secret[_-]?key|access[_-]?token|auth[_-]?token|"
            r"password|passwd|pwd|client[_-]?secret)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
        ),
    ),
]

PLACEHOLDER_HINTS = (
    "your_", "your-", "xxx", "<", ">", "${", "os.environ", "getenv",
    "example", "changeme", "change_me", "placeholder", "dummy", "fake",
    "redacted", "todo", "...", "******",
)

SKIP_BASENAMES = {".env.example", ".env.sample", ".env.template"}
SKIP_SUFFIXES = (".md", ".rst", ".txt.example")


def _is_placeholder(line: str) -> bool:
    low = line.lower()
    return any(hint in low for hint in PLACEHOLDER_HINTS)


def _redact(match: str) -> str:
    if len(match) <= 12:
        return match[:2] + "***"
    return match[:6] + "…" + match[-2:]


def _resolve_path(tool_input: dict, cwd: str) -> str:
    file_path = (
        tool_input.get("file_path")
        or tool_input.get("path")
        or tool_input.get("filePath")
        or tool_input.get("file")
        or ""
    )
    if not file_path:
        return ""
    return file_path if os.path.isabs(file_path) else os.path.join(cwd, file_path)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    cwd = payload.get("cwd") or os.getcwd()
    abs_path = _resolve_path(tool_input, cwd)
    if not abs_path:
        return 0

    basename = os.path.basename(abs_path)
    if basename in SKIP_BASENAMES or basename.endswith(SKIP_SUFFIXES):
        return 0
    if not os.path.isfile(abs_path):
        return 0

    try:
        with open(abs_path, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except OSError:
        return 0

    findings = []
    for i, line in enumerate(lines, 1):
        if _is_placeholder(line):
            continue
        for label, pattern in PATTERNS:
            m = pattern.search(line)
            if m:
                findings.append((i, label, _redact(m.group(0))))
                break

    if findings:
        rel = os.path.relpath(abs_path, cwd)
        sys.stderr.write(
            f"POSSIBILE SECRET HARDCODED in {rel} (S05 - Configuration "
            "Management). Nessun valore di configurazione o credenziale deve "
            "stare nel codice.\n"
        )
        for line_no, label, sample in findings:
            sys.stderr.write(f"  - riga {line_no}: {label} ({sample})\n")
        sys.stderr.write(
            "Sposta il valore in una variabile d'ambiente e documentalo in "
            ".env.example. Se e' un falso positivo, ignora questo avviso.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
