# parlaConINAD

Script Python didattico per interagire con INAD, l'Indice nazionale dei domicili digitali, tramite la PDND (Piattaforma Digitale Nazionale Dati).

Prerequisiti (si rimanda alla documentazione della PDND: https://docs.pagopa.it/interoperabilita-1/):
- aderire alla PDND;
- in ambiente di collaudo, creare l'accordo di fruizione dell'e-service "INAD API PUBBLICHE CONSULTAZIONE";
- attendere l'approvazione;
- creare coppia di chiavi come da documentazione;
- in ambiente di collaudo, creare un client e-service e caricarci la chiave pubblica;
- in ambiente di collaudo, creare una finalità per l'e-service "INAD API PUBBLICHE CONSULTAZIONE" e associarla al client e-service creato al punto precedente.

Configurazione di base:
1) Nella cartella /chiavi salvare chiave pubblica e privata generate per il client e-service;
2) Creare il file datiINAD.py a partire dallo schema datiINAD.schema.py con i dati del client e-service recuperati dalla PDND e con il percorso alla chiave privata.

# Avvertenze

Si tratta di un'iniziativa didattica, con lo scopo di:
- rendersi conto dell'interazione con INAD e del passaggio tramite PDND;
- individuare aspetti di criticità per integrazioni stabili ed eleganti con software "veri" in produzione.

Quindi: non ci sono controlli sui dati inseriti, la gestione di errori ed eccezioni è ridotta al minimo ecc.

Le specifiche delle API di INAD sono su GitHub: https://github.com/AgID/INAD_API_Extraction.  
Per visualizzarle in modo più comprensibile si può caricare il fiel YAML su https://editor.swagger.io/ (come link o come upload).  
La descrizione testuale è qui: https://domiciliodigitale.gov.it/dgit/home/public/docs/inad-specifiche_tecniche_api_estrazione.pdf

# Prerequisiti Python

Gli script fanno uso dei moduli:
- jose
- uuid
- os
- requests
- requests_oauth2
- socket
  
Verificare di averli installati.


# Script estraiCF.py

Cerca il domicilio digitale a partire da un codice fiscale. Richiede inoltre di specificare un riferimento al procedimento amministrativo nell'ambito del quale si richiede l'estrazione.  
Lanciare da riga di comando ("py estraiCF.py") e seguire le istruzioni a video.

Si consiglia di lanciarlo nella shell di Python (IDLE) così da poter fare ulteriori operazioni sulle variabili valorizzate (assertion, token, cf, ref) e sulla response (estrazione).  

# Script estraiCF2.py

Come estraiCF.py ma gestisce il riuso di un token JWT precedentemente ottenuto e ancora valido. Il token e la sua data di rilascio sono memorizzati nel file token_INAD.py.  
Si suggerisce di analizzare lo script estraiCF.py se si desidera avere l'idea dei passaggi dell'interazione con PDND e INAD.

# Script estraiListaCF.py

Riceve in input un file CSV nel quale una colonna contiene codici fiscali.  
Uso: py estraiListaCF.py <nomefile>.csv  
Se non specificato un file csv come argomento, cerca il file listaCF.csv
L'output generato è salvato nella "cartella di lotto".
Lo script è da completare:
- occorre attendere che l'elaborazione da parte di INAD sia pronta --> in preparazione uno script ulteriore che consente di recuperare l'esito di un'interrogazione fatta in precendeza;
- i domicili estratti sono memorizzati in un file JSON nella cartella di lotto --> in preparazione un'ulteriore elaborazione che restituisce un file CSV che aggiune al CSV orignario una o più coppie di colonne (domicilio digitale, professione);
- da prevedere la copia del CSV originario nella cartella di lotto (funzionale anche al punto precedente).

# Script verifica.py

Verifica la corrispondenza fra un codice fiscale e un domicilio digitale a uan certa data. Oltre a codice fiscale, indirizzo e-mail da verificare e data, richiede di specificare un riferimento al procedimento amministrativo nell'ambito del quale si richiede l'estrazione.  
Lanciare da riga di comando ("py verifica.py") e seguire le istruzioni a video.


# Script verifica2.py

Come verifica.py ma gestisce il riuso di un token JWT precedentemente ottenuto e ancora valido. Il token e la sua data di rilascio sono memorizzati nel file token_INAD.py.  
Si suggerisce di analizzare lo script verifica.py se si desidera avere l'idea dei passaggi dell'interazione con PDND e INAD.  


# Prossimamente
Seguiranno:
- miglioramento estrazione massiva;
- miglioramento di inad.log (interpretazione delle response per annotazione significativa nel log)


ATTENZIONE (per gli "spippolatori" del finesettimana): l'ambiente di test di Infocamere è attivo dal lunedì al venerdì dalle 7 alle 21
