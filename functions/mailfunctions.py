import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions.config import Config

class MailFunction:

    def sendConfirmationMail(newsmail,sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'confirm news ' + newsmail.msgid
        msg['From'] = Config.get("newsmail")
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
        with open(Config.get("master_path")+'/templates/messageConfirmation.txt', 'r') as f:
            src = Template(f.read())
            confirmationMessage = src.substitute(d)
        msg.attach(MIMEText(confirmationMessage,'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendSubjectErrorMail(sender,subject):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = Config.get("newsmail")
        d = {
            'subject': subject
        }
        with open(Config.get("master_path")+'/templates/SubjectError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage,'plain'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendSenderErrorMail(sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = Config.get("newsmail")
        d = {
            'sender': sender
        }
        with open(Config.get("master_path")+'/templates/SenderError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage,'plain'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendChannelErrorMail(sender,channels):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = Config.get("newsmail")
        d = {
            'channels': str(channels)
        }
        with open(Config.get("master_path")+'/templates/ChannelError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage,'plain'))
        s = smtplib.SMTP('localhost')
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendPublishedMail(msgid,sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news is published'
        msg['From'] = Config.get("newsmail")
        d = {
            'msgid': msgid
        }
        with open(Config.get("master_path")+'/templates/publishedMessage.txt', 'r') as f:
            src = Template(f.read())
            publishedMessage = src.substitute(d)
        msg.attach(MIMEText(publishedMessage,'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendDeletedMail(msgid,sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news has been deleted'
        msg['From'] = Config.get("newsmail")
        d = {
            'msgid': msgid
        }
        with open(Config.get("master_path")+'/templates/deletedMessage.txt', 'r') as f:
            src = Template(f.read())
            deletedMessage = src.substitute(d)
        msg.attach(MIMEText(deletedMessage,'plain'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendUpdatedMail(msgid,sender,body,htmlbody,attachments):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news is updated'
        msg['From'] = Config.get("newsmail")
        if htmlbody is None:
            newsbody = body
        else:
            newsbody = htmlbody
        d = {
            'msgid': msgid,
            'body': newsbody,
            'attachments': str(attachments)
        }
        with open(Config.get("master_path")+'/templates/updatedMessage.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage,'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendCreatedChannel(channelname,sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'The channel ' + channelname + ' has been created'
        msg['From'] = Config.get("newsmail")
        d = {
            'channel' : channelname
        }
        with open(Config.get("master_path")+'/templates/newchannel.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage,'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())

    def sendRequestToPublish(channel,sender,newsmail):
        msg = MIMEMultipart()
        msg['Subject'] = 'Request to publish on channel '+ channel.name
        msg['From'] = Config.get("newsmail")
        if not newsmail.is_html:
            newsbody = newsmail.body
        else:
            newsbody = newsmail.htmlbody
        d = {
            'channel': channel,
            'msgid': msgid,
            'publisher': newsmail.sender,
            'body': newsbody,
            'attachments': str(attachments)
        }
        with open(Config.get("master_path")+'/templates/requestToPublish.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage,'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()
