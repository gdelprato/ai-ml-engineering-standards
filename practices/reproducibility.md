# Pratiche — Riproducibilità e Validazione

Questa sezione definisce come implementare gli standard [S07](../standards/reproducibility.md#s07--environment-reproducibility), [S08](../standards/reproducibility.md#s08--data-reproducibility), [S09](../standards/reproducibility.md#s09--experiment-tracking) e [S10](../standards/reproducibility.md#s10--validation-gates).

---

## P07 — Environment Reproducibility

### Minimo

**`.python-version`** nel root del repository:

```
3.11.9
```

**`Makefile`** con setup completo e verificabile:

```makefile
.PHONY: setup verify-setup

setup:
	@echo "Verifico prerequisiti..."
	@python --version
	@poetry --version
	poetry install
	cp -n .env.example .env || true
	poetry run pre-commit install
	@echo "Setup completato. Configurare le variabili in .env prima di procedere."

verify-setup:
	@echo "Verifica ambiente..."
	poetry run python -c "import sys; print(f'Python {sys.version}')"
	poetry run python -c "from src.core import main; print('Import OK')"
	@echo "Ambiente verificato."
```

**Verifica obbligatoria prima della consegna:**

Un membro del team non coinvolto nel progetto esegue `make setup` su una macchina pulita e verifica che il sistema parta senza modifiche non documentate. L'esito viene annotato nella handover checklist.

### Consigliato

- Script `scripts/check-prerequisites.sh` che verifica tool richiesti e versioni
- `make setup` idempotente — eseguibile più volte senza effetti collaterali

### Avanzato

- **Docker** per isolamento completo:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY src/ ./src/
COPY configs/ ./configs/

CMD ["python", "-m", "src.main"]
```

- **Dev containers** per uniformità tra sviluppatori — `.devcontainer/devcontainer.json`

---

## P08 — Data Management

### Minimo

**Struttura dati obbligatoria:**

```
data/
├── raw/            # Dati originali — immutabili, mai modificati
│   └── .gitkeep    # La cartella è nel repository, i dati no
└── processed/      # Dati trasformati — generati da codice
    └── .gitkeep
```

`data/` in `.gitignore` — i dati non vanno nel repository. Solo la struttura.

**Script di trasformazione in `src/data/`:**

```python
# src/data/preprocessing.py

import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")
RANDOM_SEED = 42  # Fisso e documentato


def load_raw_data(filename: str) -> pd.DataFrame:
    """Carica dati raw senza modificarli."""
    return pd.read_csv(RAW_DATA_PATH / filename)


def create_train_test_split(
    df: pd.DataFrame,
    test_size: float = 0.2,
    val_size: float = 0.1,
    seed: int = RANDOM_SEED,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split fisso e riproducibile.
    Seed documentato — non modificare senza ADR.
    """
    ...
```

**README del dataset in `data/raw/README.md`:**

```markdown
# Dataset

## Fonte
- Nome: ...
- URL o sistema di origine: ...
- Data di estrazione: YYYY-MM-DD
- Versione: ...

## Schema
| Campo | Tipo | Descrizione |
|---|---|---|
| ... | ... | ... |

## Note
...
```

### Consigliato

**DVC per data versioning:**

```bash
# Inizializzare DVC
dvc init

# Tracciare un dataset
dvc add data/raw/dataset.csv

# Configurare remote storage
dvc remote add -d myremote s3://bucket/path

# Push dei dati
dvc push

# Pull dei dati su altra macchina
dvc pull
```

- `data/raw/dataset.csv.dvc` committato nel repository
- `data/raw/dataset.csv` in `.gitignore`
- Versione del dataset loggata in ogni run di training

**Data validation con Pydantic:**

```python
from pydantic import BaseModel, validator

class TicketRecord(BaseModel):
    ticket_id: str
    priority: int
    description: str
    created_at: str

    @validator("priority")
    def priority_must_be_valid(cls, v: int) -> int:
        if v not in range(1, 6):
            raise ValueError(f"Priority must be 1-5, got {v}")
        return v
```

### Avanzato

- Great Expectations per data quality checks automatizzati
- Data lineage documentato con tool dedicati — OpenLineage, Marquez
- Feature store per riuso di feature tra progetti

---

## P09 — Experiment Tracking

### Minimo

**MLflow come tool standard:**

```bash
# Installazione
poetry add mlflow

# Avvio UI locale
mlflow ui
```

**Pattern di tracking obbligatorio:**

```python
import mlflow

# Ogni progetto ha il suo experiment
mlflow.set_experiment("project-name/objective")

with mlflow.start_run(run_name="descrizione-sintetica"):
    # Log parametri
    mlflow.log_params({
        "model_type": "random_forest",
        "n_estimators": 100,
        "max_depth": 5,
        "random_seed": 42,
        "dataset_version": "v1.2",
    })

    # Training
    model = train_model(...)

    # Log metriche
    mlflow.log_metrics({
        "accuracy": accuracy,
        "f1_score": f1,
        "precision": precision,
        "recall": recall,
    })

    # Log artefatti
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_artifact("data/processed/train_split_info.json")
```

**Naming convention per gli esperimenti:**

```
{project-name}/{objective}/{variant}

Esempi:
ticket-classifier/priority-prediction/baseline
ticket-classifier/priority-prediction/with-embeddings
agent-tickets/tool-selection/langchain-v2
```

### Consigliato

**MLflow Model Registry per modelli in produzione:**

```python
# Registrare un modello
mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="ticket-priority-classifier",
)

# Transizione a produzione
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="ticket-priority-classifier",
    version=3,
    stage="Production",
)
```

- Ogni promozione a produzione richiede confronto esplicito con la versione precedente
- Tag per collegare il run all'issue GitLab che lo ha motivato

### Avanzato

- MLflow integrato con CI/CD — ogni PR che tocca il modello esegue un run di confronto automatico
- Criteri di promozione automatica basati su soglie di metrica documentate

---

## P10 — Validation Gates

### Minimo

**Criteri di accettazione nel repository:**

File `docs/acceptance-criteria.md` creato prima dell'inizio del progetto:

```markdown
# Criteri di Accettazione

**Definiti il:** YYYY-MM-DD
**Da:** [nome]
**Approvati da:** [nome cliente o stakeholder]

## Metriche di performance

| Metrica | Soglia minima | Target |
|---|---|---|
| Accuracy | > 0.85 | > 0.90 |
| Latenza p95 | < 500ms | < 200ms |
| ... | ... | ... |

## Casi d'uso obbligatori

- [ ] Il sistema gestisce correttamente i ticket di priorità 1
- [ ] Il sistema gestisce correttamente ticket con descrizione vuota
- [ ] Il sistema risponde entro il timeout definito

## Criteri di esclusione

Il sistema NON viene considerato pronto se:
- Accuracy < 0.85 sul test set
- Fallisce su qualsiasi caso d'uso obbligatorio
- Latenza p95 > 500ms
```

**Esecuzione e documentazione prima della consegna:**

```bash
make validate  # Esegue la suite di validazione completa
```

Output salvato in `docs/validation-report-YYYY-MM-DD.md`.

### Consigliato

**pytest per test strutturati con report:**

```bash
poetry run pytest tests/ \
    --tb=short \
    --junitxml=reports/test-results.xml \
    -v
```

- Test di regressione che confrontano le performance con la versione precedente
- Behavioral tests per LLM — scenari con input/output attesi documentati

### Avanzato

- Automated evaluation pipeline in CI/CD — ogni PR esegue la suite di validazione
- A/B testing framework per confronto tra versioni in produzione
- Automated rollback se le metriche in produzione degradano oltre soglia
