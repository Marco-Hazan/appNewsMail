from functions.actionsdb import ActionsDb
from Objects.Channel import Channel


class ChannelDao:



    def getChannel(name):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM channel where name = %s"
        val = (channel,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        if cursor == None:
            return None
        return Channel(record[0],record[1],record[2],record[3])

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
        return record[0]

    def insert(name,owner):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO channel (name,owner) VALUES(%s,%s)"
        val = (name,owner)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def enable(name):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE CHANNEL SET is_active = TRUE WHERE code = %s"
        val = (getCode(name),)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def disable(name):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE CHANNEL SET is_active = FALSE WHERE code = %s"
        val = (getCode(name),)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()
