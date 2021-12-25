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
from functions.mailfunctions import MailFunction
from datetime import timedelta
from datetime import datetime
from dateutil import parser
from Objects.News import News
from Dao.newsmailDao import newsmailDao
from Dao.ChannelDao import ChannelDao
from Dao.CanSendOnDao import CanSendOnDao
from Dao.SenderDao import SenderDao
from Dao.SentDao import SentDao
from bs4 import BeautifulSoup
from Objects.SendOn import SendOn
from email.parser import Parser
from Signature.CheckSig import CheckSig


#Funzione che controlla che i canali specificati via mail sono effettivamente esistenti e attivi
'''
def checkchannels(channels):
    for c in channels:
        if not ChannelDao.isActive(c):
            return False
    return True
'''

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
                    filename = part.get_filename()
                    attachments.append(filename)
                    with open("/home/marco/appNewsMail/attachments/"+str(msgid)+"/"+filename, 'ab') as f:
                        try:
                            message_bytes = base64.b64decode(str(part.get_payload()))
                            f.write(message_bytes)
                        except ValueError:
                            pass
    return attachments




'''
def checkPermissionOnChannel(sender,channels):
    id_sender = SenderDao.getId(sender)
    for ch in channels:
        if not CanSendOnDao.check(id_sender,ch):
            return False
    return True
'''


parsermail = Parser()

###
#Generazione id univoco per newsmail
unique = False
while not unique:
    token = secrets.token_bytes(16)
    milli_sec = int(round(time.time() * 1000))
    msgid = (str(token) + str(milli_sec)).encode("utf-8")
    msgid = hashlib.sha256(msgid).hexdigest()
    unique = newsmailDao.isUnique(msgid)
####


s = ""
###
#l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
for line in sys.stdin:
    s += line.replace("\n","\r\n")
data = s



email = parsermail.parsestr(s)
###

###
#estraggo sender
tot_sender = email.get('From')
cc = email.get('Cc')

sender = tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]

firmata = CheckSig.verifySignature(data,sender)

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
        newsmail = newsmailDao.get(receivedMsgid)
        bodyconfirm = extractBody(email)
        split_confirm = bodyconfirm.split("\r\n")
        new_channels = split_confirm[1][split_confirm[1].find(":")+ 1:].split(",")
        for c in new_channels:
            ChannelDao.insert(c,sender)
            CanSendOnDao.insert(sender,c);
        attachments = split_confirm[2][split_confirm[2].find(":")+ 1:].split(",")
        MailFunction.sendPublishedMail(newsmail,sender,new_channels,attachments)
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
pattern = re.compile("\[[A-Za-z0-9_, ]*\]\{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}.+")
if pattern.match(subject):
    channelnames = subject[subject.find("[")+1:subject.find("]")]
    channelnames = channelnames.split(",")
    channels = ChannelHandler.extractChannels(sender,channelnames)
    expiration_date = subject[subject.find("{")+1:subject.find("}")]
    expiration_date = datetime.strptime(expiration_date,'%d/%m/%Y')
    expiration_date = expiration_date.strftime("%Y-%m-%d %H:%M")
    title = subject[subject.find("}")+1:]
else:
    MailFunction.sendSubjectErrorMail(tot_sender,subject)
    exit()

#estraggo body
body = extractBody(email)
bodyhtml = extractHtml(email)
if bodyhtml is not None:
    body = None
attachments = extractAttachments(email,msgid)
newsmail = News(msgid,sender,title,body,bodyhtml,creation_date,expiration_date)
if firmata:
    newsmailDao.insert(newsmail,True)
else:
    newsmailDao.insert(newsmail,False)


new_channels = []
channelsnotpermitted = []

for c in channels:
    if c.isnew:
        new_channels.append(c.name)
        if firmata:
            ChannelDao.insert(c.name,c.owner)
            CanSendOnDao.insert(sender,c.name);
            SentDao.insert(msgid,c.name,True)
    elif ChannelHandler.isLegit(c.name,sender):
        SentDao.insert(msgid,c.name,True)
    elif not CanSendOnDao.check(user,c):
        channelsnotpermitted.append(c.name)
        SentDao.insert(msgid,c.name,False)
        MailFunction.sendRequestToPublish(self.channel,self.channel.owner,self.newsmail)


if firmata:
    MailFunction.sendPublishedMail(newsmail,sender,new_channels,channelsnotpermitted)
else:
    MailFunction.sendConfirmationMail(newsmail,sender,channelnames,attachments,new_channels)
