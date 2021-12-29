import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message  import EmailMessage
from functions.config import Config
from Dao.SentDao import SentDao


class MailFunction:

    def rapprArray(arr):
        s = ""
        for item in arr:
            s += str(item)+","
        return s[:-1]

    def sendConfirmationMail(newsmail,sender,channels,attachments,newchannels):
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
            'recipients': str(channels),
            'newchannels': MailFunction.rapprArray(newchannels),
            'attachments': MailFunction.rapprArray(attachments),
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


    def sendPublishedMail(newsmail,sender,newchannels,attachments,channelsNotPermitted):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news is published'
        msg['From'] = Config.get("newsmail")
        channels = SentDao.getPublishedChannels(newsmail.msgid)
        channelstext = ""
        for c in channels:
            channelstext += c.name + ","
        if newsmail.is_html():
            newsbody = newsmail.htmlbody
        else:
            newsbody = newsmail.body
        d = {
            'msgid': newsmail.msgid,
            'channels': channelstext,
            'newchannels': str(newchannels),
            'attachments': attachments,
            'expirydate' : newsmail.expiration_date,
            'body': newsbody,
            'channelsnotpermitted': str(channelsNotPermitted)
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

    def sendRequestToPublish(channel,owner,newsmail,attachments):
        print(newsmail.msgid)
        msg = MIMEMultipart()
        msg['Subject'] = 'Request to publish on channel '+ channel.name
        print(msg['Subject'])
        msg['From'] = Config.get("newsmail")
        if not newsmail.is_html:
            newsbody = newsmail.body
        else:
            newsbody = newsmail.htmlbody
        d = {
            'channel': channel.name,
            'msgid': newsmail.msgid,
            'publisher': newsmail.sender,
            'body': newsbody,
            'attachments': str(attachments)
        }
        with open(Config.get("master_path")+'/templates/requestToPublish.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage,'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        print(owner)
        s.sendmail(Config.get("newsmail"),['marco@islab.di.unimi.it'], msg.as_string())
        s.quit()
