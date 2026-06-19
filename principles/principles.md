# Principi Fondamentali

I principi definiscono il perché del modello di lavoro. Sono non negoziabili, indipendenti dal contesto tecnologico e stabili nel tempo. Ogni standard e ogni pratica di questo repository deriva da uno o più di questi principi.

---

## P01 — L'architettura prima del codice

Ogni soluzione ha un'architettura esplicita e documentata prima che venga scritto codice di produzione.

**Criterio verificabile:** Esiste un documento di architettura che un nuovo membro del team può leggere per capire cosa fa il sistema, come è strutturato e perché sono state fatte le scelte principali.

**Problema che risolve:** Codice scritto senza architettura definita produce sistemi non comprensibili, non manutenibili e non consegnabili.

---

## P02 — Ogni decisione tecnica è tracciata

Ogni decisione tecnica rilevante — architettura, modello, approccio, tool — è documentata con il contesto, le alternative considerate e la motivazione della scelta.

**Criterio verificabile:** Esiste un registro delle decisioni architetturali che spiega il perché delle scelte principali, non solo il cosa.

**Problema che risolve:** Le decisioni prese a memoria non sono trasferibili, non sono difendibili e non permettono di imparare da progetti precedenti.

---

## P03 — Il codice esplorativo non è codice di produzione

L'esplorazione e la produzione sono fasi distinte con artefatti distinti. Un notebook non va mai in produzione.

**Criterio verificabile:** Il codice di produzione vive in moduli Python strutturati, testabili e versionati. I notebook esistono solo nella cartella di esplorazione e non contengono logica di business critica.

**Problema che risolve:** I notebook come artefatti di produzione producono sistemi non testabili, non versionabili e non manutenibili.

---

## P04 — La configurazione non è nel codice

Tutto ciò che cambia tra ambienti o contesti vive nella configurazione, non nel codice. I secret non vengono mai committati.

**Criterio verificabile:** Il repository non contiene nessun valore hardcoded di ambiente o credenziale. Esiste un `.env.example` che documenta tutte le variabili necessarie.

**Problema che risolve:** Configurazione nel codice rende impossibile separare dev da prod, crea rischi di sicurezza e impedisce la riproducibilità cross-ambiente.

---

## P05 — La riproducibilità è un requisito, non un optional

Qualsiasi membro del team deve poter ricreare l'ambiente, i dati e i risultati di qualsiasi progetto senza chiedere aiuto all'autore originale.

**Criterio verificabile:** Un membro del team non coinvolto nel progetto riesce a farlo girare da zero in meno di 30 minuti seguendo solo la documentazione.

**Problema che risolve:** Sistemi riproducibili solo dall'autore originale non sono consegnabili, non sono manutenibili e creano dipendenze personali che non scalano.

---

## P06 — Nessun sistema va in produzione senza criteri di validazione espliciti

Prima di qualsiasi deploy o consegna, esistono criteri espliciti e misurabili che definiscono cosa significa "funziona".

**Criterio verificabile:** Esiste una suite di test o eval eseguita prima di ogni consegna. Il risultato è documentato — passa o non passa — con criteri definiti prima dell'inizio del progetto, non dopo.

**Problema che risolve:** Consegnare senza criteri di validazione espliciti significa non sapere se il sistema funziona, con quali limiti e in quali condizioni fallisce.

---

## P07 — Ogni task è esplicito, tracciato e collegato al suo contesto

Ogni attività di sviluppo — feature, bug, spike, ricerca — esiste come task esplicito in un sistema di tracking prima di essere iniziata. Niente lavoro invisibile.

**Criterio verificabile:** Guardando il sistema di tracking si capisce lo stato reale del progetto senza dover chiedere a nessuno.

**Problema che risolve:** Il lavoro invisibile non è pianificabile, non è comunicabile al cliente e non è trasferibile ad altri membri del team.

---

## P08 — Il codice è sempre collegato a un task

Ogni commit, ogni branch, ogni merge request è collegato a un task esplicito. Il codice senza contesto non esiste.

**Criterio verificabile:** Da qualsiasi commit si risale al task che lo ha generato, e dal task si capisce il perché della modifica.

**Problema che risolve:** Codice senza contesto è non debuggabile, non revisionabile e non trasferibile.

---

## P09 — Il workflow di sviluppo è definito e condiviso

Esiste un workflow esplicito che definisce come si passa da un requisito a codice in produzione. Tutti lo conoscono, tutti lo seguono.

**Criterio verificabile:** Un nuovo membro del team capisce come lavorare leggendo il workflow, senza dover osservare gli altri o chiedere come si fa.

**Problema che risolve:** Workflow impliciti producono qualità inconsistente, dipendenza dalle persone chiave e impossibilità di onboarding rapido.

---

## P10 — La consegna è un sistema, non un artefatto

Una consegna include non solo il sistema funzionante ma anche la documentazione operativa, i criteri di monitoraggio e le istruzioni per la manutenzione.

**Criterio verificabile:** Il cliente può operare il sistema consegnato senza dipendere dalla presenza del team che lo ha costruito.

**Problema che risolve:** Consegnare un artefatto senza contesto operativo trasferisce il problema, non la soluzione.

---

## Relazione tra principi e standard

| Principio | Standard collegati |
|---|---|
| P01 — Architettura prima del codice | S01, S02 |
| P02 — Decisioni tracciate | S02 |
| P03 — Codice esplorativo vs produzione | S03 |
| P04 — Configurazione separata | S05 |
| P05 — Riproducibilità | S07, S08, S09 |
| P06 — Validazione esplicita | S10 |
| P07 — Task espliciti | S11 |
| P08 — Codice collegato a task | S12, S13 |
| P09 — Workflow condiviso | S13, S14 |
| P10 — Consegna come sistema | S15, S16, S17 |
