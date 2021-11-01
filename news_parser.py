import email
import sys
from bs4 import BeautifulSoup
from email.parser import Parser
parser = Parser()
s = ""
for line in sys.stdin:
    s += line
email = parser.parsestr(s)
print(email.get('From')+'\n')
subject = email.get('Subject')
print(subject+'\n')
print(email.get('Date')+'\n')
print(subject[subject.find("[")+1:subject.find("]")]+'\n')
body = email.get_payload()
#vedo se il body è html
if BeautifulSoup(body, "html.parser").find():
    print("il body è html\n")
    soup = BeautifulSoup(body, "html.parser")
    headerhtml = soup.find('head')
    bodyhtml = soup.find('body')
    print('header:\n')
    print(headerhtml.decode_contents().replace("\n",""))
    print('\nbody:\n')
    print(bodyhtml.decode_contents().replace("\n",""))
else:
    print("il body non è html\n")
    print(body)
