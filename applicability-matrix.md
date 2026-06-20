# Matrice di Applicabilità per Tipo di Soluzione

Gli standard di questo repository non si applicano in modo identico a tutte le soluzioni. Una RAG senza modello da addestrare non ha "run di training da tracciare"; un classificatore non ha tool da classificare per safety. Applicare uno standard dove non ha senso erode la fiducia nelle linee guida tanto quanto ometterlo dove serve.

Questo documento definisce **quali standard si applicano a quale tipo di soluzione** e, dove lo standard resta valido ma cambia di significato, **come si reinterpreta**.

---

## Archetipi di soluzione

| Archetipo | Descrizione | Caratteristica distintiva |
|---|---|---|
| **ML classico** | Modelli predittivi, classificazione, regressione, forecasting. Include il fine-tuning di LLM. | Esiste una fase di **training** su dati. La qualità si governa con dati, feature e iperparametri. |
| **GenAI / RAG** | LLM pre-addestrato usato senza training proprio: RAG, prompt engineering, chatbot, generazione. | **Nessuna fase di training.** La qualità si governa con prompt, retrieval, configurazione ed eval. |
| **Agentico** | Come GenAI/RAG, ma l'LLM seleziona e invoca tool che compiono azioni. | Presenza di **tool con effetti** (WRITE), in particolare WRITE-IRR. Autonomia, irreversibilità, non determinismo composto. |

### Note di soglia

- **Una RAG non è agentica** per il solo fatto di usare un LLM. Diventa agentica quando l'LLM sceglie e invoca tool con effetti collaterali. La soglia operativa è la presenza di tool WRITE — non la complessità percepita del sistema.
- **Il fine-tuning riattiva gli standard di training.** Un progetto GenAI che include fine-tuning torna a comportarsi, per S08–S09, come ML classico sul perimetro dei dati e dei run di addestramento.
- **Un sistema può essere ibrido.** Una soluzione agentica con componente RAG eredita gli obblighi di entrambe le colonne. Si applica l'unione, non l'intersezione.

---

## Matrice

| Standard | ML classico | GenAI / RAG | Agentico |
|---|---|---|---|
| **S01** Architecture document | Sì | Sì | Sì |
| **S02** ADR | Sì | Sì | Sì |
| **S03** Repository structure | Sì | Sì + `prompts/`, `tools/` | Sì + `prompts/`, `tools/`, `agents/` |
| **S04** Dependency management | Sì | Sì | Sì |
| **S05** Configuration management | Sì | Sì | Sì |
| **S06** Code quality | Sì | Sì | Sì |
| **S07** Environment reproducibility | Sì | Sì | Sì |
| **S08** Data reproducibility | Sì — pieno | **Reinterpretato** (corpus, non split) | **Reinterpretato** (corpus + prompt + tool come artefatti versionati) |
| **S09** Experiment tracking | Sì — run di training | **Reinterpretato** (eval run di configurazione) | **Reinterpretato** (eval run comportamentali) |
| **S10** Validation gates | Sì — metriche su test set | Sì — eval di qualità su golden set | Sì — behavioral eval (coincide con S20) |
| **S11** Issue tracking | Sì | Sì | Sì |
| **S12** Commit convention | Sì | Sì | Sì |
| **S13** Branch strategy | Sì | Sì | Sì |
| **S14** Definition of Done | Sì | Sì | Sì + criteri agentici |
| **S15** Runbook | Sì | Sì | Sì |
| **S16** Observability | Sì | Sì + tracing prompt/risposta | Sì → esteso da S21 (step, token, costo) |
| **S17** Handover | Sì | Sì | Sì |
| **S18** Tool safety | No | No (RAG puro non ha tool con effetti) | **Sì — obbligatorio** |
| **S19** Human-in-the-loop | No | No | **Sì — obbligatorio** |
| **S20** Agentic behavioral eval | No | No | **Sì — obbligatorio** |
| **S21** Agentic observability | No | No | **Sì — obbligatorio** |
| **S22** Perimeter definition | No | Consigliato (definire cosa il sistema non risponde) | **Sì — obbligatorio** |
| **S23** Cost control | No | Consigliato (budget token per richiesta) | **Sì — obbligatorio** |

La maggior parte degli standard è trasversale. Le differenze reali sono concentrate su **tre standard che cambiano significato** (S08, S09, S10) e su **sei standard che si applicano solo all'agentico** (S18–S23).

---

## Reinterpretazione degli standard di training per soluzioni senza training

### S08 — Data Reproducibility

Lo standard chiede dati raw immutabili, trasformazioni come codice versionato, split riproducibile, dataset identificati. Per soluzioni senza training, "i dati" sono altro — ma il principio (riproducibilità del materiale che determina il comportamento) resta intatto.

| | ML classico | GenAI / RAG | Agentico |
|---|---|---|---|
| **Cosa sono "i dati"** | Dataset di training/test | Corpus della knowledge base | Corpus + definizioni dei tool + prompt |
| **Raw immutabile** | Dataset raw in sola lettura | Documenti sorgente del corpus in sola lettura | Idem + tool registry versionato |
| **Trasformazione come codice** | Preprocessing, feature engineering | Pipeline di ingestion: parsing, chunking, embedding | Idem |
| **"Split" riproducibile** | Train/val/test con seed fisso | **Golden eval set fisso e versionato** | Scenari di eval (S20) versionati |
| **Identificazione versione** | Nome, versione, data del dataset | Versione del corpus + modello di embedding + strategia di chunking | Idem + versione dei prompt e dei tool |

> Criterio di accettazione reinterpretato per RAG: *dato un risultato di eval, è possibile identificare esattamente quale versione del corpus, quale embedding model e quale strategia di chunking l'hanno prodotto, e riprodurlo.*

### S09 — Experiment Tracking

Lo standard chiede di tracciare ogni run rilevante con parametri, metriche e versione del codice. Senza training non ci sono "run di addestramento" — ma ci sono **configurazioni di sistema confrontate tra loro su una metrica di qualità**, ed è esattamente ciò che va tracciato.

| | ML classico | GenAI / RAG | Agentico |
|---|---|---|---|
| **Cosa è un "esperimento"** | Una run di training con un set di iperparametri | Una configurazione di sistema valutata sull'eval set | Una versione dell'agente valutata sulla behavioral suite |
| **Parametri da loggare** | model type, learning rate, n_estimators… | modello, prompt version, chunk size, top-k, embedding model, temperatura | idem + tool disponibili, budget, policy di autonomia |
| **Metriche da loggare** | accuracy, F1, RMSE… | faithfulness, relevance, groundedness, latenza, costo | task completion rate, out-of-scope handling, costo/task, step medi |
| **Confronto tra versioni** | Quale config ha la metrica migliore | Idem | Idem + nessuna regressione sui quattro scenari (S20) |

> Il punto non è "tracciare il training" — è **non scegliere una configurazione di prompt o di retrieval a memoria o a impressione**. La promozione di una prompt version a produzione richiede lo stesso confronto tracciato che richiede la promozione di un modello.

### S10 — Validation Gates

Lo standard resta pienamente valido per tutti e tre gli archetipi; cambia solo **cosa** si misura nel gate.

| | ML classico | GenAI / RAG | Agentico |
|---|---|---|---|
| **Contenuto del gate** | Metriche su test set + edge case | Eval di qualità su golden set + edge case | Behavioral eval — i quattro scenari obbligatori di S20 |
| **Relazione con altri standard** | Autonomo | Autonomo | **Coincide con S20** — il validation gate agentico *è* la behavioral eval suite |

---

## Come usare questa matrice

1. Identifica l'archetipo della soluzione (o gli archetipi, se ibrida).
2. Applica tutti gli standard marcati **Sì** per quella colonna.
3. Per **S08, S09, S10**, usa la reinterpretazione corrispondente all'archetipo — non la versione ML-classica per default.
4. Applica **S18–S23** se e solo se il sistema è agentico (ha tool con effetti). Se ha tool WRITE-IRR, si applicano integralmente, indipendentemente dal rischio percepito.
