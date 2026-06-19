# Pratiche — Qualità del Codice

Questa sezione definisce come implementare gli standard [S03](../standards/code-quality.md#s03--repository-structure), [S04](../standards/code-quality.md#s04--dependency-management), [S05](../standards/code-quality.md#s05--configuration-management) e [S06](../standards/code-quality.md#s06--code-quality).

---

## P03 — Repository Structure

### Minimo

Utilizzare la struttura standard definita in [S03](../standards/code-quality.md#s03--repository-structure) su ogni nuovo progetto.

**Makefile obbligatorio con almeno questi target:**

```makefile
.PHONY: setup test lint run clean

setup:
	poetry install

test:
	poetry run pytest tests/

lint:
	poetry run ruff check src/
	poetry run ruff format --check src/

run:
	poetry run python src/main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
```

**README.md con sezione Setup obbligatoria:**

```markdown
## Setup

### Prerequisiti
- Python 3.11+
- Poetry

### Installazione

\`\`\`bash
make setup
cp .env.example .env
# Configurare le variabili in .env
\`\`\`

### Esecuzione

\`\`\`bash
make run
\`\`\`

### Test

\`\`\`bash
make test
\`\`\`
```

### Consigliato

- Script di setup che verifica i prerequisiti e guida l'utente se mancano
- `make check` che esegue lint + test in sequenza
- Documentazione dei comandi Make nel README

### Avanzato

- Repository template come progetto Git separato — ogni nuovo progetto parte con `cookiecutter` o strumento equivalente
- Scaffolding automatizzato che genera la struttura con un singolo comando

---

## P04 — Dependency Management

### Minimo

**Poetry come tool standard:**

```bash
# Inizializzare un nuovo progetto
poetry init

# Aggiungere dipendenza di produzione
poetry add <package>

# Aggiungere dipendenza di sviluppo
poetry add --group dev <package>

# Installare da lock file
poetry install

# Aggiornare lock file
poetry update
```

**`pyproject.toml` con gruppi separati:**

```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
python = "^3.11"

[tool.poetry.dependencies]
# Dipendenze di produzione

[tool.poetry.group.dev.dependencies]
# Dipendenze di sviluppo — test, linting, type checking
ruff = "^0.4"
pytest = "^8.0"
mypy = "^1.0"
pre-commit = "^3.0"
```

**Versioni esplicite — non range vaghi:**

```toml
# Corretto
langchain = "^0.2.0"

# Non accettabile
langchain = "*"
langchain = ">=0.1"
```

### Consigliato

- `poetry.lock` committato e aggiornato — verificato in CI
- Aggiornamenti delle dipendenze come task espliciti in backlog — non aggiornamenti ad hoc
- Separazione ulteriore: gruppo `test`, gruppo `lint`, gruppo `docs`

### Avanzato

- Dependency scanning automatico in CI — verifica vulnerabilità note
- Renovate o Dependabot configurato per PR automatiche di aggiornamento

---

## P05 — Configuration Management

### Minimo

**Struttura della configurazione:**

```
configs/
├── dev.yaml        # Sviluppo locale
├── staging.yaml    # Pre-produzione
└── prod.yaml       # Produzione
```

**`.env.example` — obbligatorio e documentato:**

```bash
# API Keys
OPENAI_API_KEY=             # Chiave API OpenAI — ottenibile da platform.openai.com
ANTHROPIC_API_KEY=          # Chiave API Anthropic

# Database
DATABASE_URL=               # Connection string — formato: postgresql://user:pass@host:port/db

# Environment
ENVIRONMENT=dev             # dev | staging | prod
LOG_LEVEL=INFO              # DEBUG | INFO | WARNING | ERROR

# Application
MAX_RETRIES=3               # Numero massimo di retry per chiamate esterne
REQUEST_TIMEOUT=30          # Timeout in secondi per le richieste HTTP
```

**Caricamento configurazione con Pydantic Settings:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str
    environment: str = "dev"
    log_level: str = "INFO"
    max_retries: int = 3
    request_timeout: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

Il sistema fallisce all'avvio se una variabile obbligatoria è assente — non in runtime.

### Consigliato

- Configurazione caricata una volta all'avvio come singleton — non ricaricata ad ogni uso
- Validazione dei valori di configurazione oltre alla presenza — range, formato, enum
- Configurazione per ambiente gestita tramite variabile `ENVIRONMENT`

### Avanzato

- Secret management centralizzato — HashiCorp Vault, AWS Secrets Manager, Azure Key Vault
- Rotazione automatica dei secret con zero-downtime

---

## P06 — Code Quality

### Minimo

**`ruff` per linting e formatting:**

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.ruff.format]
quote-style = "double"
```

**Pre-commit hooks — `.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
```

**Installazione:**

```bash
poetry run pre-commit install
```

**Type hints obbligatori sulle funzioni pubbliche:**

```python
# Corretto
def process_ticket(ticket_id: str, priority: int) -> dict[str, Any]:
    ...

# Non accettabile
def process_ticket(ticket_id, priority):
    ...
```

### Consigliato

- `mypy` per type checking statico:

```toml
[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

- Docstring obbligatorie per funzioni pubbliche — formato Google o NumPy
- Complexity check — funzioni con complessità ciclomatica > 10 richiedono refactoring

### Avanzato

- Quality gates in CI — il pipeline fallisce se la copertura dei type hints scende sotto soglia
- Code review checklist standardizzata inclusa nel template MR di GitLab
- Mutation testing per verificare la qualità dei test
