from Channel import Channel
from News import News

class SendOn:
    def __init__(self,news,channel):
        self.newsmail = news
        self.channel = channel

    def defineAction(self):
        if self.channel.is_active and CanSendOnDao.check(self.newsmail.sender,self.channel):
            return LegitChannelAction(self.newsmail,self.channel)
        if not channel.is_active:
            return NotActiveChannelAction(self.newsmail,self.channel)
        if not CanSendOnDao.check(self.newsmail.sender,self.channel):
            return NotLegitChannelAction(self.newsmail,self.channel)
        if self.channel.isnew and self.channel.owner == self.newsmail.sender:
            return NewChannelAction(self.newsmail,self.channel)
