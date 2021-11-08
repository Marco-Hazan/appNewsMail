from functions.actionsdb import ActionsDb
import time
import datetime

class newsmailDao:

    def isUnique(self,msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 0

    def insert(self,newsmail):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO newsmail (msgid,sender,subject,body,htmlbody,creation_date,expiration_date,pub_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (
            newsmail.msgid,
            newsmail.sender,
            newsmail.subject,
            newsmail.body,
            newsmail.htmlbody,
            newsmail.creation_date,
            newsmail.expiration_date,
            newsmail.pub_date
            )
        cursor.execute(sql,val)
        connection.commit()
        connection.close()
