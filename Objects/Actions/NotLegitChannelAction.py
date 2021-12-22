from ..ActionInterface import ActionInterface
from Dao.SentDao import SentDao
from functions.mailfunctions
from functions.mailfunctions import MailFunction


class NotLegitChannelAction(ActionInterface):



    def __init__(self,newsmail,channel):
        self.newsmail = newsmail
        self.channel = channel


    def act():
        SentDao.insert(self.newsmail.msgid,self.channel,False)
        MailFunction.sendRequestToPublish(self.channel,self.channel.owner,self.newsmail)
