# Standard — Qualità del Codice

Gli standard di questa sezione definiscono i criteri minimi verificabili per struttura del repository, gestione delle dipendenze, configurazione e qualità del codice. Derivano dai principi [P03](../principles/principles.md#p03--il-codice-esplorativo-non-è-codice-di-produzione) e [P04](../principles/principles.md#p04--la-configurazione-non-è-nel-codice).

Per le pratiche di implementazione vedere [practices/code-quality.md](../practices/code-quality.md).

---

## S03 — Repository Structure

**Ogni progetto ha una struttura di repository standard.**

### Struttura obbligatoria

```
project-name/
├── configs/                  # Configurazioni per ambiente (dev, staging, prod)
├── data/
│   ├── raw/                  # Dati originali — immutabili, mai modificati
│   └── processed/            # Dati trasformati — generati da codice
├── src/                      # Codice di produzione — moduli Python strutturati
├── tests/
│   ├── unit/                 # Unit test
│   ├── integration/          # Integration test
│   └── evals/                # Eval LLM e agentiche
├── notebooks/                # Esplorazione e comunicazione — mai in produzione
├── docs/
│   ├── architecture.md       # Architecture document (S01)
│   ├── decisions/            # ADR (S02)
│   └── runbook.md            # Runbook operativo (S15)
├── scripts/                  # Script di utilità e automazione
├── .env.example              # Template variabili d'ambiente
├── pyproject.toml            # Dipendenze e configurazione progetto
├── Makefile                  # Comandi standardizzati
└── README.md                 # Entry point — setup, utilizzo, contesto
```

### Estensione per progetti LLM e agentici

```
src/
├── prompts/                  # Prompt templates versionati
├── tools/                    # Tool definitions
└── agents/                   # Agent definitions
```

### Regole non negoziabili

- `notebooks/` e `src/` sono separati — nessun notebook in `src/`
- `data/raw/` è in sola lettura — nessuna modifica manuale ai dati originali
- `src/` contiene solo moduli Python — nessun notebook, nessuno script one-off
- `.env` è in `.gitignore` — mai committato

### Criterio di accettazione

> La struttura del repository rispecchia lo standard senza deviazioni non documentate.

---

## S04 — Dependency Management

**Le dipendenze sono esplicite, versioniate e ricostruibili.**

### Requisiti minimi

- `pyproject.toml` con versioni esplicite — nessun range vago, nessun `*`
- Lock file committato nel repository — `poetry.lock` o equivalente
- Ambiente virtuale per ogni progetto — nessuna dipendenza globale
- Separazione tra dipendenze di produzione e di sviluppo

### Criterio di accettazione

> L'ambiente di sviluppo è ricostruibile da zero eseguendo un singolo comando, producendo un ambiente identico a quello originale.

### Non accettabile

- `requirements.txt` senza versioni pinnate
- Dipendenze installate globalmente
- Lock file non committato o non aggiornato

---

## S05 — Configuration Management

**Nessun valore di configurazione, credenziale o parametro di ambiente è nel codice.**

### Requisiti minimi

- Nessun valore hardcoded nel codice per: URL, chiavi API, parametri di ambiente, credenziali
- `.env.example` committato con tutte le variabili necessarie e descrizione di ciascuna
- `.env` in `.gitignore` — mai committato in nessuna circostanza
- Configurazioni per ambiente in `configs/` come file separati — `dev.yaml`, `staging.yaml`, `prod.yaml`

### Criterio di accettazione

> Una scansione automatica del repository non rileva nessun secret o valore di configurazione hardcoded. `.env.example` documenta completamente tutte le variabili necessarie per far girare il sistema.

### Non accettabile

- Chiavi API nel codice, anche nei commenti
- URL di database hardcoded
- Password o token in qualsiasi file committato

---

## S06 — Code Quality

**Il codice rispetta standard minimi di qualità verificati automaticamente.**

### Requisiti minimi

- Linting automatico — nessun codice non conforme entra nel repository
- Formatting coerente — stile uniforme su tutto il codebase
- Type hints sulle funzioni pubbliche
- Pre-commit hooks attivi — i check vengono eseguiti prima di ogni commit

### Criteri di accettazione

> I check di qualità del codice sono automatizzati e il pipeline CI fallisce se non vengono soddisfatti. Non è possibile fare merge di codice non conforme.

### Non accettabile

- Code quality verificata solo manualmente
- Pre-commit hooks disabilitati o non configurati
- Funzioni pubbliche senza type hints

---

## Checklist di conformità

Prima della consegna, verificare:

```
□ Struttura del repository conforme allo standard S03
□ pyproject.toml con versioni esplicite e lock file committato (S04)
□ Nessun valore hardcoded nel codice (S05)
□ .env.example completo e aggiornato (S05)
□ Pre-commit hooks configurati e attivi (S06)
□ Pipeline CI esegue i check di qualità (S06)
```
