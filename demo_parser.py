import sys
import os
import gnupg
import subprocess
from email.parser import Parser
parsermail = Parser()
from Signature.CheckSig import CheckSig
print("sono attivo")
s = ""
try:
    os.mkdir("/home/marco/appNewsMail/master/signaturefiles/")
except OSError:
    pass

###
#l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
for line in sys.stdin:
    s += line.replace("\n","\r\n")
with open("/home/marco/appNewsMail/master/signaturefiles/body.eml","w") as f:
    f.write(s)
    f.close()

email = parsermail.parsestr(s)
extracted = CheckSig.extractSignature(email)
if extracted:
    CheckSig.extractContent("/home/marco/appNewsMail/master/signaturefiles/body.eml")
    gpg = gnupg.GPG(gnupghome='/home/marco/.gnupg')
    sig = open("/home/marco/appNewsMail/master/signaturefiles/bodysig","rb")
    verified = gpg.verify_file(sig,"/home/marco/appNewsMail/master/signaturefiles/body.txt")
    print(verified.valid)
    print(verified.username[verified.username.find("<")+1:verified.username.find(">")])
