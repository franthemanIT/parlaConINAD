# parlaConINAD

Script Python **didattico** per interagire con INAD, l'Indice nazionale dei domicili digitali, tramite la PDND (Piattaforma Digitale Nazionale Dati - https://domiciliodigitale.gov.it).  
Gli script funzionano nell'**ambiente di collaudo** di PDND e di INAD.  
Dato il tenore didattico non ha molto senso usare gli script nell'ambiente di produzione, ma in tal caso dovrebbe essere sufficiente cambiare il valore delle variabili degli endpoint di PDND e INAD.  

L'interazione, tramite riga di comando, avviene:
- per interrogazioni singole con richiesta di inserire i dati della richiesta singola;
- per interrogazioni massive con richiesta di fornire un file CSV con una colonna di codici fiscali. Lo script estraiLista **restituisce lo stesso CSV con aggiunta dei dati del domicilio digitale**.

Lo script parlaConINAD.py contiene la definizione delle funzioni usate per l'interazione con INAD e per l'interfaccia utente (da riga di comando).  

PS: nell'ambiente INAD di collaudo ci sono dei domicili fittizi registrati, ma mi sembrano riferibili a chi sta lavorando al suo sviluppo, quindi non li ho resi visibili nel repository. Io li ho ricevuti dall'assistenza Infocamere: https://domiciliodigitale.gov.it/aswsWeb/selectLanding?idProduct=INAD&userRole=inadpa 

# Prerequisiti e configurazione

Si rimanda alla documentazione della PDND: https://docs.pagopa.it/interoperabilita-1/). In sintesi:
- aderire alla PDND;
- in ambiente di collaudo, creare l'accordo di fruizione dell'e-service "INAD API PUBBLICHE CONSULTAZIONE";
- attendere l'approvazione;
- creare coppia di chiavi come da documentazione;
- in ambiente di collaudo, creare un client e-service e caricarci la chiave pubblica;
- in ambiente di collaudo, creare una finalità per l'e-service "INAD API PUBBLICHE CONSULTAZIONE" e associarla al client e-service creato al punto precedente.

**Configurazione** di base:
1) nella cartella /chiavi salvare chiave pubblica e privata generate per il client e-service;
2) **creare il file datiINAD.py** a partire dallo schema datiINAD.schema.py con i **dati del client e-service recuperati dalla PDND** e con il percorso alla chiave privata.

# Avvertenze

Si tratta di un'**iniziativa didattica**, con lo scopo di:
- rendersi conto dell'interazione con INAD e del passaggio tramite PDND;
- individuare aspetti di criticità per integrazioni stabili ed eleganti con software "veri" in produzione.

Quindi: non ci sono controlli sui dati inseriti, la gestione di errori ed eccezioni è ridotta al minimo, le chiave privata con cui firmare è memorizzata in chiaro ecc.

Le specifiche delle API di INAD sono su GitHub: https://github.com/AgID/INAD_API_Extraction.  
Per visualizzarle in modo più comprensibile si può caricare il fiel YAML su https://editor.swagger.io/ (come link o come upload).  
La descrizione testuale è qui: https://domiciliodigitale.gov.it/dgit/home/public/docs/inad-specifiche_tecniche_api_estrazione.pdf
--> Attenzione: a metà giugno 2023, non c'è alineamento pieno fra sepcifiche API e loro descrizione testuale.

Soprattutto, per implementare **fuzioni sensate** e un **uso di INAD legittimo e utile** a chi lavora con i domicili digitali è fondamentale conoscere la **normativa**:  
- Codice dell'amministrazione digitale https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82!vig=2023-06-17, in particolare:
	- gli articoli 6-ter e 3-bis;
	- le modifiche apportate al CAD dall'articolo 24 del dl 76/2020 (https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2020-07-16;76!vig=2022-09-18)
- Linee guida AGID: https://trasparenza.agid.gov.it/moduli/downloadFile.php?file=oggetto_allegati/221871119160O__OLinee+guida+inad+ex+art.+6quater+cad.pdf


# Prerequisiti Python

Gli script fanno uso dei moduli:
- jose
- uuid
- os
- requests
- requests_oauth2
- socket
- json
- csv
- time
- datetime
- argparse
- uuid
- socket
  
Verificare di averli installati. Di solito sono tutti installati di default a part: jose, requests, requests_oauth2. 


# Script estraiCF.py

Cerca il domicilio digitale a partire da un codice fiscale. Richiede inoltre di specificare un riferimento al procedimento amministrativo nell'ambito del quale si richiede l'estrazione.  
Lanciare da riga di comando ("py estraiCF.py") e seguire le istruzioni a video.

Si consiglia di lanciarlo nella shell di Python (IDLE) così da poter fare ulteriori operazioni sulle variabili valorizzate (assertion, token, cf, ref) e sulla response (estrazione).  

# Script estraiCF2.py

Come estraiCF.py ma gestisce il riuso di un token JWT precedentemente ottenuto e ancora valido. Il token e la sua data di rilascio sono memorizzati nel file token_INAD.py.  
Si suggerisce di analizzare lo script estraiCF.py se si desidera avere l'idea dei passaggi dell'interazione con PDND e INAD.  

# Script estraiLista.py <--

Riceve in input un **file CSV** nel quale una colonna contiene codici fiscali.
Se non interrotto interroga perodicamente (variabile "pausa") il server di INAD per conoscere lo stato dell'elaborazione della richiesta e prelevare i risultati quando disponibili.  
Uso: py estraiLista.py <nomefile>.csv  
Se non specificato un file csv come argomento, cerca il file listaCF.csv (o altro configurato come defaultCSV)
L'output generato è salvato nella "cartella di lotto":
- in un file JSON come recuperato da INAD;
- in un file JSON che comprende il precendente unito alle risposte di INAD;
- in un file CSV che comprende i dati del **CSV originario con colonna/e aggiuntive per i domicili digitali** recuperati e l'eventuale professione del titolare.

Altri file di servizio creati nella cartella di lavoro:
- file JSON con il contenuto del file CSV ricevuto in input;
- file JSON di **ricevuta** della richiesta da parte di INAD (con dati aggiuntivi per il successivo recupero);
- file con lo stato dell'elaborazione (aggiornato all'ultima verifica);
- log del lotto: include parte di quanto scritto a video e eventuali risposte di INAD utili per debug;
- log di requests.

# Script recuperaLista.py

Riceve in input un file JSON di ricevuta di una lista di codici fiscali inviati in precedenza con estraiLista.py e procede al recupero dei risultati e a produrre i file di output.  
Uso: py recuperaLista.py .\cartelladilotto\filediricevuta.json  
Il risultato finale è lo stesso descritto per estraiLista.py.  


# Script verifica.py

Verifica la corrispondenza fra un codice fiscale e un domicilio digitale a uan certa data. Oltre a codice fiscale, indirizzo e-mail da verificare e data, richiede di specificare un riferimento al procedimento amministrativo nell'ambito del quale si richiede l'estrazione.  
Lanciare da riga di comando ("py verifica.py") e seguire le istruzioni a video.


# Script verifica2.py

Come verifica.py ma gestisce il riuso di un token JWT precedentemente ottenuto e ancora valido. Il token e la sua data di rilascio sono memorizzati nel file token_INAD.py.  
Si suggerisce di analizzare lo script verifica.py se si desidera avere l'idea dei passaggi dell'interazione con PDND e INAD.  


# Prossimamente
Seguiranno:
- miglioramento di inad.log (interpretazione delle response per annotazione significativa nel log)


**--> ATTENZIONE (per gli "spippolatori" del finesettimana): l'ambiente di test di Infocamere è attivo dal lunedì al venerdì dalle 7 alle 21.**
