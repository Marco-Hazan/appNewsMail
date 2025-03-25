from functions.extract import Extraction
import gnupg
import subprocess
import string
import random
import secrets
import time
from datetime import datetime as dt
import hashlib
from Dao.newsmailDao import newsmailDao
from Dao.SenderDao import SenderDao
from functions.config import Config
from functions.mailfunctions import MailFunction


def get_random_string(length):
    # choose from all lowercase letter
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
'''
def set_auth_token(username):
    lastnews = newsmailDao.getLast(username)
    if lastnews is not None:
        msgid = lastnews.msgid
    else:
        msgid = ''
    now = dt.now()
    return   str(now.minute)+ ":" + hashlib.sha256((msgid+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute + 10)).encode("utf-8")).hexdigest()[0:16]

def verify_token(username,token):
    lastnews = newsmailDao.getLast(username)
    if lastnews is not None:
        msgid = lastnews.msgid
    else:
        msgid = ''
    now = dt.now()
    minutes = token[:token.find(":")]
    realtoken = minutes + ":" + hashlib.sha256(msgid+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(minutes+10)).hexdigest()[0:16]
    return token == realtoken
'''
class RegistrationHandler:

    def isRegistrationPattern(pattern):
        print("PATTERN REGISTRAZIONE: "+pattern)
        return (
            "Sign up" in pattern or
            "confirm identity" in pattern
            )

    def handleRegistration(pattern,msg):
        if RegistrationHandler.isRegistrationPattern(pattern):
            user = Extraction.extractSender(msg)
            fullname = Extraction.extractBody(msg)
            firstname = ''
            lastname = ''
            print("HOHOHOHO")
            if fullname is not None and len(fullname.split(" ")) == 2:
                print("Arrivato ai nomi")
                fname = fullname.split(" ")[0]
                lname = fullname.split(" ")[1]
            if SenderDao.getId(user) is None:
                print("Non esiste già")
                auth_code = get_random_string(8)
                SenderDao.insert(user,firstname = fname,lastname = lname,is_active = False,code = auth_code)
                print("Inserito nel db")
                public_key_path = Extraction.extractPublicKey(msg)
                if public_key_path is not None:
                    RegistrationHandler.registerKey(public_key_path)
                MailFunction.sendConfirmIdentity(user,auth_code)

    def confirmIdentity(user,code:str):
        code = code.replace("\n","")
        realcode = SenderDao.getAuthCode(user)
        print(realcode)
        print(code)
        if realcode == code:
            print("OOH LO STIAMO FACENDO SU "+user)
            SenderDao.setActive(user)


    def registerKey(public_key_path):
        gpg = gnupg.GPG(gnupghome = Config.get("pathtogpg"))
        with open(public_key_path,"r") as f:
            import_result = gpg.import_keys(f.read())
            if import_result.count == 1:
                print("chiave importata")
            f.close()
    '''

    def updateKey(msg):
        public_key_path = Extraction.extractPublicKey(msg)
        if public_key_path is not None:
            username = Extraction.extractSender(msg)
            gpg = gnupg.GPG(gnupghome = Config.get("pathtogpg"))
            keys = gpg.list_keys()
            for k in keys:
                uid = k.uids[0]
                owner_key = uid[uid.find("<")+1:uid.find(">")]
                gpg.delete_keys(k.fingerprint)
                with open(public_key_path,"r") as f:
                    import_result = gpg.import_keys(f.read())
                    if import_result.count == 1:
                        print("chiave importata")
                    f.close()

    '''

    def RegistrationAction(pattern,msg):
        if "Sign up" in pattern:
            RegistrationHandler.handleRegistration(pattern,msg)
        elif "confirm identity" in pattern:
            print("IS CONFIRM IDENTITY")
            username = Extraction.extractSender(msg)
            code = Extraction.extractBody(msg)
            RegistrationHandler.confirmIdentity(username,code)
        '''
        elif "update key" in pattern:
            username = Extraction.extractSender(msg)
            if realpassword == givenpassword:
                RegistrationHandler.updateKey(msg)
        '''
