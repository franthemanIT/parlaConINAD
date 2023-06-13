# parlaConINAD

Script Python didattico per interagire con INAD, l'Indice nazionale dei domicili digitali, tramite la PDND (Piattaforma Digitale Nazionale Dati).

Prerequisiti (si irmando alla documentazione della PDND (https://docs.pagopa.it/interoperabilita-1/):
- aderire alla PDND;
- in ambiente di collaudo, creare l'accordo di fruizione dell'e-service "INAD API PUBBLICHE CONSULTAZIONE";
- attendere l'approvazione;
- creare coppia di chiavi come da documentazione;
- in ambiente di collaudo, creare client e-service per l'e-service "INAD API PUBBLICHE CONSULTAZIONE";
- in ambiente di collaudo, creare una finalità da associare al client e-service.

Configurazione di base:
1) Nella cartella /chiavi salvare chiave pubblica e privata generate per il client e-service;
2) Creare il file datiINAD.py a partire dallo schema datiINAD.schema.py con i dati del client e-service recuperati dalla PDND e con il percorso alla chiave privata.

Prerequisiti Python

Gli script fanno uso dei moduli:
- jose
- uuid
- os
- requests
- requests_oauth2
- socket
  
Verificare di averli installati.


Script estraiCF.py

Cerca il domicilio digitale a partire da un codice fiscale. Richiede inoltre di specificare un riferimento al procedimento amministrativo nell'ambito del quale si richiede l'estrazione.
Lanciare da riga di comando ("py estraiCF.py") e seguire le istruzioni a video.


Seguiranno: verifica di un domicilio digitale a una certa data, recupero massivo di domicili digitali a partire da un file CSV con una colonna che contiene codici fiscali.

ATTENZIONE (per gli "spippolatori" del finesettimana): l'ambiente di test di Infocamere è attivo dal lunedì al venerdì dalle 7 alle 21
