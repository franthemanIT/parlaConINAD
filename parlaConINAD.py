from jose import jwt
from jose.constants import Algorithms
import datetime
import argparse
import uuid
import os
import requests
import requests_oauth2
import socket
import datiINAD

baseURL_auth = "https://auth.uat.interop.pagopa.it/token.oauth2"
baseURL_INAD = datiINAD.baseURL
logFileName="INAD.log"

def getIPAddress():
    return socket.gethostbyname(socket.gethostname())

callingIP = getIPAddress()
callingUser = os.getlogin()

def timestamp():
    return datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    
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
  os.system('clear')

def get_private_key(key_path):
  with open(key_path, "rb") as private_key:
    encoded_string = private_key.read()
    return encoded_string
    
def get_key(key_path):
  with open(key_path, "rb") as key:
    encoded_string = key.read()
    return encoded_string
    
def create_m2m_client_assertion(kid, alg, typ, iss, sub, aud, jti, iat, exp, key, purposeID = ""):  #iss e exp in realtà sono predeterminati, non argomenti così come jti, id univoco da creare sul momento
    issued = datetime.datetime.utcnow()
    delta = datetime.timedelta(minutes=43200)
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
    return(client_assertion)

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
        logRequest(logFile, requestTime, "POST", "requestToken", "xxxx")
        r = requests.post(baseURL_auth, headers = headers, timeout=100, data=body)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return(r, body)


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
    return(r)

def ottieniVoucher(client_id, purposeId = ""):
    pass
    
def estrai(token, cf, ref):  #cf è il codice fiscale, ref è il practicalReference cioè il riferimento al procedimento amministrativo per il quale si richiede l'estrazione
    url = baseURL_INAD+"/extract/"+cf
    headers = {'Authorization': 'Bearer '+token}
    #parameters = {'codice_fiscale' : cf, 'practicalReference' : ref}
    parametri = {'practicalReference' : ref}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "estrai", "richiesto domicilio digitale per "+cf)
        r = requests.get(url, headers = headers, params = parametri, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return(r)
    
def verifica(token, cf, ref, mail, data):  #cf è il codice fiscale, data è la data in cui verificare, ref è il practicalReference cioè il riferimento al procedimento amministrativo per il quale si richiede l'estrazione
    url = baseURL_INAD+"/verify/"+cf
    headers = {'Authorization': 'Bearer '+token}
    #parametri = {'codice_fiscale' : cf, 'practicalReference' : ref} #errati? il cf va in URL non in params
    parametri = {'practicalReference' : ref, 'digital_address' : mail, 'since' : data}
    #parametri = {'practicalReference' : ref, 'since' : data} #parametri incompleti per test
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "verifica", "richiesta verifica del domicilio digitale "+mail)
        r = requests.get(url, headers = headers, params = parametri, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return(r)
    
def caricaLista(token, lista, ref):
    url = baseURL_INAD+"/listDigitalAddress"
    headers = {'Authorization': 'Bearer '+token}
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
    return(r)
    
def statoLista(token, idLista):
    url = baseURL_INAD+"/listDigitalAddress/state/"+idLista
    headers = {'Authorization': 'Bearer '+token}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "verifica stato lista", "richiesta verifica stato per lista id "+idLista)
        r = requests.get(url, headers = headers, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return(r)

def prelevaLista(token, idLista):
    url = baseURL_INAD+"/listDigitalAddress/response/"+idLista
    headers = {'Authorization': 'Bearer '+token}
    with open(logFileName, "a+") as logFile:
        requestTime=timestamp()
        logRequest(logFile, requestTime, "GET", "verifica stato lista", "richiesta verifica stato per lista id "+idLista)
        r = requests.get(url, headers = headers, timeout=100)
        responseTime=timestamp()
        info = str(r.status_code)
        logResponse(logFile, responseTime, requestTime, r.status_code, info)
    return(r)
