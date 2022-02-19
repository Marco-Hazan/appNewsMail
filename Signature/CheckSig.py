import sys
import os
import gnupg
import shutil
import subprocess
from functions.config import Config
from email.parser import Parser

class CheckSig:

    def extractContent(patheml,msg):
        f = open(patheml, "rb")
        b = f.read()
        s = b.decode(encoding="ISO-8859-15")
        boundary = msg.get_boundary()[0:len(msg.get_boundary())-2]
        print(boundary)
        cont = s.split("--"+boundary)[1]
        cont = cont[cont.find("\n")+1:].rstrip() + "\r\n"
        b = bytes(cont,"ISO-8859-15")
        f = open(Config.get("master_path")+"signaturefiles/body.txt", "wb")
        f.write(b)
        f.close()

    def extractSignature(email):
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() == 'application/pgp-signature':
                    with open(Config.get("master_path")+"signaturefiles/bodysig", 'w') as f:
                        f.write(str(part.get_payload()))
                        f.close()
                        return True
        return False

    def verifySignature(data,signer):
        try:
            os.mkdir(Config.get("master_path")+"signaturefiles/")
        except OSError:
            pass
        parsermail = Parser()
        print("Ciao verify")
        with open(Config.get("master_path")+"signaturefiles/body.eml","w") as f:
            f.write(data)
            f.close()
        email = parsermail.parsestr(data)
        extracted = CheckSig.extractSignature(email)
        if extracted:
            CheckSig.extractContent(Config.get("master_path")+"signaturefiles/body.eml",email)
            gpg = gnupg.GPG(gnupghome = Config.get("pathtogpg"))
            sig = open(Config.get("master_path")+"signaturefiles/bodysig","rb")
            verified = gpg.verify_file(sig,Config.get("master_path")+"signaturefiles/body.txt")
            if not verified.username is None:
                username = verified.username[verified.username.find("<")+1:verified.username.find(">")]
                if verified.valid and signer == username:
                    print("Firma valida da "+ username)
                    shutil.rmtree(Config.get("master_path")+"signaturefiles")
                    return True
            shutil.rmtree(Config.get("master_path")+"signaturefiles")
            return False
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
