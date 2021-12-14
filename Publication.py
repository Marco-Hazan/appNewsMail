from SenderDao import SenderDao
from SentDao import SentDao
from CanSendOnDao import CanSendOnDao
from ChannelDao import ChannelDao
from Objects.Channel import Channel

class ChannelHandler:

    def extractChannels(sender,channels):
        arr_channels = []
        for chname in channels:
            if ChannelDao.get(chname) == None:
                arr_channels.append(Channel(chname,chname,sender,True))
            else:
                arr_channels.append(ChannelDao.get(chname))

    def extractLegitChannels(user,channels):
        arr_channels = []
        for c in channels:
            if (ChannelDao.isActive(c) and CanSendOnDao.check(user,c)) or not ChannelDao.exists(c):
                arr_channels.append(c)
        return arr_channels

    def extractNonActiveChannels(channels):
        arr_channels = []
        for c in channels:
            if ChannelDao.isntActive(c):
                arr_channels.append(c)
        return arr_channels

    def extractNotPermittedChannels(user,channels):
        arr_channels = []
        for c in channels:
            if ChannelDao.exists(c) and not CanSendOnDao.check(user,c):
                arr_channels.append(c)
        return arr_channels

    def extractNewChannels(channels):
        arr_channels = []
        for c in channels:
            if not ChannelDao.exists(c):
                arr_channels.append(c)
        return arr_channels

    def extractBody(email):
        body = None
        if email.get_content_type() == 'text/plain':
            body = email.get_payload()
        return body

    def EnableUsersOnChannel(users,channel):
        for u in users:
            if SenderDao.isActive(u):
                CanSendOnDao.insert(u,channel)

    def DisableUsersOnChannel(users,channel):
        for u in users:
            if SenderDao.isActive(u):
                CanSendOnDao.delete(u,channel)


    def EnableOnceNews(msgid,channel):
        SentDao.enable(msgid,channel)



    def EnableUserOnChannel(user,channel):
        if SenderDao.isActive(user):
            CanSendOnDao.insert(user,channel)

    def createChannel(name,owner):
        ChannelDao.insert(name,owner)

    def enableChannel(name):
        ChannelDao.enable(name)

    def disableChannel(name):
        ChannelDao.disable(name)

    def reject(msgid,channel):
        SentDao.disable(msgid,channel)

    def IsChannelRelatedPattern(pattern):
        return "Enable channel" in pattern or "Disable channel" in pattern or
        "Enable user on channel" in pattern or "Disable user on channel" in pattern or
        "Enable publication" in pattern or "Reject" in pattern

    def ChannelAction(pattern,email):
        if "Enable channel" in pattern:
            enableChannel(extractBody(email))
            return True
        elif "Disable channel" in pattern:
            disableChannel(extractBody(email))
            return True
        elif "Enable user on channel" in pattern:
            users = str(newsmail.get('Cc')).split(", ")
            EnableUsersOnChannel(users,extractBody(email))
            return True
        elif "Disable user on channel" in pattern:
            users = str(newsmail.get('Cc')).split(", ")
            DisableUsersOnChannel(users,extractBody(email))
            return True
        elif "Enable publication" in pattern:
            if len(pattern.split(" ")) == 3 and len(pattern.split(" ")[2]) == 64:
                EnableOnceNews(pattern.split(" ")[2],extractBody(email))
                return True
            elif len(pattern.split(" ")) == 3 and pattern.split(" ")[2] == "always" and len(pattern.split(" ")[3]) == 64:
                tot_sender = email.get('From')
                sender = tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]
                EnableUserOnChannel(sender,extractBody(email))
                return True
        elif "Reject" in pattern and len(pattern.split(" ")) == 2 and len(pattern.split(" ")[1]) == 64:
            reject(pattern.split(" ")[1],extractBody(email))
            return True
        return None
