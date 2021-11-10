from functions.actionsdb import ActionsDb

class SenderDao:

    def isActive(self,sender):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM appuser where username = %s and is_active = true"
        val = (sender,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 1
