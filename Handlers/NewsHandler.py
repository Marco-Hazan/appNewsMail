from functions.config import Config
import markdown
from functions.Attachments import Attachments
from os import path
import shutil
from Dao.newsmailDao import newsmailDao
from functions.extract import Extraction
from Dao.ChannelDao import ChannelDao
from functions.mailfunctions import MailFunction
from Dao.SentDao import SentDao
from .RegistrationHandler import RegistrationHandler
import re
import datetime
from datetime import timedelta
from datetime import datetime

class NewsHandler:

    def updateTitlePattern(pattern):
        return ("update title" in pattern and len(pattern.split(
            "update title ")) > 1 and len(pattern.split("update title ")[1]) == 64)

    def updateExpDatePattern(pattern):
        print("is expiration_date pattern?")
        return "update expiration_date" in pattern and len(pattern.split(
            "update expiration_date ")) > 1 and len(pattern.split("update expiration_date ")[1]) == 64

    def confirmPattern(pattern):
        return ("confirm news" in pattern and len(pattern.split(
            "confirm news ")) > 1 and len(pattern.split("confirm news ")[1]) == 64)

    def updatePattern(pattern):
        return "update news" in pattern and len(pattern.split(
            "update news ")) > 1 and len(pattern.split("update news ")[1]) == 64

    def deletePattern(pattern):
        return "delete news" in pattern and len(pattern.split(
            "delete news ")) > 1 and len(pattern.split("delete news ")[1]) == 64

    def confirm_news(mail, pattern):
        sender = Extraction.extractSender(mail)
        receivedMsgid = pattern.split("confirm news ")[1]
        status = newsmailDao.getStatus(receivedMsgid)
        if status is not None:
            if (
                    status == 1
                    and newsmailDao.getSender(receivedMsgid) == sender
            ):
                public_key_path = Extraction.extractPublicKey(mail)
                if public_key_path is not None:
                    print("Oh dovresti registrare la chiave pubblica")
                    RegistrationHandler.registerKey(public_key_path)
                newsmail = newsmailDao.get(receivedMsgid)
                channels = SentDao.getChannels(receivedMsgid)
                new_channels = []
                for c in channels:
                    if (
                        c.owner == sender
                        and (c.is_active is False)
                        and (SentDao.totNews(c.name) == 1)
                    ):
                        new_channels.append(c.name)
                        ChannelDao.enable(c.name)
                attachments = Attachments.getAttachments(receivedMsgid[0:32])
                unpublishedchannels = SentDao.getUnPublishedChannels(
                    receivedMsgid)
                notpermittedchnames = []
                for ch in unpublishedchannels:
                    if (
                        ch.owner == sender and
                        not ch.is_active and
                        Config.get("enablechannel_on_ownernews")
                    ):
                        ChannelDao.enable(ch.name)
                        SentDao.enable(receivedMsgid,ch.name)
                    notpermittedchnames.append(ch.name)
                newsmailDao.updateStatus(receivedMsgid, 2)
                MailFunction.sendPublishedMail(
                    newsmail, sender, new_channels, attachments,
                    notpermittedchnames
                )

    def delete_news(email, pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split("delete news ")[1]
        if (
            newsmailDao.getSender(receivedMsgid) == sender
        ):
            newsmailDao.deleteNews(receivedMsgid)
            pathAttachments = Config.get(
                "attachments_path")+"/"+receivedMsgid[0:32]
            if path.exists(pathAttachments):
                shutil.rmtree(pathAttachments)
            MailFunction.sendDeletedMail(receivedMsgid, sender)

    def update_news(email, pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split("update news ")[1]
        if (
            newsmailDao.getSender(receivedMsgid) == sender
        ):
            pathAttachments = Config.get("attachments_path")+"/"+receivedMsgid[0:32]
            if path.exists(pathAttachments):
                shutil.rmtree(pathAttachments)
            body = Extraction.extractBody(email)
            bodyhtml = Extraction.extractHtml(email)
            if bodyhtml is None:
                bodyhtml = markdown.markdown(
                    Extraction.extractBody(email))
            newsmailDao.updateBody(receivedMsgid, body, bodyhtml)
            attachments = Extraction.extractAttachments(email, receivedMsgid)
            MailFunction.sendUpdatedMail(
                newsmailDao.get(receivedMsgid), attachments
            )

    def update_title(email, pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split("update title ")[1]
        status = newsmailDao.getStatus(receivedMsgid)
        print("sto aggiornando titolo...")
        if (
            status == 2
            and newsmailDao.getSender(receivedMsgid) == sender
        ):
            title = Extraction.extractBody(email).strip()
            newsmailDao.updateTitle(receivedMsgid, title)

    def update_expirydate(email, pattern):
        sender = Extraction.extractSender(email)
        receivedMsgid = pattern.split("update expiration_date ")[1]
        status = newsmailDao.getStatus(receivedMsgid)
        if (
            status == 2
            and newsmailDao.getSender(receivedMsgid) == sender
        ):
            expiration_date = Extraction.extractBody(email)
            print("expiration_date: "+expiration_date)
            pattern_expdate = re.compile(
                "[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]")
            if pattern_expdate.match(expiration_date):
                print("mattcha")
                expiration_date = datetime.strptime(expiration_date, '%d/%m/%Y')
                print(expiration_date)
                expiration_date = expiration_date.strftime("%Y-%m-%d %H:%M")
                print(expiration_date)
                newsmailDao.updateExpirationDate(
                    receivedMsgid, expiration_date)

    def isNewsRelated(pattern):
        return (("confirm news" in pattern) or ("delete news" in pattern)
                or ("update news" in pattern) or "update title" in pattern
                or "update expiration_date" in pattern)

    def newsAction(email, pattern):
        pattern = pattern.replace("\r","").replace("\n","")
        print(NewsHandler.updateTitlePattern(pattern))
        if NewsHandler.confirmPattern(pattern):
            NewsHandler.confirm_news(email, pattern)
        elif NewsHandler.deletePattern(pattern):
            NewsHandler.delete_news(email, pattern)
        elif NewsHandler.updatePattern(pattern):
            NewsHandler.update_news(email, pattern)
        elif NewsHandler.updateTitlePattern(pattern):
            print("update title")
            NewsHandler.update_title(email, pattern)
        elif NewsHandler.updateExpDatePattern(pattern):
            print("SI é Expiration pattern")
            NewsHandler.update_expirydate(email, pattern)
