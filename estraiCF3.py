import datiINAD
import parlaConINAD
import datetime
import os

key = parlaConINAD.get_private_key(datiINAD.keyPath)
tokenFile = "token_INAD"
tokenPath = ".\\" + tokenFile + ".py"
durataToken = 86400

a = input('Ci sarei, ho trovato anche la chiave.. premi invio')
print('Verifico la validità del token disponibile')

## Verifica se un token valido è disponibile, altrimenti ne crea uno e lo memorizza nel file token_INAD.py
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

##Ottiene i dati da verificare
cf = input('Inserisci il codice fiscale per cui estrarre il domicilio digitale: ')
ref = input('Inserisci un riferimento al procedimento amministrativo: ')

##Estrazione del domicilio digitale da INAD
estrazione = parlaConINAD.estrai(token, cf, ref)
if estrazione.status_code == 200:
  print('Di seguito la response completa:')
  print(estrazione.content)
  try:
    print('Ecco il domicilio digitale di '+cf+': '+estrazione.json()["digitalAddress"][0]["digitalAddress"])
  except:
    print('L\'interazione è andata a buon fine, ma probabilmente il servizio è chiuso. Leggi sopra.')
else:
  if estrazione.status_code == 404:
    print('Domicilio digitale non trovato. Ragionevolmente '+cf+' non è registrato su INAD')
    print('Di seguito la response completa:')
    print(estrazione.json())
  else:
    print('Qualcosa è andato storto, lo status code della risposta è: '+estrazione.status_code+'. Consulta le specifiche per maggiori informazioni')
