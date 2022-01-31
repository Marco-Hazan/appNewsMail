from ..ActionInterface import ActionInterface
from Dao.SentDao import SentDao
from newsmailDao import


class LegitChannelAction(ActionInterface):



    def __init__(self,newsmail,channel):
        self.newsmail = newsmail
        self.channel = channel


    def act():
        SentDao.insert(self.newsmail.msgid,self.channel,True)
