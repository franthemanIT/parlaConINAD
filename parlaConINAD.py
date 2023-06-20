import datetime
import sys
#import argparse
import uuid
import os
import socket
import requests
#import requests_oauth2
from jose import jwt
from jose.constants import Algorithms
import datiINAD

baseURL_auth = "https://auth.uat.interop.pagopa.it/token.oauth2" #Ambiente PDND di collaudo
baseURL_INAD = datiINAD.baseURL
logFileName="INAD.log"

## Funzioni che servono per l'interazione con l'utente
def getIPAddress():
    return socket.gethostbyname(socket.gethostname())

callingIP = getIPAddress()
callingUser = os.getlogin()

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")

def attendi():
    q = input("Premi INVIO/ENTER per proseguire.")

def termina():
    q = input("Premi INVIO/ENTER per terminare.")
    sys.exit()

#def scegli(domanda):
    #q = input(domanda)
    #if q in listaOK:
        #risposta = True
    #else:
        #risposta = False
    #return risposta

listaOK = ["sì", "SI", "S", "s", "Sì", "OK", "si"] # elenco di parole da interpretare come risposta affermativa in caso di domanda posta dal programma

## Funzioni che servono per la manipolazione di file di input e output
def crea_cartella(suffisso, dataeora=""): # crea cartella con nome "dataeora-suffisso"
    x = timestamp() if dataeora=="" else dataeora
    path="./" + x + "-" + suffisso + "/"
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


## Funzioni che servono per il logging
def logRequest(logFile, requestTime, verbo, metodo, info):
    rigaDiLog=[requestTime, callingIP, callingUser, verbo, metodo, info]
    logFile.write(";".join(rigaDiLog))
    logFile.write("\n")
    logFile.flush()

def logResponse(logFile, responseTime, requestTime, status_code, info):
    rigaDiLog=[responseTime, callingIP, requestTime, str(status_code), info]
    logFile.write(";".join(rigaDiLog))
    logFile.write("\n")
    logFile.flush()
    
def clear():
    os.system("clear")

## Funzioni che servono per interazione con PDND per staccare il token
def get_private_key(key_path):
    with open(key_path, "rb") as private_key:
        encoded_string = private_key.read()
        return encoded_string
    
def get_key(key_path):
    with open(key_path, "rb") as key:
        encoded_string = key.read()
        return encoded_string

def create_m2m_client_assertion(kid, alg, typ, iss, sub, aud, key, purposeID = ""):  #crea l'asserzione firmata per ottenere il token da PDND
    issued = datetime.datetime.utcnow()
    delta = datetime.timedelta(minutes=2)
    expire_in = issued + delta
    jti = uuid.uuid4()
    headers_rsa = {
        "kid": kid,
        "alg": alg,
        "typ": typ
    }
    payload = {
        "iss": iss,
        "sub": sub,
        "aud": aud,
        "jti": str(jti),
        "iat": issued,
        "exp": expire_in,
        "purposeId" : purposeID
    }
    client_assertion = jwt.encode(payload, key, algorithm=Algorithms.RS256, headers=headers_rsa)
    return client_assertion

def token_request(client_id, client_assertion):
    client_assertion_type = datiINAD.Client_assertion_type
    grant_type = datiINAD.Grant_type
    body = {
        "client_id" : client_id,
        "client_assertion" : client_assertion,
        "client_assertion_type" : client_assertion_type,
        "grant_type" : grant_type
    }
    headers = {"Content-Type" : "application/x-www-form-urlencoded"}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "POST", "requestToken", client_id)
        r = requests.post(baseURL_auth, headers = headers, timeout=100, data=body)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return (r, body)


def getToken(client_id, client_assertion):
    client_assertion_type = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
    grant_type = "client_credentials"
    body = {
        "client_id" : client_id,
        "client_assertion" : client_assertion,
        "client_assertion_type" : client_assertion_type,
        "grant_type" : grant_type
    }
    headers = {"Content-Type" : "application/x-www-form-urlencoded"}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "POST", "requestToken", "richiesto JWT per client "+client_id)
        r = requests.post(baseURL_auth, headers = headers, timeout=100, data=body)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return r

## def ottieniVoucher(client_id, purposeId = ""):
##    pass


## Funzioni per l'interazione con INAD (autoesplicative)
def estrai(token, cf, ref):  #cf è il codice fiscale, ref è il practicalReference cioè il riferimento al procedimento amministrativo per il quale si richiede l'estrazione
    url = baseURL_INAD+"/extract/"+cf
    headers = {"Authorization": "Bearer "+token}
    #parameters = {"codice_fiscale" : cf, "practicalReference" : ref}
    parametri = {"practicalReference" : ref}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "estrai", "richiesto domicilio digitale per "+cf[:2]+"***")
        r = requests.get(url, headers = headers, params = parametri, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return r

def verifica(token, cf, ref, mail, data):  #cf è il codice fiscale, data è la data in cui verificare, ref è il practicalReference cioè il riferimento al procedimento amministrativo per il quale si richiede l'estrazione
    url = baseURL_INAD+"/verify/"+cf
    headers = {"Authorization": "Bearer "+token}
    parametri = {"practicalReference" : ref, "digital_address" : mail, "since" : data}
    #parametri = {"practicalReference" : ref, "since" : data} #parametri incompleti per test
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "verifica", "richiesta verifica del domicilio digitale "+mail[:3]+"***")
        r = requests.get(url, headers = headers, params = parametri, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return r

def caricaLista(token, lista, ref):
    url = baseURL_INAD+"/listDigitalAddress"
    headers = {"Authorization": "Bearer "+token}
    payload = {
                "codiciFiscali" : lista,
                "practicalReference" : ref
              }
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "POST", "carica lista di CF", "richiesta verifica massiva per "+ref)
        r = requests.post(url, headers = headers, json = payload, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return r

def statoLista(token, idLista):
    url = baseURL_INAD+"/listDigitalAddress/state/"+idLista
    headers = {"Authorization": "Bearer "+token}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "verifica stato lista", "richiesta verifica stato per lista id "+idLista)
        r = requests.get(url, headers = headers, timeout=100, allow_redirects = False)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return r

def prelevaLista(token, idLista):
    url = baseURL_INAD+"/listDigitalAddress/response/"+idLista
    headers = {"Authorization": "Bearer "+token}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "verifica stato lista", "richiesta verifica stato per lista id "+idLista)
        r = requests.get(url, headers = headers, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return r
