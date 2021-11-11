import email
import sys
import re
import random
import base64
import os
import datetime
from datetime import timedelta
from datetime import datetime
from dateutil import parser
from functions.News import News
from newsmailDao import newsmailDao
from AttachmentDao import AttachmentDao
from ChannelDao import ChannelDao
from SenderDao import SenderDao
from bs4 import BeautifulSoup
from email.parser import Parser


#Funzione che controlla che i canali specificati via mail sono effettivamente esistenti e attivi
def checkchannels(channels):
    daochannel = ChannelDao()
    for c in channels:
        print("CANALE:\t"+c)
        if not daochannel.isActive(c):
            return False
    return True

#Funzione che controlla che il sender sia esistente e attivo
def checksender(sender):
    daosender = SenderDao()
    return daosender.isActive(sender)





parsermail = Parser()
dao_news = newsmailDao()


###
#Generazione id univoco per newsmail
unique = False
while not unique:
    msgid = random.randint(0,1000000)
    unique = dao_news.isUnique(msgid)
####


s = ""
###
#l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
for line in sys.stdin:
    s += line
email = parsermail.parsestr(s)
###


body = email.get_payload()



###
#estraggo sender
sender = email.get('From')
sender = sender[sender.find("<")+1:sender.find("@")]
###


#estraggo il subject della mail
tot_subject = email.get('Subject')
#estraggo data della mail
date = email.get('Date')
x = parser.parse(date)
creation_date = x.strftime("%Y-%m-%d %H:%M")
#il subject è valido se rispetta questa modalità: [channel1,channel2,...]{dd/mm/yyyy}subject
pattern = re.compile("\[[A-Za-z0-9, ]*\]\{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}.+")
if pattern.match(tot_subject):
    channels = tot_subject[tot_subject.find("[")+1:tot_subject.find("]")]
    channels = channels.split(",")
    expiration_date = tot_subject[tot_subject.find("{")+1:tot_subject.find("}")]
    expiration_date = datetime.strptime(expiration_date,'%d/%m/%Y')
    expiration_date = expiration_date.strftime("%Y-%m-%d %H:%M")
    pub_date = None
    subject = tot_subject[tot_subject.find("}")+1:]
#estraggo body
body = ""
bodyhtml = None
attachments = []
valid_channels = checkchannels(channels)
valid_sender = checksender(sender)
if valid_channels and valid_sender:
    if email.is_multipart():
        for part in email.walk():
            print(part.get_content_type())
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
            if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                body += part.get_payload().replace("\n","")
            #vedo se il body è html, nel caso estraggo body e header del documento html
            #se il documento non è html estraggo solo l'intero body della mail
            if part.get_content_type() == 'text/html':
                if BeautifulSoup(part.get_payload(), "html.parser").find():
                    soup = BeautifulSoup(part.get_payload(), "html.parser")
                    headerhtml = soup.find('head')
                    bodyhtml = soup.find('body')
                    bodyhtml = bodyhtml.decode_contents().replace("\n","")
    else:
        body += email.get_payload()
    newsmail = News(msgid,sender,subject,channels,body,bodyhtml,creation_date,pub_date,expiration_date)
    dao_news.insert(newsmail)
    dao_attachment = AttachmentDao()
    dao_attachment.insert(msgid,attachments)
else:
    print("ERRORE")
