import json
import csv

lottoJson = "lotto.json"
domiciliJson = "domiciliDigitali.json"
chiaveCF = "codiceFiscale"
lottoElaboratoJson = "lottoElaborato.json"
outputCSV = "elaboratoCSV.csv"

with open(lottoJson, "r") as file:
	lotto = json.load(file)
	
with open(domiciliJson, "r") as file:
	listaDomicili = json.load(file)['list']
    

lottoElaborato = []

for soggetto in lotto:
    dizio = {}
    dizio.update(soggetto)
    chiave = soggetto[chiaveCF]
    for risultato in listaDomicili:
        if risultato["codiceFiscale"] == chiave:
            if "digitalAddress" in risultato:
                for address in risultato["digitalAddress"]:
                    indice = risultato["digitalAddress"].index(address)
                    suffisso = ('' if indice == 0 else str(indice+1)) 
                    dizio.update({"domicilioDigitale"+suffisso : address["digitalAddress"]})
                    if "practicedProfession" in address:
                        dizio.update({"professione"+suffisso : address["practicedProfession"]})
            print(dizio)
            break
    lottoElaborato.append(dizio)    

N = 0
for i in lottoElaborato:
    l=len(i)
    if l > N:
        posiz = lottoElaborato.index(i) # la posizione dell'elemento
    N = max(N,l)
        
fieldnames = list(lottoElaborato[posiz].keys())

with open(outputCSV, "w") as outputfile:
    writer = csv.DictWriter(outputfile, fieldnames=fieldnames, delimiter = ";", lineterminator="\n")
    outputfile.write(";".join(fieldnames))
    outputfile.write("\n")
    writer.writerows(lottoElaborato)
