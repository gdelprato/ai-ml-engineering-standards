#!/usr/bin/env python3
"""Core delle regole degli standard della practice — logica pura, indipendente
dall'agente.

Gli adattatori di hook per ciascun agente (`.claude/hooks/`, `.gemini/hooks/`,
`.github/hooks/`) importano queste funzioni e le mappano sul proprio contratto:
tutti e tre bloccano l'azione con `exit 2` + motivazione su stderr.

Questo modulo NON fa I/O sul contratto di hook: riceve dati gia' estratti e
restituisce esiti strutturati. In questo modo la stessa regola vale identica su
ogni agente e c'e' un'unica fonte di verita' da mantenere.

Tenuto allineato con gli hook self-contained di `.claude/hooks/` (riferimento
storico, lasciati invariati).
"""
import os
import re
import shlex

# =========================================================================
# S03 / S04 / S05 / S08 — vincoli sui path di scrittura (guard_paths)
# =========================================================================

# Chiavi possibili per il path del file nei vari contratti di hook
# (Claude: file_path; Gemini: path; altri agenti: varianti camelCase).
_PATH_KEYS = ("file_path", "path", "filePath", "file")
# Chiavi possibili per il comando shell (commit check).
_COMMAND_KEYS = ("command", "cmd", "commandLine")


def resolve_path(tool_input: dict, cwd: str) -> str:
    """Estrae e normalizza il path assoluto del file dal tool_input, oppure ''."""
    tool_input = tool_input or {}
    file_path = ""
    for key in _PATH_KEYS:
        if tool_input.get(key):
            file_path = tool_input[key]
            break
    if not file_path:
        return ""
    return file_path if os.path.isabs(file_path) else os.path.join(cwd, file_path)


def resolve_command(tool_input: dict) -> str:
    """Estrae la stringa di comando shell dal tool_input, oppure ''."""
    tool_input = tool_input or {}
    for key in _COMMAND_KEYS:
        if tool_input.get(key):
            return tool_input[key]
    return ""


def check_write_violation(abs_path: str, cwd: str, exists: bool):
    """Verifica i vincoli strutturali su una scrittura.

    Restituisce la motivazione del blocco (str) se la scrittura viola uno
    standard, altrimenti None.
    """
    norm = abs_path.replace(os.sep, "/")
    rel = os.path.relpath(abs_path, cwd).replace(os.sep, "/")
    basename = os.path.basename(norm)

    # --- S08: data/raw/ immutabile -------------------------------------
    # Si blocca la modifica di file gia' esistenti. La creazione di nuovi file
    # raw e' permessa (ingestion), ma editare un raw esistente no.
    if "/data/raw/" in norm or rel.startswith("data/raw/"):
        if exists:
            return (
                "BLOCCATO (S08 - Data Reproducibility): data/raw/ e' in sola "
                "lettura. I dati raw sono immutabili: nessuna modifica manuale.\n"
                "Se serve trasformare i dati, scrivi uno script in src/ che "
                "produca l'output in data/processed/."
            )

    # --- S04/S05: mai scrivere .env ------------------------------------
    if basename == ".env" or (
        basename.startswith(".env.") and not basename.endswith(".example")
    ):
        return (
            "BLOCCATO (S04/S05 - Configuration Management): il file .env non va "
            "scritto ne' committato. Documenta le variabili in .env.example "
            "(senza valori reali) e tieni .env in .gitignore."
        )

    # --- S03: nessun notebook in src/ ----------------------------------
    if basename.endswith(".ipynb") and ("/src/" in norm or rel.startswith("src/")):
        return (
            "BLOCCATO (S03 - Repository Structure): i notebook non vivono in "
            "src/. L'esplorazione sta in notebooks/; src/ contiene solo moduli "
            "Python strutturati e testabili."
        )

    return None


# =========================================================================
# S05 — scansione di secret hardcoded (scan_secrets)
# =========================================================================

# (etichetta, pattern). I pattern catturano la forma tipica del secret.
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

# File che possono legittimamente contenere placeholder/esempi.
SKIP_BASENAMES = {".env.example", ".env.sample", ".env.template"}
SKIP_SUFFIXES = (".md", ".rst", ".txt.example")


def _is_placeholder(line: str) -> bool:
    low = line.lower()
    return any(hint in low for hint in PLACEHOLDER_HINTS)


def _redact(match: str) -> str:
    if len(match) <= 12:
        return match[:2] + "***"
    return match[:6] + "…" + match[-2:]


def scan_secrets(abs_path: str, cwd: str):
    """Rilegge il file da disco e cerca secret hardcoded.

    Restituisce un report testuale (str) se trova qualcosa, altrimenti None.
    I file pensati per contenere placeholder (.env.example, doc) sono esclusi.
    """
    basename = os.path.basename(abs_path)
    if basename in SKIP_BASENAMES or basename.endswith(SKIP_SUFFIXES):
        return None
    if not os.path.isfile(abs_path):
        return None

    try:
        with open(abs_path, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except OSError:
        return None

    findings = []
    for i, line in enumerate(lines, 1):
        if _is_placeholder(line):
            continue
        for label, pattern in PATTERNS:
            m = pattern.search(line)
            if m:
                findings.append((i, label, _redact(m.group(0))))
                break

    if not findings:
        return None

    rel = os.path.relpath(abs_path, cwd)
    out = [
        f"POSSIBILE SECRET HARDCODED in {rel} (S05 - Configuration Management). "
        "Nessun valore di configurazione o credenziale deve stare nel codice."
    ]
    for line_no, label, sample in findings:
        out.append(f"  - riga {line_no}: {label} ({sample})")
    out.append(
        "Sposta il valore in una variabile d'ambiente e documentalo in "
        ".env.example. Se e' un falso positivo, ignora questo avviso."
    )
    return "\n".join(out)


# =========================================================================
# S12 — commit convention (check_commit)
# =========================================================================

VALID_TYPES = {"feat", "fix", "refactor", "test", "docs", "chore", "eval"}
GENERIC = {"wip", "update", "fix", "misc", "stuff", "changes", "tmp", "test", "."}
SUBJECT_RE = re.compile(
    r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s+(?P<desc>.+)$"
)


def extract_commit_messages(command: str):
    """Restituisce la lista di stringhe passate con -m/--message, o None se il
    comando non e' un git commit con messaggio estraibile in modo affidabile."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None

    joined = " ".join(tokens)
    if "git" not in tokens or "commit" not in tokens:
        return None
    if not re.search(r"\bgit\b.*\bcommit\b", joined):
        return None

    # Command substitution / heredoc: messaggio non estraibile in modo
    # affidabile. Non bloccare per evitare falsi positivi.
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


def check_commit(command: str):
    """Valida la commit convention S12 su un comando shell.

    Restituisce una tupla (status, message):
      - ("ok", "")        nessun problema o non applicabile
      - ("block", msg)    da bloccare (exit 2)
      - ("warn", msg)     avviso non bloccante (exit 0, ma mostra msg)
    """
    if not command:
        return ("ok", "")

    messages = extract_commit_messages(command)
    if not messages:
        return ("ok", "")

    subject = messages[0].strip().splitlines()[0].strip()

    if subject.lower() in GENERIC:
        return (
            "block",
            f"COMMIT BLOCCATO (S12 - Commit Convention): messaggio generico "
            f"'{subject}'. Usa il formato '<type>(<scope>): descrizione' con un "
            "messaggio che spieghi il perche' della modifica.",
        )

    m = SUBJECT_RE.match(subject)
    if not m:
        return (
            "block",
            "COMMIT BLOCCATO (S12 - Commit Convention): il subject non rispetta "
            "il formato.\n"
            "  Atteso:  <type>(<scope>): descrizione breve\n"
            "  Esempio: feat(agent): add tool call retry with backoff\n"
            f"  Tipi ammessi: {', '.join(sorted(VALID_TYPES))}",
        )

    ctype = m.group("type")
    if ctype not in VALID_TYPES:
        return (
            "block",
            f"COMMIT BLOCCATO (S12 - Commit Convention): type '{ctype}' non "
            f"ammesso. Usa uno tra: {', '.join(sorted(VALID_TYPES))}.",
        )

    full = "\n".join(messages)
    if not re.search(r"(?i)(refs|closes|fixes)\s*:?\s*#\d+", full):
        return (
            "warn",
            "[avviso S12] Commit senza riferimento all'issue (es. 'Refs: #42'). "
            "Ogni commit dovrebbe essere collegato a un task (P08). Procedo "
            "comunque.",
        )

    return ("ok", "")
