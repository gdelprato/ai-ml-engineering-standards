# Standard — Riproducibilità e Validazione

Gli standard di questa sezione definiscono i criteri minimi verificabili per riproducibilità degli ambienti, dei dati, degli esperimenti e per la validazione prima della consegna. Derivano dal principio [P05](../principles/principles.md#p05--la-riproducibilità-è-un-requisito-non-un-optional) e [P06](../principles/principles.md#p06--nessun-sistema-va-in-produzione-senza-criteri-di-validazione-espliciti).

Per le pratiche di implementazione vedere [practices/reproducibility.md](../practices/reproducibility.md).

---

## S07 — Environment Reproducibility

**L'ambiente di sviluppo è ricostruibile da chiunque in meno di 30 minuti.**

### Requisiti minimi

- `README.md` contiene una sezione Setup con istruzioni verificate e funzionanti
- `Makefile` espone almeno i comandi: `make setup`, `make test`, `make run`
- `.python-version` fissa la versione Python del progetto
- Le istruzioni di setup sono state verificate da un membro del team non coinvolto nel progetto

### Criterio di accettazione

> Un ingegnere che non ha mai visto il progetto riesce a configurare l'ambiente e far girare il sistema in meno di 30 minuti seguendo solo il README, senza chiedere assistenza.

### Non accettabile

- Setup che richiede passaggi non documentati
- Istruzioni che funzionano solo sulla macchina dell'autore
- Dipendenze da tool installati globalmente non documentati

---

## S08 — Data Reproducibility

**I dati raw sono immutabili. Ogni trasformazione è codice versionato e riproducibile.**

### Requisiti minimi

- `data/raw/` è in sola lettura — nessuna modifica manuale, mai
- Ogni trasformazione dei dati è uno script Python esplicito in `src/` — nessuna operazione manuale irripetibile
- Lo split train/validation/test è fisso, documentato e riproducibile — seed esplicito, non ricalcolato ad ogni run
- I dataset usati in training e evaluation sono identificati — nome, versione, data, fonte

### Criterio di accettazione

> Dato un risultato di training, è possibile identificare esattamente quali dati sono stati usati e rieseguire il training ottenendo risultati comparabili.

### Non accettabile

- Trasformazioni manuali sui dati raw
- Split train/test ricreato ad ogni run senza seed fisso
- Dataset non identificati o non versionati

---

## S09 — Experiment Tracking

**Ogni esperimento rilevante è tracciato con parametri, metriche e versione del codice.**

### Requisiti minimi

- Ogni run di training o fine-tuning rilevante è tracciata
- Per ogni run sono registrati: parametri, metriche, versione del codice, versione dei dati
- Gli esperimenti sono organizzati per progetto e obiettivo — non tutti in un unico spazio piatto
- È possibile confrontare esperimenti e identificare quale configurazione ha prodotto i risultati migliori

### Criterio di accettazione

> Data una decisione di modello, è possibile risalire all'esperimento che la giustifica, con parametri e metriche documentati.

### Non accettabile

- Risultati degli esperimenti tracciati solo a memoria o in chat
- Esperimenti non collegati alla versione del codice che li ha prodotti
- Impossibilità di confrontare esperimenti passati

---

## S10 — Validation Gates

**Prima di ogni consegna esistono criteri di validazione espliciti, eseguiti e documentati.**

### Requisiti minimi

- I criteri di accettazione sono definiti prima dell'inizio del progetto — non dopo
- Esiste una suite di validazione eseguita prima di ogni consegna o deploy
- Il risultato è esplicito e binario — passa o non passa — con log del risultato
- I criteri coprono almeno: correttezza funzionale, performance su test set, comportamento su edge cases

### Criteri aggiuntivi per sistemi LLM e agentici

- Behavioral eval su scenari rappresentativi con output atteso documentato
- Test di regressione che verificano il comportamento non sia degradato rispetto alla versione precedente

### Criterio di accettazione

> Esiste un report di validazione per ogni consegna che documenta i criteri verificati, i risultati ottenuti e la firma di approvazione.

### Non accettabile

- Validazione basata su impressione soggettiva
- Criteri di accettazione definiti dopo aver visto i risultati
- Consegna senza documentazione della validazione eseguita

---

## Checklist di conformità

Prima della consegna, verificare:

```
□ Setup verificato da membro del team non coinvolto nel progetto (S07)
□ data/raw/ non contiene modifiche manuali (S08)
□ Tutte le trasformazioni dati sono script Python versionati (S08)
□ Split train/validation/test documentato con seed fisso (S08)
□ Esperimenti rilevanti tracciati con parametri e metriche (S09)
□ Criteri di accettazione definiti e documentati (S10)
□ Suite di validazione eseguita con risultati documentati (S10)
```
