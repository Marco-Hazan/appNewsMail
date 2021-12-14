s = ""
###
#l'input arrivato da stdin lo salvo all'interno di una stringa che quindi passo al parser di email
for line in sys.stdin:
    s += line

print(s)
