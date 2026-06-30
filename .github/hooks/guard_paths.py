#!/usr/bin/env python3
"""GitHub Copilot — PreToolUse: applica i vincoli strutturali sulle scritture.

Hook autonomo (nessuna dipendenza esterna): blocca scritture che violano
  - S08  data/raw/ e' immutabile (nessuna modifica manuale ai dati originali)
  - S04/S05  .env non viene mai scritto/committato (usare .env.example)
  - S03  nessun notebook (.ipynb) dentro src/

Contratto Copilot: payload JSON su stdin. Gli hook PreToolUse sono fail-closed
(un errore nega l'azione): per bloccare si esce con codice 2 e si scrive la
motivazione su stderr; altrimenti si esce 0.
"""
import json
import os
import sys


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

    norm = abs_path.replace(os.sep, "/")
    rel = os.path.relpath(abs_path, cwd).replace(os.sep, "/")
    basename = os.path.basename(norm)

    # --- S08: data/raw/ immutabile ---------------------------------------
    if "/data/raw/" in norm or rel.startswith("data/raw/"):
        if os.path.exists(abs_path):
            sys.stderr.write(
                "BLOCCATO (S08 - Data Reproducibility): data/raw/ e' in sola "
                "lettura. I dati raw sono immutabili: nessuna modifica manuale.\n"
                "Se serve trasformare i dati, scrivi uno script in src/ che "
                "produca l'output in data/processed/.\n"
            )
            return 2

    # --- S04/S05: mai scrivere .env --------------------------------------
    if basename == ".env" or (
        basename.startswith(".env.") and not basename.endswith(".example")
    ):
        sys.stderr.write(
            "BLOCCATO (S04/S05 - Configuration Management): il file .env non va "
            "scritto ne' committato. Documenta le variabili in .env.example "
            "(senza valori reali) e tieni .env in .gitignore.\n"
        )
        return 2

    # --- S03: nessun notebook in src/ ------------------------------------
    if basename.endswith(".ipynb") and ("/src/" in norm or rel.startswith("src/")):
        sys.stderr.write(
            "BLOCCATO (S03 - Repository Structure): i notebook non vivono in "
            "src/. L'esplorazione sta in notebooks/; src/ contiene solo moduli "
            "Python strutturati e testabili.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
