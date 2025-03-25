import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions.config import Config
from Dao.SentDao import SentDao
from Dao.newsmailDao import newsmailDao

def sendMail(rcpt:str, content:str,subject):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = Config.get("smtpmail")
    msg['To'] = rcpt
    msg.attach(MIMEText(content,'html'))
    s = smtplib.SMTP(Config.get("smtphost"))
    s.starttls()
    s.login(Config.get("smtpuser"),Config.get("smtppassword"))
    s.sendmail(Config.get("smtpmail"), rcpt, msg.as_string())
    s.quit()