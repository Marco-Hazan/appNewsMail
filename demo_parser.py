import markdown
import sys
from email.parser import Parser
parsermail = Parser()


#Perchè sia markdown
def is_markdown(text):
    return (any(x not in text for x in ('#'))
    and any(x not in text for x in ('1.', '-'))
    and any(x not in text for x in ('---', '>','*'))


###
#l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
s = ""
for line in sys.stdin:
    s += line.replace("\n","\r\n")

output = markdown.markdown(s)
print(output)
