from functions.actionsdb import ActionsDb
class AttachmentDao:

    def insert(self,msgid,attachments):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO attachment (newsmail,name) VALUES(%s,%s)"
        for at in attachments:
            val = (msgid,at)
            cursor.execute(sql,val)
            connection.commit()
        connection.close()
