import email
import sys
import re
import shutil
import random
import secrets
import hashlib
import base64
import os
import time
import datetime
from Publication import ChannelHandler
from os import path
from functions.verify_signature import PyCrypto
from functions.mailfunctions import MailFunction
from datetime import timedelta
from datetime import datetime
from dateutil import parser
from functions.News import News
from newsmailDao import newsmailDao
from AttachmentDao import AttachmentDao
from ChannelDao import ChannelDao
from CanSendOnDao import CanSendOnDao
from SenderDao import SenderDao
from bs4 import BeautifulSoup
from Objects.SendOn import SendOn
from email.parser import Parser


#Funzione che controlla che i canali specificati via mail sono effettivamente esistenti e attivi
def checkchannels(channels):
    for c in channels:
        if not ChannelDao.isActive(c):
            return False
    return True

#Funzione che controlla che il sender sia esistente e attivo
def checksender(sender):
    return SenderDao.isActive(sender)

def extractBody(email):
    body = ""
    if email.is_multipart():
        for part in email.walk():
            if part.get_content_type() == 'text/plain':
                body += part.get_payload().replace("\n","")
    else:
        if email.get_content_type() == 'text/plain':
            body = email.get_payload()
    return body

def find_pubkey_loc():
    for filename in os.listdir("/home/marco/appNewsMail/attachments/"+msgid):
        if ".asc" in filename:
            return "/home/marco/appNewsMail/attachments/"+msgid+"/"+filename
    return None


def extractHtml(email):
    bodyhtml = None
    if email.is_multipart():
        for part in email.walk():
            if part.get_content_type() == 'text/html':
                #if BeautifulSoup(part.get_payload(), "html.parser").find():
                    #soup = BeautifulSoup(part.get_payload(), "html.parser")
                    #headerhtml = soup.find('head')
                    #bodyhtml = soup.find('body')
                    #bodyhtml = bodyhtml.decode_contents().replace("\n","")
                bodyhtml = part.get_payload()
    else:
        if email.get_content_type() == 'text/html':
            #if BeautifulSoup(part.get_payload(), "html.parser").find():
                #soup = BeautifulSoup(part.get_payload(), "html.parser")
                #headerhtml = soup.find('head')
                #bodyhtml = soup.find('body')
                #bodyhtml = bodyhtml.decode_contents().replace("\n","")
            bodyhtml = email.get_payload()
    return bodyhtml

def extractAttachments(email,msgid):
    attachments = []
    if email.is_multipart():
        for part in email.walk():
            if part.get_content_type() != 'text/plain' and part.get_content_type() != 'multipart/mixed' and part.get_content_type != 'text/html' and part.get_content_type() != 'multipart/alternative':
                try:
                    os.mkdir("/home/marco/appNewsMail/attachments/"+str(msgid))
                except OSError:
                    pass
                if part.get_filename() is not None:
                    '''
                    filename = part.get_filename()
                    if filename == "OpenPGP_signature":
                        global signature_flag
                        signature_flag = True
                        signature = str(part.get_payload())
                    elif ".asc" in filename:
                        with open("/home/marco/appNewsMail/attachments/"+str(msgid)+"/"+filename, 'a') as f:
                            try:
                                f.write(str(part.get_payload()))
                            except ValueError:
                                pass
                    else:
                    '''
                    attachments.append(filename)
                    with open("/home/marco/appNewsMail/attachments/"+str(msgid)+"/"+filename, 'ab') as f:
                        try:
                            message_bytes = base64.b64decode(str(part.get_payload()))
                            f.write(message_bytes)
                        except ValueError:
                            pass
    return attachments





def checkPermissionOnChannel(sender,channels):
    id_sender = SenderDao.getId(sender)
    for ch in channels:
        if not CanSendOnDao.check(id_sender,ch):
            return False
    return True



parsermail = Parser()
dao_news = newsmailDao()
signature_flag = False
signature = None

###
#Generazione id univoco per newsmail
unique = False
while not unique:
    token = secrets.token_bytes(16)
    milli_sec = int(round(time.time() * 1000))
    msgid = (str(token) + str(milli_sec)).encode("utf-8")
    msgid = hashlib.sha256(msgid).hexdigest()
    unique = dao_news.isUnique(msgid)
####


s = ""
###
#l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
for line in sys.stdin:
    s += line
data = s
email = parsermail.parsestr(s)
###

###
#estraggo sender
tot_sender = email.get('From')
cc = email.get('Cc')

sender = tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]

#estraggo data della mail
date = email.get('Date')
x = parser.parse(date)
creation_date = x.strftime("%Y-%m-%d %H:%M")
###

valid_sender = checksender(sender)
if not valid_sender:
    MailFunction.sendSenderErrorMail(sender)
    exit()

#estraggo il subject della mail
subject = email.get('Subject')
if "confirm news" in subject and len(subject.split(" ")) == 3:
    receivedMsgid = subject.split(" ")[2]
    status = newsmailDao.getStatus(receivedMsgid)
    if status is 1 and newsmailDao.getSender(receivedMsgid) == sender:
        newsmailDao.updateStatus(receivedMsgid,2)
        MailFunction.sendPublishedMail(receivedMsgid,sender)
        exit()
    else:
        exit()


if "delete news" in subject and len(subject.split(" ")) == 3:
    receivedMsgid = subject.split(" ")[2]
    status = newsmailDao.getStatus(receivedMsgid)
    if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
        newsmailDao.deleteNews(receivedMsgid)
        pathAttachments = "/home/marco/appNewsMail/attachments/"+receivedMsgid
        if path.exists(pathAttachments):
            shutil.rmtree(pathAttachments)
        MailFunction.sendDeletedMail(receivedMsgid,sender)
        exit()
    else:
        exit()


if "update news" in subject and len(subject.split(" ")) == 3:
    receivedMsgid = subject.split(" ")[2]
    status = newsmailDao.getStatus(receivedMsgid)
    if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
        pathAttachments = "/home/marco/appNewsMail/attachments/"+receivedMsgid
        if path.exists(pathAttachments):
            shutil.rmtree(pathAttachments)
        body = extractBody(email)
        htmlbody = extractHtmlBody(email)
        newsmailDao.updateBody(receivedMsgid,body,htmlbody)
        attachments = extractAttachments(email,receivedMsgid)
        MailFunction.sendUpdatedMail(receivedMsgid,sender,body,htmlbody,attachments)
        exit()
    else:
        exit()

#il subject è valido se rispetta questa modalità: [channel1,channel2,...]{dd/mm/yyyy}subject
pattern = re.compile("\[[A-Za-z0-9, ]*\]\{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}.+")
if pattern.match(subject):
    channels = subject[subject.find("[")+1:subject.find("]")]
    channels = channels.split(",")
    channels = ChannelHandler.extractChannels(channels)
    expiration_date = subject[subject.find("{")+1:subject.find("}")]
    expiration_date = datetime.strptime(expiration_date,'%d/%m/%Y')
    expiration_date = expiration_date.strftime("%Y-%m-%d %H:%M")
    pub_date = None
    title = subject[subject.find("}")+1:]
else:
    MailFunction.sendSubjectErrorMail(tot_sender,subject)
    exit()
'''
legit_channels = ChannelHandler.extractLegitChannels(channels)
notlegit_channels = ChannelHandler.extractNotPermittedChannels(sender,channels)
new_channels = ChannelHandler.extractNewChannels(channels)
'''

for c in new_channels:
    ChannelHandler.createChannel(c,sender)
    MailFunction.sendCreatedChannel()


#estraggo body
body = extractBody(email)
bodyhtml = extractHtml(email)
if bodyhtml is not None:
    body = None
attachments = extractAttachments(email,msgid)
newsmail = News(msgid,sender,title,body,bodyhtml,creation_date,expiration_date)
dao_news.insert(newsmail)
for c in channels:
    sendon = SendOn(newsmail,c)
    action = sendon.defineAction()
    action.act()
MailFunction.sendConfirmationMail(newsmail,sender)

'''
if signature_flag == True:
    public_key_loc = find_pubkey_loc()
    public_key = str(email.get('Autocrypt')).split("keydata=")[1]
    valid_signature = PyCrypto.verify_sign(public_key,signature,data)
    if valid_signature:
        pass
        #print("FIRMA VALIDATA OH CAZZO")
'''
