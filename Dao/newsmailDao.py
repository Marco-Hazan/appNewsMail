from functions.actionsdb import ActionsDb
from SentDao import SentDao
from SenderDao import SenderDao
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
        sender_id = SenderDao.getId(newsmail.sender)
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "INSERT INTO newsmail (msgid,sender,title,body,htmlbody,creation_date,expiration_date) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val = (
            newsmail.msgid,
            sender_id,
            newsmail.title,
            newsmail.body,
            newsmail.htmlbody,
            newsmail.creation_date,
            newsmail.expiration_date
            )
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def updateStatus(msgid,statuscode):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE newsmail set statuscode = %s where msgid = %s"
        val = (statuscode,msgid)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def getStatus(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT statuscode FROM newsmail where msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        return record[0]


    def getSender(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT appuser.username FROM newsmail JOIN appuser ON appuser.id = newsmail.sender where msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        return record[0]

    def deleteNews(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "DELETE FROM newsmail WHERE msgid = %s"
        val = (msgid,)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()

    def updateBody(msgid,body,htmlbody):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE newsmail set body = %s,htmlbody = %s where msgid = %s"
        val = (body,htmlbody,msgid)
        cursor.execute(sql,val)
        connection.commit()
        connection.close()
