#!/usr/bin/env python3
"""Generatore delle utility per-agente a partire dall'unica fonte `.claude/`.

I corpi (prompt) degli slash command e delle personas di review sono scritti una
volta sola nei file di `.claude/commands/` e `.claude/agents/`. Questo script ne
deriva le varianti nel formato di ciascun agente, così non c'e' duplicazione a
mano e le versioni non divergono nel tempo:

  .claude/commands/<x>.md  ->  .gemini/commands/<x>.toml      (/<x>)
                           ->  .github/prompts/<x>.prompt.md  (/<x>)

  .claude/agents/<x>.md    ->  .gemini/commands/review/<x>.toml   (/review:<x>)
                           ->  .github/chatmodes/<x>.chatmode.md  (chat mode)

Uso:  python3 tools/gen_agent_tooling.py
Nessuna dipendenza esterna.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAUDE_COMMANDS = ROOT / ".claude" / "commands"
CLAUDE_AGENTS = ROOT / ".claude" / "agents"

GEMINI_COMMANDS = ROOT / ".gemini" / "commands"
GEMINI_REVIEW = GEMINI_COMMANDS / "review"
COPILOT_PROMPTS = ROOT / ".github" / "prompts"
COPILOT_CHATMODES = ROOT / ".github" / "chatmodes"

BANNER = "GENERATO da tools/gen_agent_tooling.py — non modificare a mano."


def parse_front_matter(text: str):
    """Estrae il front matter YAML (valori su singola riga) e il corpo."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text.strip()
    fm = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        if ":" in line:
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip()
        i += 1
    body = "\n".join(lines[i + 1:]).strip()
    return fm, body


def toml_escape(s: str) -> str:
    """Escape per stringa TOML basic (un'unica riga)."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def yaml_dq(s: str) -> str:
    """Escape per scalare YAML double-quoted (un'unica riga)."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  scritto {path.relative_to(ROOT)}")


def gen_gemini_command(name: str, description: str, body: str, review: bool):
    prompt = body.replace("$ARGUMENTS", "{{args}}")
    # Stringa literal multilinea ('''): nessun escape, prompt verbatim.
    content = (
        f"# {BANNER}\n"
        f'description = "{toml_escape(description)}"\n'
        f"prompt = '''\n{prompt}\n'''\n"
    )
    out = (GEMINI_REVIEW if review else GEMINI_COMMANDS) / f"{name}.toml"
    write(out, content)


def gen_copilot_prompt(name: str, description: str, body: str):
    prompt = body.replace("$ARGUMENTS", "${input}")
    content = (
        "---\n"
        f'description: "{yaml_dq(description)}"\n'
        "mode: agent\n"
        "---\n"
        f"<!-- {BANNER} -->\n\n"
        f"{prompt}\n"
    )
    write(COPILOT_PROMPTS / f"{name}.prompt.md", content)


def gen_copilot_chatmode(name: str, description: str, body: str):
    content = (
        "---\n"
        f'description: "{yaml_dq(description)}"\n'
        "tools: ['codebase', 'search', 'usages', 'findTestFiles', 'runCommands']\n"
        "---\n"
        f"<!-- {BANNER} -->\n\n"
        f"{body}\n"
    )
    write(COPILOT_CHATMODES / f"{name}.chatmode.md", content)


def main():
    print("Genero le utility per Gemini CLI e GitHub Copilot da .claude/ ...")

    print("\nSlash command (.claude/commands/ -> Gemini + Copilot):")
    for md in sorted(CLAUDE_COMMANDS.glob("*.md")):
        fm, body = parse_front_matter(md.read_text(encoding="utf-8"))
        name = md.stem
        description = fm.get("description", name)
        gen_gemini_command(name, description, body, review=False)
        gen_copilot_prompt(name, description, body)

    print("\nPersonas di review (.claude/agents/ -> Gemini command + Copilot chat mode):")
    for md in sorted(CLAUDE_AGENTS.glob("*.md")):
        fm, body = parse_front_matter(md.read_text(encoding="utf-8"))
        name = fm.get("name", md.stem)
        description = fm.get("description", name)
        gen_gemini_command(name, description, body, review=True)
        gen_copilot_chatmode(name, description, body)

    print("\nFatto.")


if __name__ == "__main__":
    main()
