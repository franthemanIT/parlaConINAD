#dati client INAD di TEST

#dati per creare l'assertion m2m
kid = ''
typ = 'JWT'
iss = ''
sub = ''
aud = 'auth.uat.interop.pagopa.it/client-assertion'
alg = 'RS256'
PurposeID = ''
keyPath = '.\chiavi\...' #percorso della chiave privata che corrisponde alla chiave pubblica inserita nel client PDND

#dati per creare il token
Client_id = ''
Client_assertion_type = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
Grant_type = 'client_credentials'

#dati per invocare l'e-service INAD (ambiente di collaudo)
baseURL = 'https://domiciliodigitaleapi.oscl.infocamere.it/rest/inad/v1/domiciliodigitale'
