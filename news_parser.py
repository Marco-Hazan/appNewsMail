import email
import sys
import re
from bs4 import BeautifulSoup
from email.parser import Parser
parser = Parser()
s = ""
#l'input arrivato da stdin lo salvo all'interno di una stringa
for line in sys.stdin:
    s += line
email = parser.parsestr(s)
#estraggo sender
print(email.get('From')+'\n')
#estraggo subject
subject = email.get('Subject')
print("Total Subject:"+subject+'\n')
#estraggo data della mail
print("Data email:"+email.get('Date')+'\n')
#il subject è valido se rispetta questa modalità: [channel1,channel2,...]{dd/mm/yyyy}subject
pattern = re.compile("\[[A-Za-z0-9, ]*\]\{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}.+")
if pattern.match(subject):
    print("Canali:"+subject[subject.find("[")+1:subject.find("]")]+'\n')
    print("Data dichiarata:"+subject[subject.find("{")+1:subject.find("}")]+'\n')
    print("Subject:"+subject[subject.find("}")+1:]+"\n")
#estraggo body
body = email.get_payload()
#vedo se il body è html, nel caso estraggo body e header del documento html
if BeautifulSoup(body, "html.parser").find():
    print("il body è html\n")
    soup = BeautifulSoup(body, "html.parser")
    headerhtml = soup.find('head')
    bodyhtml = soup.find('body')
    print('header:\n')
    print(headerhtml.decode_contents().replace("\n",""))
    print('\nbody:\n')
    print(bodyhtml.decode_contents().replace("\n",""))
#se il documeno non è html estraggo solo l'intero body della mail
else:
    print("il body non è html\n")
    print(body)
