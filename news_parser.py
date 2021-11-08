import email
import sys
import re
import random
import datetime
from datetime import timedelta
from datetime import datetime
from dateutil import parser
from functions.News import News
from newsmailDao import newsmailDao
from bs4 import BeautifulSoup
from email.parser import Parser
parsermail = Parser()
s = ""
#l'input arrivato da stdin lo salvo all'interno di una stringa
for line in sys.stdin:
    s += line
email = parsermail.parsestr(s)
#estraggo sender
sender = email.get('From')
sender = sender[sender.find("<")+1:sender.find("@")]
#estraggo subject
tot_subject = email.get('Subject')
#estraggo data della mail
date = email.get('Date')
x = parser.parse(date)
expiration_date = x + timedelta(days = 7)
creation_date = x.strftime("%Y-%m-%d %H:%M")
#il subject è valido se rispetta questa modalità: [channel1,channel2,...]{dd/mm/yyyy}subject
pattern = re.compile("\[[A-Za-z0-9, ]*\]\{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}.+")
if pattern.match(tot_subject):
    channels = tot_subject[tot_subject.find("[")+1:tot_subject.find("]")]
    pub_date = tot_subject[tot_subject.find("{")+1:tot_subject.find("}")]
    pub_date = datetime.strptime(pub_date,'%d/%m/%Y')
    pub_date = pub_date.strftime("%Y-%m-%d %H:%M")
    subject = tot_subject[tot_subject.find("}")+1:]
#estraggo body
body = email.get_payload()
#vedo se il body è html, nel caso estraggo body e header del documento html
if BeautifulSoup(body, "html.parser").find():
    soup = BeautifulSoup(body, "html.parser")
    headerhtml = soup.find('head')
    bodyhtml = soup.find('body')
    print(headerhtml.decode_contents().replace("\n",""))
    bodyhtml = bodyhtml.decode_contents().replace("\n","")
#se il documento non è html estraggo solo l'intero body della mail
else:
    bodyhtml = None
dao = newsmailDao()
unique = False
while not unique:
    msgid = random.randint(0,1000000)
    unique = dao.isUnique(msgid)
newsmail = News(msgid,sender,subject,channels.split(","),body,bodyhtml,creation_date,pub_date,expiration_date)
dao.insert(newsmail)
