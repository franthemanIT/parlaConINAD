import datiINAD
import parlaConINAD

def clear():
  os.system('clear')

def get_private_key(key_path):
  with open(key_path, "rb") as private_key:
    encoded_string = private_key.read()
    return encoded_string
  
key = get_private_key(datiINAD.keyPath)


a = input('Ci sarei, ho trovato anche la chiave.. premi invio')
cf = input('Inserisci il codice fiscale per cui verificare il domicilio digitale: ')
mail = input('Inserisci l\'indirizzo PEC da verificare: ')
data = input ('Inserisci la data alla quale verificare (AAAA-MM-GG): ')
ref = input('Inserisci un riferimento al procedimento amministrativo: ')

(assertion) = parlaConINAD.create_m2m_client_assertion(datiINAD.kid, datiINAD.alg, datiINAD.typ, datiINAD.iss, datiINAD.sub, datiINAD.aud, 0, 0, 0, key, datiINAD.PurposeID)
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
