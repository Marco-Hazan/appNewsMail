import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions.config import Config
from Dao.SentDao import SentDao
from Dao.newsmailDao import newsmailDao


class MailFunction:

    def rapprArray(arr):
        s = ""
        for item in arr:
            s += str(item)+","
        return s[:-1]

    def sendConfirmationMail(newsmail, sender, channels, attachments, newchannels):
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
            'publisher': sender,
            'title': newsmail.title,
            'attachments': str(attachments),
            'recipients': str(channels),
            'expirydate': str(newsmail.expiration_date),
            'body': newsbody
        }
        with open(Config.get("master_path")+'/templates/messageConfirmation.txt', 'r') as f:
            src = Template(f.read())
            confirmationMessage = src.substitute(d)
        msg.attach(MIMEText(confirmationMessage, 'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendSubjectErrorMail(sender, subject):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = Config.get("newsmail")
        d = {
            'subject': subject
        }
        with open(Config.get("master_path")+'/templates/SubjectError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage, 'plain'))
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
        msg.attach(MIMEText(errorMessage, 'plain'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendChannelErrorMail(sender, channels):
        msg = MIMEMultipart()
        msg['Subject'] = 'Error on validation news'
        msg['From'] = Config.get("newsmail")
        d = {
            'channels': str(channels)
        }
        with open(Config.get("master_path")+'/templates/ChannelError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        msg.attach(MIMEText(errorMessage, 'plain'))
        s = smtplib.SMTP('localhost')
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendPublishedMail(newsmail, sender, newchannels, attachments, channelsNotPermitted):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news is published'
        msg['From'] = Config.get("newsmail")
        channels = SentDao.getPublishedChannels(newsmail.msgid)
        bodytoupdate = newsmailDao.getBody(newsmail.msgid).replace("\n", "%0A")
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
            'expirydate': newsmail.expiration_date,
            'body': newsbody,
            'bodytoupdate': bodytoupdate,
            'channelsnotpermitted': str(channelsNotPermitted)
        }
        with open(Config.get("master_path")+'/templates/publishedMessage.txt', 'r') as f:
            src = Template(f.read())
            publishedMessage = src.substitute(d)
        msg.attach(MIMEText(publishedMessage, 'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendDeletedMail(msgid, sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news has been deleted'
        msg['From'] = Config.get("newsmail")
        d = {
            'msgid': msgid
        }
        with open(Config.get("master_path")+'/templates/deletedMessage.txt', 'r') as f:
            src = Template(f.read())
            deletedMessage = src.substitute(d)
        msg.attach(MIMEText(deletedMessage, 'plain'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())
        s.quit()

    def sendUpdatedMail(news, attachments):
        msg = MIMEMultipart()
        msg['Subject'] = 'The news is updated'
        msg['From'] = Config.get("newsmail")
        publishedChannels = SentDao.getPublishedChannels(news.msgid)
        channels = []
        for c in publishedChannels:
            channels.append(c.name)
        bodytoupdate = newsmailDao.getBody(news.msgid).replace("\n", "%0A")
        d = {
            'msgid': news.msgid,
            'body': news.htmlbody,
            'channels': str(channels),
            'attachments': str(attachments),
            'bodytoupdate': bodytoupdate,
            'expirydate': news.expiration_date
        }
        with open(Config.get("master_path")+'/templates/updatedMessage.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage, 'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [news.sender], msg.as_string())
        s.quit()

    def sendCreatedChannel(channelname, sender):
        msg = MIMEMultipart()
        msg['Subject'] = 'The channel ' + channelname + ' has been created'
        msg['From'] = Config.get("newsmail")
        d = {
            'channel': channelname
        }
        with open(Config.get("master_path")+'/templates/newchannel.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage, 'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), [sender], msg.as_string())

    def sendRequestToPublish(channel, owner, newsmail, attachments):
        print(newsmail.msgid)
        msg = MIMEMultipart()
        msg['Subject'] = 'Request to publish on channel ' + channel.name
        print(msg['Subject'])
        msg['From'] = Config.get("newsmail")
        if not newsmail.is_html:
            newsbody = newsmail.body
        else:
            newsbody = newsmail.htmlbody
        d = {
            'title': newsmail.title,
            'channel': channel.name,
            'publisher': newsmail.sender,
            'body': newsbody,
            'attachments': str(attachments)
        }
        with open(Config.get("master_path")+'/templates/requestToPublish.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage, 'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        print(owner)
        s.sendmail(Config.get("newsmail"), [
                   owner], msg.as_string())
        s.quit()

    def sendListOfChannels(rcpt, channels):
        msg = MIMEMultipart()
        msg['Subject'] = 'List of your channels'
        msg['From'] = Config.get("newsmail")
        string_channels = ''
        for c in channels:
            if c.owner == rcpt:
                owner = 'YOU'
            else:
                owner = c.owner
            string_channels += '<tr><td>'+c.name+'</td><td>'+owner+'</td></tr>'
        d = {
            'channels': string_channels
        }
        with open(Config.get("master_path")+'/templates/listChannels.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        msg.attach(MIMEText(updatedMessage, 'html'))
        s = smtplib.SMTP(Config.get("smtp"))
        s.sendmail(Config.get("newsmail"), rcpt, msg.as_string())
        s.quit()
