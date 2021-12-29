from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import Message
import smtplib
import gnupg
import time
import unittest
from Dao.newsmailDao import newsmailDao

class TestNews(unittest.TestCase):

    def messageFromSignature(signature):
        message = Message()
        message['Content-Type'] = 'application/pgp-signature; name="signature.asc"'
        message['Content-Description'] = 'OpenPGP digital signature'
        message.set_payload(signature)
        return message


    #Subject: [islab]{19/01/2022}Titolo News
    #Body: Prova news

    #Test di un text plain co

    def test_1(self):
        basemsg = MIMEMultipart()
        basemsg.attach(MIMEText('Prova news','plain'))
        gpg = gnupg.GPG(gnupghome='/home/marco/.gnupg')
        basetext = basemsg.as_string().replace('\n', '\r\n')
        signature = str(gpg.sign(basetext, detach=True))
        self.assertNotEqual(signature,None)
        signmsg = TestNews.messageFromSignature(signature)
        msg = MIMEMultipart(_subtype="signed", micalg="pgp-sha1",
        protocol="application/pgp-signature")
        msg['Subject'] = '[islab]{19/01/2022}Titolo News2'
        msg['From'] = 'marco@islab.di.unimi.itt'
        msg.attach(basemsg)
        msg.attach(signmsg)
        s = smtplib.SMTP("localhost")
        s.sendmail("marco@islab.di.unimi.itt",["newsmail@islab.di.unimi.it"], msg.as_string())
        s.quit()
        time.sleep(1)
        news = newsmailDao.getLast('marco@islab.di.unimi.it')
        print(news.msgid)
        self.assertEqual(newsmailDao.getStatus(news.msgid),2)

    def test_2(self):
        basemsg = MIMEMultipart()
        basemsg.attach(MIMEText('Prova news','plain'))
        basetext = basemsg.as_string().replace('\n', '\r\n')
        msg = MIMEMultipart()
        msg['Subject'] = '[islab]{19/01/2022}Titolo News1'
        msg['From'] = 'marco@islab.di.unimi.itt'
        msg.attach(basemsg)
        s = smtplib.SMTP("localhost")
        print(msg.as_string())
        s.sendmail("marco@islab.di.unimi.itt",["newsmail@islab.di.unimi.it"], msg.as_string())
        s.quit()
        time.sleep(1)
        news = newsmailDao.getLast('marco@islab.di.unimi.it')
        print(news.msgid)
        self.assertEqual(newsmailDao.getStatus(news.msgid),1)


testnews = TestNews()
testnews.test_2()

if __name__ == '__main__':
    unittest.main()
