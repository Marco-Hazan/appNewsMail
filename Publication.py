from Dao.SenderDao import SenderDao
from Dao.SentDao import SentDao
from Dao.CanSendOnDao import CanSendOnDao
from Dao.ChannelDao import ChannelDao
from Dao.newsmailDao import newsmailDao
from Objects.Channel import Channel

def extractBody(email):
    body = None
    if email.get_content_type() == 'text/plain':
        body = email.get_payload()
    return body

class ChannelHandler:

    #Extract channels
    def extractChannels(sender,channels):
        arr_channels = []
        for chname in channels:
            if ChannelDao.getChannel(chname) == None: #if channel is new then assign the ownership to the sender
                arr_channels.append(Channel(chname,chname,sender,True))
            else:
                arr_channels.append(ChannelDao.getChannel(chname))
        return arr_channels

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

    def deleteChannel(name,owner):
        ChannelDao.delete(name,owner)

    def enableChannel(name):
        ChannelDao.enable(name)

    def disableChannel(name):
        ChannelDao.disable(name)

    def reject(msgid,channel):
        SentDao.delete(msgid,channel)

    def isLegit(chname,sender):
        return (ChannelDao.isActive(chname) and (CanSendOnDao.check(sender,chname) or ChannelDao.isOwner(sender,chname)))

    def IsChannelRelatedPattern(pattern):
        return ("Create channel" in pattern or "Delete channel" in pattern or
        "Enable channel" in pattern or "Disable channel" in pattern or
        "Enable user on channel" in pattern or "Disable user on channel" in pattern or
        "Enable publication" in pattern or "Reject" in pattern)

    def ChannelAction(pattern,email):
        if "Create channel" in pattern:
            tot_sender = email.get('From')
            sender = tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]
            ChannelHandler.createChannel(extractBody(email).strip(),sender)
        elif "Delete channel" in pattern:
            tot_sender = email.get('From')
            sender = tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]
            ChannelHandler.deleteChannel(extractBody(email).strip(),sender)
        elif "Enable channel" in pattern:
            ChannelHandler.enableChannel(extractBody(email).strip())
            return True
        elif "Disable channel" in pattern:
            ChannelHandler.disableChannel(extractBody(email).strip())
            return True
        elif "Enable user on channel" in pattern:
            users = str(email.get('Cc')).split(", ")
            ChannelHandler.EnableUsersOnChannel(users,extractBody(email).strip())
            return True
        elif "Disable user on channel" in pattern:
            users = str(email.get('Cc')).split(", ")
            ChannelHandler.DisableUsersOnChannel(users,extractBody(email).strip())
            return True
        elif "Enable publication" in pattern:
            print(pattern.split(" "))
            if len(pattern.split(" ")) == 4 and ("once" in pattern.split(" ")[2]) and len(pattern.split(" ")[3]) == 64:
                ChannelHandler.EnableOnceNews(pattern.split(" ")[3],extractBody(email).strip())
                return True
            elif len(pattern.split(" ")) == 4 and ("always" in pattern.split(" ")[2]) and len(pattern.split(" ")[3]) == 64:
                tot_sender = email.get('From')
                sender = tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]
                newsmail = newsmailDao.get(pattern.split(" ")[3])
                ChannelHandler.EnableUserOnChannel(newsmail.sender,extractBody(email).strip())
                return True
        elif "Reject" in pattern and len(pattern.split(" ")) == 3 and len(pattern.split(" ")[2]) == 64:
            ChannelHandler.reject(pattern.split(" ")[2],extractBody(email).strip())
            return True
        return None
