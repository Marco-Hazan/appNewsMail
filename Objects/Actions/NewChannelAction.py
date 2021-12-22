from ..ActionInterface import ActionInterface
from Dao.SentDao import SentDao
from functions.mailfunctions import MailFunction

class NewChannelAction(ActionInterface):



    def __init__(self,newsmail,channel):
        self.newsmail = newsmail
        self.channel = channel


    def act():
        ChannelDao.insert(channel.name,channel.owner)
        MailFunction.sendCreatedChannel(channel.name,newsmail.sender)
