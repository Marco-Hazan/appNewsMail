import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailFunction:

    def sendConfirmationMail(newsmail,sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'confirm news ' + newsmail.msgid
        msg['From'] = "newsmail@islab.di.unimi.it"
        if newsmail.is_html():
            newsbody = newsmail.htmlbody
        else:
            newsbody = newsmail.body
        msg['To'] = sender
        d = {
            'msgid': newsmail.msgid,
            'publisher' : sender,
            'title' : newsmail.title,
            'recipients': ' '.join(newsmail.channels),
            'attachments': ' '.join(newsmail.attachments),
            'expirydate': str(newsmail.expiration_date),
            'body': newsbody
        }
        with open('/home/marco/appNewsMail/master/functions/messageConfirmation.txt', 'r') as f:
            src = Template(f.read())
            confirmationMessage = src.substitute(d)
        msg.attach(MIMEText(confirmationMessage,'html'))
        s = smtplib.SMTP('localhost')
        s.sendmail("newsmail@islab.di.unimi.it", [sender], msg.as_string())
        s.quit()

    def sendSubjectErrorMail(sender,subject):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = "newsmail@islab.di.unimi.it"
        d = {
            'subject': subject
        }
        with open('/home/marco/appNewsMail/master/functions/SubjectError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage,'plain'))
        s = smtplib.SMTP('localhost')
        s.sendmail("newsmail@islab.di.unimi.it", [sender], msg.as_string())
        s.quit()

    def sendSenderErrorMail(sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = "newsmail@islab.di.unimi.it"
        d = {
            'sender': sender
        }
        with open('/home/marco/appNewsMail/master/functions/SenderError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage,'plain'))
        s = smtplib.SMTP('localhost')
        s.sendmail("newsmail@islab.di.unimi.it", [sender], msg.as_string())
        s.quit()

    def sendChannelErrorMail(sender,channels):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = "newsmail@islab.di.unimi.it"
        d = {
            'channels': str(channels)
        }
        with open('/home/marco/appNewsMail/master/functions/ChannelError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage,'plain'))
        s = smtplib.SMTP('localhost')
        s.sendmail("newsmail@islab.di.unimi.it", [sender], msg.as_string())
        s.quit()

    def sendPublishedMail(msgid,sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news is published'
        msg['From'] = "newsmail@islab.di.unimi.it"
        d = {
            'msgid': msgid
        }
        with open('/home/marco/appNewsMail/master/functions/publishedMessage.txt', 'r') as f:
            src = Template(f.read())
            publishedMessage = src.substitute(d)
        msg.attach(MIMEText(publishedMessage,'html'))
        s = smtplib.SMTP('localhost')
        s.sendmail("newsmail@islab.di.unimi.it", [sender], msg.as_string())
        s.quit()

    def sendDeletedMail(msgid,sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news has been deleted'
        msg['From'] = "newsmail@islab.di.unimi.it"
        d = {
            'msgid': msgid
        }
        with open('/home/marco/appNewsMail/master/functions/deletedMessage.txt', 'r') as f:
            src = Template(f.read())
            deletedMessage = src.substitute(d)
        msg.attach(MIMEText(deletedMessage,'plain'))
        s = smtplib.SMTP('localhost')
        s.sendmail("newsmail@islab.di.unimi.it", [sender], msg.as_string())
        s.quit()
