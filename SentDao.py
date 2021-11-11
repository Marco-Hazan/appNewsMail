from functions.actionsdb import ActionsDb
from ChannelDao import ChannelDao
class SentDao:

    def insert(self,msgid,channels):
        actionsDb = ActionsDb()
        channelDao = ChannelDao()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO sent (newsmail,channel) VALUES(%s,%s)"
        for c in channels:
            code = channelDao.getCode(c)
            val = (msgid,code)
            cursor.execute(sql,val)
            connection.commit()
        connection.close()
