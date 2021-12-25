from functions.actionsdb import ActionsDb
from .ChannelDao import ChannelDao
from .SenderDao import SenderDao

class CanSendOnDao:

    def check(sender,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        code = ChannelDao.getCode(channel)
        senderid = SenderDao.getId(sender)
        sql = "SELECT * FROM cansendon where appuser = %s and channel = %s"
        val = (senderid,code)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1

    def insert(sender,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO cansendon (channel,appuser) VALUES(%s,%s)"
        code = ChannelDao.getCode(channel)
        idsender = SenderDao.getId(sender)
        val = (code,idsender)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def delete(sender,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "DELETE FROM cansendon WHERE channel = %s AND appuser = %s"
        code = ChannelDao.getCode(channel)
        val = (code,sender)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()
