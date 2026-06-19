# Pratiche — Gestione del Lavoro

Questa sezione definisce come implementare gli standard [S11](../standards/work-management.md#s11--issue-tracking), [S12](../standards/work-management.md#s12--commit-convention), [S13](../standards/work-management.md#s13--branch-strategy) e [S14](../standards/work-management.md#s14--definition-of-done).

---

## P11 — Issue Tracking

### Minimo

**GitLab Issues come sistema unico di tracking.**

**Label obbligatorie da configurare su ogni progetto:**

| Label | Colore | Quando usarla |
|---|---|---|
| `type::feature` | Verde | Nuova funzionalità |
| `type::bug` | Rosso | Comportamento errato |
| `type::spike` | Giallo | Ricerca e analisi tecnica |
| `type::refactor` | Blu | Refactoring senza cambiamento funzionale |
| `type::eval` | Viola | Aggiunta o modifica di eval ML/LLM |
| `type::docs` | Grigio | Documentazione |
| `priority::high` | Rosso scuro | Da completare nello sprint corrente |
| `priority::medium` | Arancione | Default |
| `priority::low` | Verde chiaro | Quando possibile |

**Board con stati obbligatori:**

```
Backlog → In Progress → In Review → Done
```

**Template issue minimo:**

```markdown
## Obiettivo
Cosa deve essere raggiunto con questo task.

## Criterio di completamento
Come si verifica che il task è Done.

## Note tecniche
Contesto rilevante, dipendenze, vincoli.
```

### Consigliato

- Milestone per raggruppare task per obiettivo o sprint
- Issue collegata all'ADR se il task implementa una decisione architetturale
- Weight sulle issue per stima dell'effort — scala Fibonacci: 1, 2, 3, 5, 8

### Avanzato

- Issue templates separati per tipo in `.gitlab/issue_templates/`
- Velocity tracking per stima realistica dei tempi futuri
- Retrospettiva sistematica a fine milestone con issue dedicata

---

## P12 — Commit Convention

### Minimo

**Conventional Commits** come standard. Vedere [S12](../standards/work-management.md#s12--commit-convention) per il formato completo.

**Configurazione Commitizen per enforcing:**

```toml
# pyproject.toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
tag_format = "v$version"
```

```bash
# Installazione
poetry add --group dev commitizen

# Commit con wizard interattivo
poetry run cz commit
```

**Pre-commit hook per validazione:**

```yaml
# .pre-commit-config.yaml
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

**Esempi corretti:**

```bash
feat(agent): add exponential backoff on tool call failure

Implements retry logic with configurable max attempts and base delay.
Backoff is applied only to transient errors (timeout, rate limit).

Refs: #42

fix(preprocessing): handle null values in ticket description field

Refs: #67

docs(runbook): add troubleshooting section for database connection errors

Refs: #71

eval(agent): add out-of-scope scenario tests for ticket routing

Refs: #55
```

### Consigliato

- Changelog generato automaticamente da commitizen: `cz changelog`
- Tag semantici generati automaticamente: `cz bump`

### Avanzato

- Semantic versioning completamente automatizzato in CI/CD basato sui commit

---

## P13 — Branch Strategy

### Minimo

**GitFlow semplificato:**

```
main
 └── develop
      ├── feature/42-agent-retry-logic
      ├── feature/55-eval-out-of-scope
      └── fix/67-null-handling-preprocessing
```

**Naming convention obbligatorio:**

```
feature/<issue-id>-<nome-descrittivo>
fix/<issue-id>-<nome-descrittivo>
refactor/<issue-id>-<nome-descrittivo>
eval/<issue-id>-<nome-descrittivo>
```

**Configurazione branch protection su GitLab** — obbligatoria su `main`:

```
Settings > Repository > Protected Branches

Branch: main
Allowed to push: No one
Allowed to merge: Maintainers
Require approval: 1 approvazione
```

**Workflow standard:**

```bash
# Creare una branch da develop
git checkout develop
git pull origin develop
git checkout -b feature/42-agent-retry-logic

# Sviluppo e commit
git add .
git commit  # usa commitizen

# Push e apertura MR
git push origin feature/42-agent-retry-logic
# Aprire MR su GitLab: feature/42-... → develop
```

**Merge Request template** — `.gitlab/merge_request_templates/Default.md`:

```markdown
## Issue collegata

Closes #<issue-number>

## Cambiamenti introdotti

Descrizione sintetica di cosa cambia e perché.

## Checklist

- [ ] Codice conforme agli standard di linting
- [ ] Test scritti e passanti
- [ ] Documentazione aggiornata se necessario
- [ ] Definition of Done verificata
- [ ] ADR creato se la MR introduce una decisione architetturale rilevante
```

### Consigliato

- Delete branch automatically after merge — configurato su GitLab
- Squash commits on merge per mantenere la storia di `main` pulita
- MR collegata all'issue tramite `Closes #<issue-id>` per chiusura automatica

### Avanzato

- **Trunk-based development** per team con CI/CD solido e alta frequenza di deploy
- Feature flags per deploy di funzionalità incomplete senza branch a lunga vita

---

## P14 — Definition of Done

### Minimo

File `docs/definition-of-done.md` nel repository di ogni progetto:

```markdown
# Definition of Done

Un task è considerato **Done** quando soddisfa tutti questi criteri.

## Criteri generali

- [ ] Codice revisionato e approvato da almeno un altro membro del team
- [ ] Tutti i test esistenti passano — nessuna regressione
- [ ] Test pertinenti al task scritti e passanti
- [ ] Nessun warning o errore di linting
- [ ] Documentazione aggiornata se il task introduce o modifica comportamento pubblico
- [ ] Issue collegata aggiornata con note rilevanti e chiusa
- [ ] Branch cancellata dopo il merge

## Criteri aggiuntivi per task ML/AI

- [ ] Esperimento tracciato su MLflow con parametri e metriche (se task di modeling)
- [ ] Eval aggiornata se il task modifica comportamento del modello o dell'agente
- [ ] Validation gate eseguito e documentato (se il task impatta il sistema in produzione)

## Criteri aggiuntivi per task agentici

- [ ] Tool registry aggiornato se il task introduce o modifica tool
- [ ] Suite di eval agentiche eseguita senza regressioni
- [ ] Osservabilità verificata — il nuovo comportamento è tracciato correttamente
```

### Consigliato

- DoD verificata come checklist nel template MR — integrata nel processo di review
- DoD distinta per tipo di task — una per feature, una per bug fix, una per spike

### Avanzato

- Verifica automatica di parte della DoD in CI/CD — linting, test, copertura
- DoD review trimestrale per aggiornamento in base alle lezioni apprese
