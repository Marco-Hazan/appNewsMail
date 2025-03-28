from functions.actionsdb import ActionsDb
from Objects.Channel import Channel
from .SenderDao import SenderDao


class ChannelDao:


    def getUserChannel(user):
        channels = []
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT name,is_active,owner FROM channel where owner = %s"
        val = (SenderDao.getId(user),)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        for record in rows:
            channels.append(Channel(record[0],record[1],SenderDao.getUsername(record[2]),False))
        connection.close()
        return channels

    def getChannel(name):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT name,is_active,owner FROM channel where name = %s"
        val = (name,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        if record == None:
            return None
        return Channel(record[0],record[1],SenderDao.getUsername(record[2]),False)

    def exists(channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM channel where name = %s"
        val = (channel,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1

    def isActive(channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM channel where name = %s and is_active = true"
        val = (channel,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1

    def isOwner(user,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        userid = SenderDao.getId(user)
        sql = "SELECT * FROM channel where name = %s and owner = %s"
        val = (channel,userid)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1

    def isntActive(channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM channel where name = %s and is_active = false"
        val = (channel,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1

    def getCode(channelname):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM channel where name = %s"
        val = (channelname,)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        if record is not None:
            return record[0]
        return None

    def getName(code):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT name FROM channel where code = %s"
        val = (code,)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        return record[0]

    def insert(channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO channel (name,owner) VALUES(%s,%s)"
        ownerid = SenderDao.getId(channel.owner)
        val = (channel.name,ownerid)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def delete(name,owner):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "DELETE FROM channel WHERE name = %s AND owner = %s"
        ownerid = SenderDao.getId(owner)
        val = (name,ownerid)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def enable(name):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE CHANNEL SET is_active = TRUE WHERE code = %s"
        val = (ChannelDao.getCode(name),)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def disable(name):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE CHANNEL SET is_active = FALSE WHERE code = %s"
        print(name)
        print(ChannelDao.getCode('islab'))
        val = (ChannelDao.getCode(name),)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def getByCode(code):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT name,is_active,owner FROM channel where code = %s"
        val = (code,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        if cursor == None:
            return None
        return Channel(record[0],record[1],SenderDao.getUsername(record[2]),False)

    def updateName(oldname,newname):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE CHANNEL SET name = %s WHERE code = %s"
        val = (ChannelDao.getCode(oldname),newname)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()
