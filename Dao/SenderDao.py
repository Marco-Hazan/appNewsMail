from functions.actionsdb import ActionsDb



class SenderDao:

    def isActive(sender):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM appuser where username = %s and is_active = true"
        val = (sender,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1

    def getId(sender):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM appuser where username = %s"
        val = (sender,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        return record[0]

    def getUsername(id):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT username FROM appuser where id = %s"
        val = (id,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        return record[0]
