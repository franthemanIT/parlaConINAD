import datiINAD
import parlaConINAD
import datetime
import os
import json
import csv
import sys
import time
import os.path
import os

###import per annotare il log di requests
import logging
from http.client import HTTPConnection  # py3
log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)

## Varabili di ambiente (?)
key = parlaConINAD.get_private_key(datiINAD.keyPath)
tokenFile = "token_INAD"
tokenPath = ".\\" + tokenFile + ".py"
durataToken = 86400
listaOK = parlaConINAD.listaOK ##risposte da interpretare come sì come risposta affermativa in caso di domanda posta dal programma

## Acquisizione del motivo della richiesta
print("Benvenuto. Ti guiderò per cercare e aggiungere il domicilio digitale a una lista di codici fiscali contenuti in un file CSV.")
ref = input("Per iniziare, indica una breve descrizione del motivo della ricerca su INAD: ")
data_lotto = parlaConINAD.timestamp()

## Inizializzazione di cartella di lotto, file di output e logging
path=parlaConINAD.crea_cartella(ref, data_lotto) # crea la cartella di lavoro del lotto
lottoLog=path + data_lotto + "-" + "lotto.log"
ricevutaJson = path + data_lotto + "-ricevuta.json"
statoJson = path + data_lotto + "-stato.json"
domiciliJson = path + data_lotto + "-domiciliDigitali.json"
lottoJson=path + data_lotto + "-" + "Lotto.json"
#erroriCSV = path + data_lotto + "-" + "ErroriCSV.csv"
#risultatoCFJson=path + data_lotto + "-" + "RisultatoCF.json"
#esitoInviiJson=path + data_lotto + "-" + "EsitoInvii.json"
#inviiNonElaborati = path + data_lotto + "-" + "messaggiNonElaborati.csv" #NEW
requestsLog = path + data_lotto + "-" + "Requests.log"
fh = logging.FileHandler(requestsLog)
log.addHandler(fh)

# definisco la funzione stampa da usare al posto di print per scrivere il messaggio anche sul file Lotto.log - POI studaire un sistema migliore!!
def stampa(stringa):
   print(stringa)
   with open(lottoLog, 'a+') as fileLog:
      rigaDiLog=[parlaConINAD.timestamp(),stringa]
      fileLog.write(";".join(rigaDiLog))
      fileLog.write("\n")
      fileLog.flush()

def logga(stringa):
   with open(lottoLog, 'a+') as fileLog:
      rigaDiLog=[parlaConINAD.timestamp(),stringa]
      fileLog.write(";".join(rigaDiLog))
      fileLog.write("\n")
      fileLog.flush()

stampa("Ciao " + os.getlogin() + "!") #apre il lotto di log salutando l'utente
logga("Data della richiesta: "+data_lotto)
logga("Motivo della richiesta: "+ref)
## 1 File CSV come argomento

## 2 verifico esistenza del file
if len(sys.argv) > 1:
   if os.path.exists(sys.argv[1]):
      stampa("File "+sys.argv[1]+" trovato.")
      proseguire = input("Proseguire? (Sì/No):")
      if proseguire in listaOK:
         stampa("OK, proseguo.")
         nomeFileDati = sys.argv[1]
      else:
          q = input("Premi INVIO/ENTER per terminare.")
          stampa("Programma terminato.")
          exit()
   else:
      stampa("File di input non valido.")
      stampa("Per favore indicalo nel seguente modo: python <nomeDelTuoFile>.csv.")
      q = input("Premi INVIO/ENTER per terminare.")
      stampa("Programma terminato.")
      exit()
elif os.path.exists("listaCF.csv"):
   usa_default = input("Non hai indicato il file con i dati da processare. \nHo trovato il file listaCF.csv. Vuoi usare questo? (Sì/No): ")
   if usa_default in listaOK:
         stampa("OK, proseguo con questo file.")
         nomeFileDati = "listaCF.csv"
   else:
         stampa("Per favore indica il file con i dati da processare nel seguente modo:")
         stampa("python inviaLottoAvvisiDiPagamento.py <nomeDelTuoFile.csv>")
         q = input("Premi INVIO/ENTER per terminare.")
         stampa("Programma terminato.")
         exit()
else:
   stampa("Non hai indicato il file CSV con i dati da processare. Per favore indicalo nel seguente modo:")
   stampa("python inviaLottoAvvisiDiPagamento.py <nomeDelTuoFile.csv>")
   q = input("Premi INVIO/ENTER per terminare.")
   stampa("Programma terminato.")
   exit()

outputCSV = path + nomeFileDati
logga("Nome del file con i dati di input: "+nomeFileDati)
logga("Cartella di lavoro: "+path)


## 5 ci copio il CSV

## 6 importo il CSV in dizionario
with open(nomeFileDati, "r") as input:
    reader = csv.DictReader(input, delimiter=";")
    lotto = []
    for i in reader:
        lotto.append(i)
with open(lottoJson, "w+") as file:
    file.write(json.dumps(lotto, sort_keys=False, indent=4))

## 8 chiedo quale colonna contiene il codiceFiscale
print("Il CSV importato ha le seguenti chiavi:")
chiaviCSV = list(lotto[0].keys())
for i in chiaviCSV:
   print(i)
#chiaveCF = input("Indicare la chiave che contiene il codice fiscale: ")
chiaveCF = "codiceFiscale"
while not chiaveCF in chiaviCSV:
   chiaveCF = input("Indicare la chiave che contiene il codice fiscale: ")

## 9 estraggo lista di cf per INAD
listaCF = []
for i in lotto:
    listaCF.append(i[chiaveCF])
stampa("Ho estratto la lista di codici fiscali per cui richiedere il domicilio digitale.")

## Verifica se un token valido è disponibile, altrimenti ne crea uno e lo memorizza nel file token_INAD.py
stampa("Sono pronto per inviare la lista dei codici fiscali all'INAD.")
stampa('Verifico la validità del token disponibile.')
parlaConINAD.attendi()

if os.path.exists(".\\token_INAD.py"):
    import token_INAD
    allora = datetime.datetime.strptime(token_INAD.creato, '%a, %d %b %Y %H:%M:%S %Z')
    adesso = datetime.datetime.now()
    if int((adesso - allora).total_seconds()) < (durataToken-600):
       token = token_INAD.token
       print('Il token a disposizione è ancora valido')
    else:
       print('Il token a disposizione è scaduto. Ne ottengo un altro.')
       a = input('Premi INVIO per proseguire.')
       assertion = parlaConINAD.create_m2m_client_assertion(datiINAD.kid, datiINAD.alg, datiINAD.typ, datiINAD.iss, datiINAD.sub, datiINAD.aud, 0, 0, 0, key, datiINAD.PurposeID)
       with open("assertion.m2m", "w+") as file_ass:
         file_ass.write(assertion)
       b = input('Ho creato l\'asserzione firmata, guarda il file assertion.. premi invio')
       (token_response, body) = parlaConINAD.token_request(datiINAD.iss, assertion)
       if token_response.status_code == 200:
         token = token_response.json()["access_token"]
         creato = token_response.headers['date']
         with open(tokenPath, "w+") as File:
           File.write('token = \''+ token + '\'')
           File.write('\n')
           File.write('creato = \'' + creato + '\'')
           File.write('\n')
         a = input('Ho creato il token o voucher. Premi invio per estrarre il domicilio digitale...')
       else:
        print("Non sono riuscito a creare il token, guarda un po\' token_response cosa dice..")       
else:
    print('Nessun token disponibile. Ne ottengo uno.')
    assertion = parlaConINAD.create_m2m_client_assertion(datiINAD.kid, datiINAD.alg, datiINAD.typ, datiINAD.iss, datiINAD.sub, datiINAD.aud, 0, 0, 0, key, datiINAD.PurposeID)
    with open("assertion.m2m", "w+") as file_ass:
        file_ass.write(assertion)
    b = input('Ho creato l\'asserzione firmata, guarda il file assertion.. premi invio')
    (token_response, body) = parlaConINAD.token_request(datiINAD.iss, assertion)
    if token_response.status_code == 200:
      token = token_response.json()["access_token"]
      creato = token_response.headers['date']
      with open(tokenPath, "w+") as File:
        File.write('token = \''+ token + '\'')
        File.write('\n')
        File.write('creato = \'' + creato + '\'')
        File.write('\n')
      a = input('Ho creato il token o voucher. Premi invio per estrarre il domicilio digitale...')
    else:
      print("Non sono riuscito a creare il token, guarda un po\' token_response cosa dice..")

## Invio della lista dei codici fiscali a INAD
## Se OK, salvo la response come ricevuta.json nella cartella di lotto (con anche nome del CSV di partenza e cartella di lavoro)
invio = parlaConINAD.caricaLista(token, listaCF, ref)

#pausa = 120 + 2 * len(listaCF)
pausa = 10
if invio.status_code == 200:
    stampa("Lista dei file inviata correttamente. Attendo " + str(pausa) + " secondi per verificare lo stato della richiesta.")
    stampa("Ho salvato la ricevuta della richiesta nella cartella di lotto.")
    stampa("Puoi interrompere l'esecuzione del programma con CTRL+C e recuperare il risultato della ricerca con lo script recuperaLista.py.")
    with open(ricevutaJson, "w") as file:
        ricevuta = invio.json()
        ricevuta["nomeFileDati"] = nomeFileDati
        ricevuta["cartellaDiLavoro"] = path
        file.write(json.dumps(ricevuta,sort_keys=False, indent=4))
else:
    stampa("Qualcosa è andato storto. Faccio un po' di debug e ti faccio sapere... :)")
    stampa("Puoi controllare i log nella cartella di lotto.")
    parlaConINAD.termina()

## 12 attendo un tempo T = T(numero di cf richiesti)
time.sleep(pausa)

## 13 verifico stato e copio response in stato.json (se stato.json esiste, prendo l'id da ricevuta e lo sovrascrivo, se non esiste lo creo)
idLista = ricevuta['id']
verifica = parlaConINAD.statoLista(token, idLista)
listaPronta = False
while listaPronta == False:
    if verifica.status_code in [404, 303]: ## poi sarà 303:
        listaPronta == true
        stampa("La richiesta è stata elaborata da INAD. Procedo a prelevarla.")
        with open(statoJson, "w") as file:
            file.write(json.dumps(verifica.json(), sort_keys=False, indent=4))
        listaPronta = True
    elif verifica.status_code == 200:
        with open(statoJson, "w") as file:
            file.write(json.dumps(verifica.json(), sort_keys=False, indent=4))
        stampa("La richiesta è ancora in elaborazione. Attendo "+str(pausa)+" per verificare nuovamente. ")
        stampa("Puoi interrompere il programma con CTRL+C e verificare in seguito lo stato di elaborazione con verificaLista.py.")
        time.sleep(pausa)
    else: 
        stampa("Qualcosa non funziona. Magari è scaduto il token. Termino il programma. Esegui la verifica più tardi con verificaLista.py.")
        with open(statoJson, "w") as file:
            file.write(json.dumps(verifica.json(), sort_keys=False, indent=4))
        parlaConINAD.termina()
    
## 15 recupero i domicili e li salvo in domiciliDigitali.json
domicili = parlaConINAD.prelevaLista(token, idLista)
if domicili.status_code == 200:
    with open(domiciliJson, "w") as file:
        file.write(json.dumps(domicili.json(), sort_keys=False, indent = 4))
    stampa("Ho recuperato la lista dei domicili digitali.")
    stampa("La trovi nel file " + domiciliJson + " nella cartella di lavoro.")
else:
    stampa("Qualcosa è andato storto. Ti invito a guardare i file di log e riprovare più tardi con verificaLista.py.")

## 16 creo un nuovo csv (stesso nome con suffisso "_DD")con altre colonne per il codice fiscale e la professione eventuale. A tal fine:
##   - conto il numero massimo N di domicili trovati;
##   - aggiungo 2N colonne al CSV: domicilioDigitale, professione, domicilioDigitale2, peofessione2, ...., domicilioDigitaleN, professioneN
##with open("output.csv", "w") as output:
##    fieldnames=lotto[0].keys()
##    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter = ";", lineterminator="\n")
##    writer.writeheader
####    writer.writerows(lotto)
## --> da studiare come creare il CSV nuovo.. with open fileinput with open fileoutput... oppure uso il dizionario importato al passo 6, ci aggiungo i 2N nuovi chiavi/valori e poi converto in csv (con modulo csv)
## mi servono: os, datetime, json, csv.
## può capitare che mi rompo di aspettare e accolgo il suggerimento di interrompere con ctrl+c e poi lanciare "recuperaLista.py" con argomento la ricevuta.json
## recuperaLista parte da 14 (gestire l'impostazione della cartella di lotto come parlaConIO.verificaConsegnaLotto ... creare tabella lotto da lotto.json


