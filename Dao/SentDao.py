from functions.actionsdb import ActionsDb
from ChannelDao import ChannelDao
class SentDao:

    def insertAll(msgid,channels):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO senton (newsmail,channel) VALUES(%s,%s)"
        for c in channels:
            code = ChannelDao.getCode(c)
            val = (msgid,code)
            cursor.execute(sql,val)
            connection.commit()
        connection.close()

    def insert(msgid,channel,enable):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO senton (newsmail,channel,enable) VALUES(%s,%s,%s)"
        code = ChannelDao.getCode(channel)
        val = (msgid,code,enable)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def enable(msgid,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE senton SET enable = TRUE WHERE newsmail = %s AND channel = %s"
        code = ChannelDao.getCode(channel)
        val = (msgid,code)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def disable(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE senton SET enable = FALSE WHERE newsmail = %s AND channel = %s"
        code = ChannelDao.getCode(channel)
        val = (msgid,code)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()
