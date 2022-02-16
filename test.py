from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import Message
import smtplib
import gnupg
import time
import unittest
from functions.config import Config
from Dao.newsmailDao import newsmailDao
from Dao.SentDao import SentDao
from Dao.ChannelDao import ChannelDao

tester = "marco.hazan@studenti.unimi.it"

def sendMailSigned(subject,body,type):
    basemsg = MIMEMultipart()
    basemsg.attach(MIMEText(body,type))
    gpg = gnupg.GPG(gnupghome = Config.get("pathtogpg"))
    basetext = basemsg.as_string().replace('\n', '\r\n')
    signature = str(gpg.sign(basetext, detach=True))
    signmsg = TestNews.messageFromSignature(signature)
    msg = MIMEMultipart(_subtype="signed", micalg="pgp-sha1",
    protocol="application/pgp-signature")
    msg['Subject'] = subject
    msg['From'] = tester + "t"
    msg.attach(basemsg)
    msg.attach(signmsg)
    s = smtplib.SMTP("localhost")
    s.sendmail(tester+"t",["newsmail@islab.di.unimi.it"], msg.as_string())
    s.quit()

def sendMail(subject,body,type):
    basemsg = MIMEMultipart()
    basemsg.attach(MIMEText(body,type))
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = tester + "t"
    msg.attach(basemsg)
    s = smtplib.SMTP("localhost")
    s.sendmail(tester + "t",["newsmail@islab.di.unimi.it"], msg.as_string())
    s.quit()


class TestNews(unittest.TestCase):

    def messageFromSignature(signature):
        message = Message()
        message['Content-Type'] = 'application/pgp-signature; name="signature.asc"'
        message['Content-Description'] = 'OpenPGP digital signature'
        message.set_payload(signature)
        return message


    #Subject: [islab]{19/01/2022}Titolo News Prova
    #Body: Prova news
    #Content-type: text/plain
    #Firmata: SI

    def test_1(self):
        subject = '[islab]{19/01/2022}Titolo News Prova'
        body = 'Prova news'
        sendMailSigned(subject,body,'plain')
        time.sleep(1)
        news = newsmailDao.getLastByTitle('Titolo News Prova')
        self.assertEqual(newsmailDao.getStatus(news.msgid),2)
        newsmailDao.deleteNews(news.msgid)
        news2 = newsmailDao.getLastByTitle('Titolo News Prova')
        self.assertNotEqual(news2,news)
        self.assertIsNone(newsmailDao.get(news.msgid))
        sent_channels = SentDao.getChannels(news.msgid)
        self.assertEqual(0,len(sent_channels))

    #Subject: [islab]{19/01/2022}Titolo News Prova 2
    #Body: Prova news 2
    #Content-type: text/plain
    #Firmata: SI
    def test_2(self):
        subject = '[islab]{19/01/2022}Titolo News Prova 2'
        body = 'Prova news 2'
        sendMail(subject,body,'plain')
        time.sleep(1)
        news = newsmailDao.getLastByTitle('Titolo News Prova 2')
        self.assertEqual(newsmailDao.getStatus(news.msgid),1)
        sent_channels = SentDao.getChannels(news.msgid)
        self.assertEqual(len(sent_channels),1)
        self.assertEqual(sent_channels[0].name,'islab')
        newsmailDao.deleteNews(news.msgid)
        news2 = newsmailDao.getLastByTitle('Titolo News Prova 2')
        self.assertNotEqual(news2,news)
        self.assertIsNone(newsmailDao.get(news.msgid))
        sent_channels = SentDao.getChannels(news.msgid)
        self.assertEqual(0,len(sent_channels))

    #Subject: [islab,newchannel]{19/01/2022}Titolo News Prova 3
    #Body: <p><b>Prova News</b></p>
    #Content-type: text/html
    #Firmata: SI

    def test_3(self):
        subject = '[islab,newchannel]{19/01/2022}Titolo News Prova 3'
        body = '<p><b>Prova News</b></p>'
        sendMailSigned(subject,body,'html')
        time.sleep(1)
        news = newsmailDao.getLastByTitle('Titolo News Prova 3')
        self.assertEqual(newsmailDao.getStatus(news.msgid),2)
         #sent_channels = SentDao.getChannels("0f36f299e8fb373dd053127d30cce07577978854bbb3cb5f9cce3767c2d597d4")
        newchannel = ChannelDao.getChannel('newchannel')
        self.assertIsNotNone(newchannel)
        self.assertEqual(newchannel.name,'newchannel')
        self.assertEqual(newchannel.owner,tester)
        sent_channels = SentDao.getChannels(news.msgid)
        self.assertEqual(len(sent_channels),2)
        self.assertEqual(sent_channels[0].name,'islab')
        newsmailDao.deleteNews(news.msgid)
        news2 = newsmailDao.getLastByTitle('Titolo News Prova 3')
        self.assertNotEqual(news2,news)
        self.assertIsNone(newsmailDao.get(news.msgid))
        sent_channels = SentDao.getChannels(news.msgid)
        self.assertEqual(0,len(sent_channels))
        sendMailSigned('Delete channel','newchannel','plain')
        time.sleep(1)
        newchannel = ChannelDao.getChannel('newchannel')
        self.assertIsNone(newchannel)

    def test_4(self):
        subject = '[islab]Titolo News Prova 4'
        body = '# Prova news'
        sendMail(subject,body,'plain')
        time.sleep(1)
        news = newsmailDao.getLastByTitle('Titolo News Prova 4')
        self.assertEqual(newsmailDao.getStatus(news.msgid),1)
        subject = 'confirm news news.msgid'
        body = '# Prova news'




if __name__ == '__main__':
    unittest.main()
