import datiINAD
import parlaConINAD
import datetime
import os

def clear():
  os.system('clear')

def get_private_key(key_path):
  with open(key_path, "rb") as private_key:
    encoded_string = private_key.read()
    return encoded_string
  
key = get_private_key(datiINAD.keyPath)
tokenFile = "token_INAD"
tokenPath = ".\\" + tokenFile + ".py"
durataToken = 86400

a = input('Ci sarei, ho trovato anche la chiave.. premi invio')
print('Verifico la validità del token disponibile')

if os.path.exists(".\\token_INAD.py"):
    import token_INAD
    allora = datetime.datetime.strptime(token_INAD.creato, '%a, %d %b %Y %H:%M:%S %Z')
    adesso = datetime.datetime.now()
    if int((adesso - allora).total_seconds()) < (durataToken-60):
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

#OTTIENI I DATI DA VERIFICARE
cf = input('Inserisci il codice fiscale per cui verificare il domicilio digitale: ')
mail = input('Inserisci l\'indirizzo PEC da verificare: ')
data = input ('Inserisci la data alla quale verificare (AAAA-MM-GG): ')
ref = input('Inserisci un riferimento al procedimento amministrativo: ')

verifica = parlaConINAD.verifica(token, cf, ref, mail, data)
if verifica.status_code == 200:
  print('Di seguito la response completa:')
  print(verifica.content)
  try:
    print('La verifica del domicilio digitale '+mail+' per '+cf+' ha dato esito: '+verifica.json()["outcome"])
  except:
    print('L\'interazione è andata a buon fine, ma probabilmente il servizio è chiuso. Leggi sopra.')
else:
  if verifica.status_code == 404:
    print('Domicilio digitale non trovato. Ragionevolmente '+cf+' non è registrato su INAD. Quindi, l\'indirizzo PEC non è domicilio digitale generale.')
    print('Di seguito la response completa:')
    print(verifica.json())
  else:
    print('Qualcosa è andato storto, lo status code della risposta è: '+verifica.status_code+'. Consulta le specifiche per maggiori informazioni')
