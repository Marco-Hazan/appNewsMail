Setting server di postfix:
ogni user per ora è un user della macchina
mail non lette salvate in /var/mail/nomeutente
mail lette salvate in /home/nomeutente/mbox

Main.cf:
aliases: /etc/aliases
myhostname: uniServer.it  (Usando Thunderbird veniva richiesto)

Contenuto di /etc/aliases: newsmail: "|python3 /home/appNewsMail/master/news_parser.py > /home/appNewsMail/master/demofile.txt"

L'intera app è momentaneamente salvata nella home.

News_parser:
estrae sender,subject e body della mail
sender è nella forma <username@domain> perciò viene estratto solo username
subject deve essere nella forma [channel1,channel2,...]{dd/mm/YYYY}titolo_news
Vengono quindi estratti i canali e salvati dentro un array, salvata la data di scadenza come timestamp e salvato il titolo della news.
Se il sender e i channel sono validi viene generato un msgid e parsato il body della mail:
il body può essere multipart oppure no. Se non è multipart l'unica parte sarà di tipo (content-type) text/plain, se invece è multipart potrebbe esserci html oppure altri tipi di contenuti che saranno allegati.
Se c'è solo una parte estraggo semplicemente l'intero body. Se c'è sia text/plain che text/html allora estraggo sia l'intero body che il body dell'html. Se ci sono altri tipi di contenuti, se hanno un filename, li estraggo come allegati decodificando da base64 e scrivo un file con il contenuto di quei bytes.
Una volta estratto tutto salvo tutte le varie parti estratte e il msgid in un ogggetto News che passerò a un data access object che si collega con il database e salva la news nel database.


Gestione allegati:
I file estratti vengono salvati in /home/appNewsMail/attachments/msgid, dove msgid è l'id della mail dove sono stati estratti.


Gestione database:
- diagramma er
In un file di configurazione .yaml ho salvato le informazioni per collegarsi a un database.
I database per ora supportati sono mysql e postgresql (già testati)
In un file python actionsdb.py vengono gestite le varie connessioni leggendo le informazioni necessarie dal file di configurazione.
Da una funzione di connessione viene quindi ritornato un oggetto connection (mysql o postgresql). Per quanto gli oggetti ritornati da postgresql o mysql sono diversi i metodi per accedere alla base di dati sono identici perciò i vari dao che accedono al database possono operare senza sapere su quale specifico dbms.


Moduli python utilizzati:
Parser da email.parser -> modulo per parsare le mail e ritornare un oggetto email
email -> modulo per gestire contenuto della mail
BeatifulSoup da bs4 -> modulo per parsare file html (usato per estrarre body)
re -> modulo usato per vedere se una stringa matcha con una particolare espressione regolare (nel subject)
random -> generazione msgid
base64 -> decodifica file allegati
datetime -> generazione timestamp
psycopg e mysql.connector -> moduli per la connessione rispettivamente a dbms postgres e mysql
yaml -> per leggere i file di configurazione .yaml
