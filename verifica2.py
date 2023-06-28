import datetime
import os
import datiINAD
import parlaConINAD

key = parlaConINAD.get_private_key(datiINAD.keyPath)
tokenFile = "token_INAD"
tokenPath = ".\\" + tokenFile + ".py"
durataToken = 86400

a = input("Ci sarei, ho trovato anche la chiave.. premi INVIO/ENTER")
print("Verifico la validità del token disponibile")

if os.path.exists(".\\token_INAD.py"):
    import token_INAD
    allora = datetime.datetime.strptime(token_INAD.creato, "%a, %d %b %Y %H:%M:%S %Z")
    adesso = datetime.datetime.now()
    if int((adesso - allora).total_seconds()) < (durataToken-60):
        token = token_INAD.token
        print("Il token a disposizione è ancora valido")
    else:
        print("Il token a disposizione è scaduto. Ne ottengo un altro.")
        #a = input("Premi INVIO per proseguire.")
        assertion = parlaConINAD.create_m2m_client_assertion(datiINAD.kid, datiINAD.alg, datiINAD.typ, datiINAD.iss, datiINAD.sub, datiINAD.aud, key, datiINAD.PurposeID)
        #with open("assertion.m2m", "w+") as file_ass:
            #file_ass.write(assertion)
        #b = input("Ho creato l\'asserzione firmata, guarda il file assertion.. premi invio")
        (token_response, body) = parlaConINAD.token_request(datiINAD.iss, assertion)
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]
            creato = token_response.headers["date"]
            with open(tokenPath, "w+") as File:
                File.write("token = \'"+ token + "\'")
                File.write("\n")
                File.write("creato = \'" + creato + "\'")
                File.write("\n")
            #a = input("Ho creato il token o voucher. Premi invio per estrarre il domicilio digitale...")
            print("Ho creato il token (o voucher). Imvio la lista di codici fiscali a INAD...")
        else:
            print("Non sono riuscito a creare il token, guarda un po\' token_response cosa dice..")
else:
    print("Nessun token disponibile. Ne ottengo uno.")
    assertion = parlaConINAD.create_m2m_client_assertion(datiINAD.kid, datiINAD.alg, datiINAD.typ, datiINAD.iss, datiINAD.sub, datiINAD.aud, key, datiINAD.PurposeID)
    #with open("assertion.m2m", "w+") as file_ass:
        #file_ass.write(assertion)
    #b = input("Ho creato l\'asserzione firmata, guarda il file assertion.. premi invio")
    (token_response, body) = parlaConINAD.token_request(datiINAD.iss, assertion)
    if token_response.status_code == 200:
        token = token_response.json()["access_token"]
        creato = token_response.headers["date"]
        with open(tokenPath, "w+") as File:
            File.write("token = \'"+ token + "\'")
            File.write("\n")
            File.write("creato = \'" + creato + "\'")
            File.write("\n")
        #a = input("Ho creato il token o voucher. Premi invio per estrarre il domicilio digitale...")
        print("Ho creato il token (o voucher). Imvio la lista di codici fiscali a INAD...")
    else:
        print("Non sono riuscito a creare il token, guarda un po\' token_response cosa dice..")

#OTTIENI I DATI DA VERIFICARE
cf = input("Inserisci il codice fiscale per cui verificare il domicilio digitale: ")
mail = input("Inserisci l\'indirizzo PEC da verificare: ")
data = input ("Inserisci la data alla quale verificare (AAAA-MM-GG): ")
ref = input("Inserisci un riferimento al procedimento amministrativo: ")

verifica = parlaConINAD.verificaDomicilio(token, cf, ref, mail, data)
if verifica.status_code == 200:
    try:
        if verifica.json()["outcome"] is True:
            print("La verifica del domicilio digitale "+ mail +" per "+cf+" ha dato esito POSITIVO.")
        elif verifica.json()["outcome"] is False:
            print("La verifica del domicilio digitale "+ mail +" per "+cf+" ha dato esito NEGATIVO.")
    except:
        print("L\'interazione è andata a buon fine, ma probabilmente il servizio è chiuso. Leggi sopra.")
    print("Di seguito la response completa:")
    print(verifica.content)
elif verifica.status_code == 400:
    print("Richiesta mal formulata: " +verifica.json()["detail"])
elif verifica.status_code == 401:
    print("Non autorizzato: " + verifica.json()["detail"])
    print("Di seguito il contenuto completo della risposta: ")
    print(verifica.json())
elif verifica.status_code == 403:
    print:("Operazione non consentita: " + verifica.json()["detail"])
    print("Di seguito il contenuto completo della risposta: ")
    print(verifica.json())
elif verifica.status_code == 404:
    print(verifica.json()["status"] +" - " + verifica.json()["detail"])
    print("Quindi, l\'indirizzo PEC inserito non è domicilio digitale generale.")
    print("Di seguito il contenuto completo della risposta: ")
    print(verifica.json())
else:
    print("Qualcosa è andato storto, lo status code della risposta è: "+str(verifica.status_code)+". Consulta le specifiche per maggiori informazioni")
    print("Di seguito il contenuto completo della risposta: ")
    print(verifica.content)

parlaConINAD.termina()
