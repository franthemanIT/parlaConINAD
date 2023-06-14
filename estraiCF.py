import datiINAD
import parlaConINAD

key = parlaConINAD.get_private_key(datiINAD.keyPath)

a = input('Ci sarei, ho trovato anche la chiave.. premi invio')
cf = input('Inserisci il codice fiscale per cui estrarre il domicilio digitale: ')
ref = input('Inserisci un riferimento al procedimento amministrativo: ')

assertion = parlaConINAD.create_m2m_client_assertion(datiINAD.kid, datiINAD.alg, datiINAD.typ, datiINAD.iss, datiINAD.sub, datiINAD.aud, 0, 0, 0, key, datiINAD.PurposeID)
#print(assertion)
with open("assertion.m2m", "w+") as file_ass:
    file_ass.write(assertion)

b = input('Ho creato l\'asserzione firmata, guarda il file assertion.. premi invio')

(token_response, body) = parlaConINAD.token_request(datiINAD.iss, assertion)

if token_response.status_code == 200:
  token = token_response.json()["access_token"]
  #print(token)
  a = input('Ho creato il token o voucher. Premi invio per estrarre il domicilio digitale...')
else:
  print("Non sono riuscito a creare il token, guarda un po\' token_response cosa dice..")


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
