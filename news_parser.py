import email
import markdown
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
from Handlers.Publication import ChannelHandler
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
from Handlers.NewsHandler import NewsHandler
from functions.extract import Extraction
from Handlers.RegistrationHandler import RegistrationHandler
from functions.config import Config

#Funzione che controlla che il sender sia esistente e attivo


def checksender(sender):
    return SenderDao.isActive(sender)

###
#Generazione id univoco per newsmail

####


def generaId():
    unique = False
    msgid = None
    while not unique:
        token = secrets.token_bytes(16)
        milli_sec = int(round(time.time() * 1000))
        msgid = (str(token) + str(milli_sec)).encode("utf-8")
        msgid = hashlib.sha256(msgid).hexdigest()
        unique = newsmailDao.isUnique(msgid)
    return msgid


###
#l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
s = ""
for line in sys.stdin:
    s += line.replace("\n", "\r\n")
data = s
print(data)
parsermail = Parser()
msg = parsermail.parsestr(data)
###

###
# estraggo sender
sender = Extraction.extractSender(msg)
valid_sender = checksender(sender)
if not Config.get("publicaccess") and not valid_sender:
    MailFunction.sendSenderErrorMail(sender)
    exit()
firmata = CheckSig.verifySignature(data, sender)
cc = msg.get('Cc')
# estraggo data della mail
date = msg.get('Date')
creation_date = parser.parse(date)
#creation_date = creation_date.strftime("%Y-%m-%d %H:%M")
###
# estraggo il subject della mail
subject = msg.get('Subject')

if RegistrationHandler.isRegistrationPattern(subject):
    RegistrationHandler.RegistrationAction(subject,msg)
    exit()

if ChannelHandler.IsChannelRelatedPattern(subject) and firmata:
    ChannelHandler.ChannelAction(subject, msg)
    exit()

if NewsHandler.isNewsRelated(subject):
    NewsHandler.newsAction(msg, subject)
    exit()
# il subject è valido se rispetta questa modalità: [channel1,channel2,...]{dd/mm/yyyy}subject
valid_pattern1 = "\[[A-Za-z0-9_, ]*\]\{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}.+"
valid_pattern2 = "\[[A-Za-z0-9_, ]*\].+"

pattern1 = re.compile(valid_pattern1)
pattern2 = re.compile(valid_pattern2)
if pattern1.match(subject) or pattern2.match(subject):
    msgid = generaId()
    channelnames = subject[subject.find("[")+1:subject.find("]")]
    channelnames = channelnames.split(",")
    channels = ChannelHandler.extractChannels(sender, channelnames)
    if pattern1.match(subject):
        expiration_date = subject[subject.find("{")+1:subject.find("}")]
        expiration_date = datetime.strptime(expiration_date, '%d/%m/%Y')
        #expiration_date = expiration_date.strftime("%Y-%m-%d %H:%M")
        title = subject[subject.find("}")+1:]
    else:
        expiration_date = None
        title = subject[subject.find("]")+1:]
else:
    MailFunction.sendSubjectErrorMail(sender, subject)
    exit()

# straggo body
# body = Extraction.extractBody(msg)
body = None
bodyhtml = Extraction.extractHtml(msg)
if bodyhtml is None:
    body = Extraction.extractBody(msg)
    bodyhtml = markdown.markdown(body)
attachments = Extraction.extractAttachments(msg, msgid)
newsmail = News(msgid, sender, title, body, bodyhtml,
                creation_date, expiration_date)
if firmata:
    newsmailDao.insert(newsmail, True)
else:
    newsmailDao.insert(newsmail, False)


new_channels = []
channelsnotpermitted = []


for c in channels:
    if c.isnew:
        if Config.get("createchannelonnews"):
            new_channels.append(c.name)
            ChannelDao.insert(c)
            CanSendOnDao.insert(c.owner,c.name)
            SentDao.insert(msgid, c.name, True)
            if not firmata:
                ChannelDao.disable(c.name)
    elif ChannelHandler.isLegit(c.name, sender):
        SentDao.insert(msgid, c.name, True)
    elif not CanSendOnDao.check(sender, c.name):
        channelsnotpermitted.append(c.name)
        SentDao.insert(msgid, c.name, False)
        MailFunction.sendRequestToPublish(c, c.owner, newsmail, attachments)
    elif (
            (not c.is_active ) and
            (c.owner == sender) and
            Config.get("enablechannel_on_ownernews")
        ):
            if firmata:
                ChannelDao.enable(c.name)
                SentDao.insert(msgid,c.name,True)
            else:
                SentDao.insert(msgid,c.name,False)




if firmata:
    MailFunction.sendPublishedMail(
        newsmail, sender, new_channels, attachments, channelsnotpermitted)
else:
    MailFunction.sendConfirmationMail(
        newsmail, sender, channelnames, attachments, new_channels)
