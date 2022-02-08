from functions.config import Config
import email
import os
import markdown
import base64
from os import path
import shutil
from Dao.newsmailDao import newsmailDao
from functions.extract import Extraction
from Dao.ChannelDao import ChannelDao
from Dao.CanSendOnDao import CanSendOnDao
from Dao.SenderDao import SenderDao
from functions.mailfunctions import MailFunction
from Dao.SentDao import SentDao
import re

class NewsHandler:

    def updateTitlePattern(pattern):
        return "update title" in pattern and len(pattern.split(" ")) == 3 and len(pattern.split(" ")[2]) == 64

    def updateExpDatePattern(pattern):
        return "update expiration_date" in pattern and len(pattern.split(" ")) == 3 and len(pattern.split(" ")[2]) == 64

    def confirmPattern(pattern):
        return ("confirm news" in pattern and len(pattern.split(" ")) == 3 and len(pattern.split(" ")[2]) == 64)

    def updatePattern(pattern):
        return "update news" in pattern and len(pattern.split(" ")) == 3 and len(pattern.split(" ")[2]) == 64

    def deletePattern(pattern):
        return "delete news" in pattern and len(pattern.split(" ")) == 3 and len(pattern.split(" ")[2]) == 64

    def confirm_news(email,pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        # if status in not None: ----
        if status is 1 and newsmailDao.getSender(receivedMsgid) == sender:
            newsmailDao.updateStatus(receivedMsgid,2)
            newsmail = newsmailDao.get(receivedMsgid)
            bodyconfirm = Extraction.extractBody(email)
            split_confirm = bodyconfirm.split("\r\n")
            new_channels = split_confirm[1][split_confirm[1].find(":")+ 1:].split(",")
            for c in new_channels:
                ChannelDao.insert(c,sender)
                CanSendOnDao.insert(sender,c)
            attachments = split_confirm[2][split_confirm[2].find(":")+ 1:].split(",")
            unpublishedchannels = SentDao.getUnPublishedChannels(receivedMsgid)
            notpermittedchnames = []
            for ch in unpublishedchannels:
                notpermittedchnames.append(ch.name)
            MailFunction.sendPublishedMail(newsmail,sender,new_channels,attachments,notpermittedchnames)

    def delete_news(email,pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
            newsmailDao.deleteNews(receivedMsgid)
            pathAttachments = Config.get("attachments_path")+"/"+receivedMsgid
            if path.exists(pathAttachments):
                shutil.rmtree(pathAttachments)
            MailFunction.sendDeletedMail(receivedMsgid,sender)



    def update_news(email,pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
            pathAttachments = Config.get("attachments_path")+"/"+receivedMsgid
            if path.exists(pathAttachments):
                shutil.rmtree(pathAttachments)
            body = None
            bodyhtml = Extraction.extractHtml(email)
            if bodyhtml is None:
                bodyhtml = markdown.markdown(Extraction.extractBody(email)).replace("\n","<br>")
            newsmailDao.updateBody(receivedMsgid,body,bodyhtml)
            attachments = Extraction.extractAttachments(email,receivedMsgid)
            MailFunction.sendUpdatedMail(receivedMsgid,sender,body,bodyhtml,attachments)


    def update_title(email,pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
            title = Extraction.extractBody(email).strip()
            newsmailDao.updateTitle(receivedMsgid,title)

    def update_expirydate(email,pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
            expiration_date = Extraction.extractBody(email)
            pattern_expdate = re.compile("{[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\}")
            if pattern_expdate.match(expiration_date):
                newsmailDao.updateExpirationDate(receivedMsgid,expiration_date)


    def isNewsRelated(pattern):
        return (("confirm news" in pattern) or ("delete news" in pattern) or ("update news" in pattern)
        or "update title" in pattern or "update expiration_date" in pattern)


    def newsAction(email,pattern):
        if NewsHandler.confirmPattern(pattern):
            NewsHandler.confirm_news(email,pattern)
        elif NewsHandler.deletePattern(pattern):
            NewsHandler.delete_news(email,pattern)
        elif NewsHandler.updatePattern(pattern):
            NewsHandler.update_news(email,pattern)
        elif NewsHandler.updateTitlePattern(pattern):
            NewsHandler.update_title(email,pattern)
        elif NewsHandler.updateExpDatePattern(pattern):
            NewsHandler.update_expirydate(email,pattern)

'''

    if "confirm news" in subject and len(subject.split(" ")) == 3:

        receivedMsgid = subject.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is 1 and newsmailDao.getSender(receivedMsgid) == sender:
            newsmailDao.updateStatus(receivedMsgid,2)
            newsmail = newsmailDao.get(receivedMsgid)
            bodyconfirm = Extraction.extractBody(email)
            split_confirm = bodyconfirm.split("\r\n")
            new_channels = split_confirm[1][split_confirm[1].find(":")+ 1:].split(",")
            for c in new_channels:
                ChannelDao.insert(c,sender)
                CanSendOnDao.insert(sender,c)
            attachments = split_confirm[2][split_confirm[2].find(":")+ 1:].split(",")
            MailFunction.sendPublishedMail(newsmail,sender,new_channels,attachments)
            exit()
        else:
            exit()


    if "delete news" in subject and len(subject.split(" ")) == 3:
        receivedMsgid = subject.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
            newsmailDao.deleteNews(receivedMsgid)
            pathAttachments = "/home/marco/appNewsMail/attachments/"+receivedMsgid
            if path.exists(pathAttachments):
                shutil.rmtree(pathAttachments)
            MailFunction.sendDeletedMail(receivedMsgid,sender)
            exit()
        else:
            exit()


    if "update news" in subject and len(subject.split(" ")) == 3:
        receivedMsgid = subject.split(" ")[2]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is 2 and newsmailDao.getSender(receivedMsgid) == sender:
            pathAttachments = "/home/marco/appNewsMail/attachments/"+receivedMsgid
            if path.exists(pathAttachments):
                shutil.rmtree(pathAttachments)
            body = Extraction.extractBody(email)
            htmlbody = Extraction.extractHtmlBody(email)
            newsmailDao.updateBody(receivedMsgid,body,htmlbody)
            attachments = Extraction.extractAttachments(email,receivedMsgid)
            MailFunction.sendUpdatedMail(receivedMsgid,sender,body,htmlbody,attachments)
            exit()
        else:
            exit()
'''
