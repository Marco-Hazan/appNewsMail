from functions.actionsdb import ActionsDb

class ChannelDao:

    def isActive(self,channel):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM channel where name = %s and is_active = true"
        val = (channel,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1

    def getCode(self,channelname):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM channel where name = %s"
        val = (channelname,)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        return record[0]
