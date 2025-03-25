from functions.actionsdb import ActionsDb
from .ChannelDao import ChannelDao
from .SenderDao import SenderDao

#This class permits to perform action on the table cansendon of newsmail

class CanSendOnDao:

    def check(user,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        code = ChannelDao.getCode(channel)
        if code is not None:
            userid = SenderDao.getId(user)
            sql = "SELECT * FROM cansendon where appuser = %s and channel = %s"
            val = (userid,code)
            cursor.execute(sql, val)
            records = cursor.fetchall()
            connection.close()
            return cursor.rowcount == 1
        return False

    def insert(user,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO cansendon (channel,appuser) VALUES(%s,%s)"
        code = ChannelDao.getCode(channel)
        iduser = SenderDao.getId(user)
        val = (code,iduser)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def delete(user,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "DELETE FROM cansendon WHERE channel = %s AND appuser = %s"
        code = ChannelDao.getCode(channel)
        iduser = SenderDao.getId(user)
        val = (code,iduser)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def getChannels(user):
        channels = []
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        userid = SenderDao.getId(user)
        sql = "SELECT channel FROM cansendon where appuser = %s"
        val = (userid,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        for row in records:
            channels.append(ChannelDao.getByCode(row[0]))
        connection.close()
        return channels
