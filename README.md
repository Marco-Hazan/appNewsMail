Aggiornamento 09/11/2021:

all'arrivo di una mail allo user newsmail viene mandato un input come standard input allo script news_parser.py.
Esso estrae sender della mail, subject e body.
Il subject deve essere nella forma [channel1,channel2,...]{dd/mm/YYYY} titolo news . Tra parentesi quadre sono contenuti i canali sui quali dovrà essere pubblicata la news, tra parentesi graffe la data di quando verrà pubblicata la news e fuori dalle parentesi il titolo della news.
Il body poi può essere passato come un html e in quel caso viene salvato anche il body html.

I dati vengono salvati in un database che può essere configurato all'interno di un file config.yaml. Per ora questa libreria è compatibile con postgresql e con mysql-server. 
