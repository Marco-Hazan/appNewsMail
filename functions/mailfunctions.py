import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions.config import Config
from Dao.SentDao import SentDao
from Dao.newsmailDao import newsmailDao
import functions.mailutils as mailutils

class MailFunction:

    def rapprArray(arr):
        s = ""
        for item in arr:
            s += str(item)+","
        return s[:-1]

    def sendConfirmationMail(newsmail, rcpt, channels, attachments, newchannels):
        d = {
            'msgid': newsmail.msgid,
            'publisher': rcpt,
            'title': newsmail.title,
            'attachments': str(attachments),
            'recipients': str(channels),
            'expirydate': str(newsmail.expiration_date),
            'newsmail' : Config.get("newsmail"),
            'body': newsmail.htmlbody
        }
        with open(Config.get("master_path")+'/templates/messageConfirmation.txt', 'r') as f:
            src = Template(f.read())
            confirmationMessage = src.substitute(d)
        mailutils.sendMail(rcpt,confirmationMessage,'confirm news ' + newsmail.msgid)

    def sendSubjectErrorMail(rcpt, subject):
        d = {
            'subject': subject
        }
        with open(Config.get("master_path")+'/templates/SubjectError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        mailutils.sendMail(rcpt,errorMessage,'Error on validation news')

    def sendSenderErrorMail(rcpt):
        d = {
            'sender': rcpt
        }
        with open(Config.get("master_path")+'/templates/SenderError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        mailutils.sendMail(rcpt,errorMessage,'Error on validation news')

    def sendChannelErrorMail(rcpt, channels):
        d = {
            'channels': str(channels)
        }
        with open(Config.get("master_path")+'/templates/ChannelError.txt', 'r') as f:
            src = Template(f.read())
            errorMessage = src.substitute(d)
        mailutils.sendMail(rcpt,errorMessage,'Error on validation news')

    def sendPublishedMail(newsmail, rcpt, newchannels, attachments, channelsNotPermitted):
        channels = SentDao.getPublishedChannels(newsmail.msgid)
        channelstext = ""
        for c in channels:
            channelstext += c.name + ","
        if newsmail.is_html():
            bodytoupdate = ''
        else:
            bodytoupdate = newsmail.body
        bodytoupdate = bodytoupdate.replace("\n", "%0A")
        if len(channelsNotPermitted) > 0:
            d2 = {
                'channelsnotpermitted': str(channelsNotPermitted)
            }
            with open(Config.get("master_path")+'/templates/channelnotpermitted.txt', 'r') as f2:
                src2 = Template(f2.read())
                message_channelsnotpermitted = src2.substitute(d2)
        else:
            message_channelsnotpermitted = ''
        d = {
            'msgid': newsmail.msgid,
            'title': newsmail.title,
            'expiration_date': newsmail.expiration_date,
            'channels': channelstext,
            'newchannels': str(newchannels),
            'attachments': attachments,
            'expirydate': newsmail.expiration_date,
            'body': newsmail.htmlbody,
            'bodytoupdate': bodytoupdate,
            'channelsnotpermitted': message_channelsnotpermitted,
            'newsmail' : Config.get("newsmail")
        }
        with open(Config.get("master_path")+'/templates/publishedMessage.txt', 'r') as f:
            src = Template(f.read())
            publishedMessage = src.substitute(d)
        mailutils.sendMail(rcpt,publishedMessage,'The news is published')

    def sendDeletedMail(msgid, rcpt):
        d = {
            'msgid': msgid
        }
        with open(Config.get("master_path")+'/templates/deletedMessage.txt', 'r') as f:
            src = Template(f.read())
            deletedMessage = src.substitute(d)
        mailutils.sendMail(rcpt,deletedMessage,'The news has been deleted')

    def sendUpdatedMail(news, attachments):
        publishedChannels = SentDao.getPublishedChannels(news.msgid)
        channels = []
        for c in publishedChannels:
            channels.append(c.name)
        if news.is_html():
            bodytoupdate = ''
        else:
            bodytoupdate = news.body
        bodytoupdate = bodytoupdate.replace("\n", "%0A")
        d = {
            'msgid': news.msgid,
            'body': news.htmlbody,
            'channels': str(channels),
            'attachments': str(attachments),
            'bodytoupdate': bodytoupdate,
            'newsmail' : Config.get("newsmail"),
            'expirydate': news.expiration_date
        }
        with open(Config.get("master_path")+'/templates/updatedMessage.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        mailutils.sendMail(news.sender,updatedMessage,'The news is updated')

    def sendCreatedChannel(channelname, rcpt):
        d = {
            'newsmail' : Config.get("newsmail"),
            'channel': channelname
        }
        with open(Config.get("master_path")+'/templates/newchannel.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        mailutils.sendMail(rcpt,updatedMessage,'The channel ' + channelname + ' has been created')

    def sendRequestToPublish(channel, owner, newsmail, attachments):
        d = {
            'title': newsmail.title,
            'first32_msgid': newsmail.msgid[0:32],
            'channel': channel.name,
            'publisher': newsmail.sender,
            'body': newsmail.htmlbody,
            'newsmail' : Config.get("newsmail"),
            'attachments': str(attachments)
        }
        with open(Config.get("master_path")+'/templates/requestToPublish.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        mailutils.sendMail(owner,updatedMessage,'Request to publish on channel ' + channel.name)

    def sendListOfChannels(rcpt, channels):
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
        mailutils.sendMail(rcpt,updatedMessage,'List of your channels')

    def sendConfirmIdentity(rcpt,password):
        d = {
            'pwd': password,
            'newsmail': Config.get("newsmail")
        }
        with open(Config.get("master_path")+'/templates/confirmIdentity.txt', 'r') as f:
            src = Template(f.read())
            updatedMessage = src.substitute(d)
        mailutils.sendMail(rcpt,updatedMessage,'Request to confirm identity')
