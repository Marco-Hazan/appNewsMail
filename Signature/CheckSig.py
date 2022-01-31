import sys
import os
import gnupg
import subprocess
from email.parser import Parser

class CheckSig:

    def extractContent(patheml):
        f = open(patheml, "rb")
        b = f.read()
        s = b.decode(encoding="ISO-8859-15")
        boundary = s.split('boundary=')[1].split('"')[1]
        cont = s.split("--"+boundary)[1]
        cont = cont[cont.find("\n")+1:].rstrip() + "\r\n"
        b = bytes(cont,"ISO-8859-15")
        f = open("/home/marco/appNewsMail/master/signaturefiles/body.txt", "wb")
        f.write(b)
        f.close()

    def extractSignature(email):
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() == 'application/pgp-signature':
                    with open("/home/marco/appNewsMail/master/signaturefiles/bodysig", 'w') as f:
                        f.write(str(part.get_payload()))
                        f.close()
                        return True
        return False

    def verifySignature(data,signer):
        try:
            os.mkdir("/home/marco/appNewsMail/master/signaturefiles/")
        except OSError:
            pass
        parsermail = Parser()
        with open("/home/marco/appNewsMail/master/signaturefiles/body.eml","w") as f:
            f.write(data)
            f.close()
        email = parsermail.parsestr(data)
        extracted = CheckSig.extractSignature(email)
        if extracted:
            CheckSig.extractContent("/home/marco/appNewsMail/master/signaturefiles/body.eml")
            gpg = gnupg.GPG(gnupghome='/home/marco/.gnupg')
            sig = open("/home/marco/appNewsMail/master/signaturefiles/bodysig","rb")
            verified = gpg.verify_file(sig,"/home/marco/appNewsMail/master/signaturefiles/body.txt")
            username = verified.username[verified.username.find("<")+1:verified.username.find(">")]
            if verified.valid and signer == username:
                print("Firma valida da "+ username)
                return True
            return False
            shutil.rmtree("/home/marco/appNewsMail/master/signaturefiles")
        return False

    #parsermail = Parser()
    #print("sono attivo")
    #s = ""
    #try:
        #os.mkdir("/home/marco/appNewsMail/master/signaturefiles/")
    #except OSError:
        #pass

    ###
    #l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
    #for line in sys.stdin:
        #s += line.replace("\n","\r\n")
