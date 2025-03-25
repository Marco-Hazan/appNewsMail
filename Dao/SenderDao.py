
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
        idsender = None
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM appuser where username = %s"
        val = (sender,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        if not record is None:
            idsender = record[0]
        return idsender

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

    def getPassword(username):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT password FROM appuser where username = %s"
        val = (username,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        return record[0]

    def insert(username,code = None,password = None,firstname = None,lastname = None,is_active = False):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO appuser (username,password,firstname,lastname,is_active,verification_code) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (username,password,firstname,lastname,is_active,code)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def delete(username):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "DELETE FROM appuser WHERE username = %s"
        val = (username,)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def setActive(username):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE appuser SET is_active = TRUE WHERE username = %s"
        val = (username,)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def getAuthCode(username):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT verification_code FROM appuser where username = %s"
        val = (username,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        return record[0]

    def getNames(username):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT firstname,lastname FROM appuser where username = %s"
        val = (username,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        if record is not None and len(record) == 2:
            return [record[0],record[1]]
        connection.close()
