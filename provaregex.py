import re
string = "[ciao,bella]{11/08/2018}ok";
pattern = re.compile("\[[A-Za-z0-9, ]*\]\{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}.+")
if pattern.match(string):
    print("true")
else:
    print("false")
