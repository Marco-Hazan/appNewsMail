from functions.actionsdb import ActionsDb
from .SentDao import SentDao
from Objects.News import News
from .SenderDao import SenderDao
import time
import datetime
from datetime import timedelta
from datetime import datetime


class newsmailDao:

    def getStatus(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        connection.close()
        if row is not None:
            return row[5]
        return None

    def getLast(username):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where sender = %s ORDER BY creation_date DESC"
        idsender = SenderDao.getId(username)
        val = (idsender,)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        connection.close()
        if row is not None:
            return News(row[0], row[1], row[2], row[3], row[4], row[6], row[7])
        return None

    def getLastByTitle(title):
        news = None
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where title = %s ORDER BY creation_date DESC"
        val = (title,)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        connection.close()
        if row is not None:
            creation_date = row[6]
            creation_date = creation_date.strftime("%d/%m/%Y")
            expiration_date = row[7]
            if expiration_date is not None:
                expiration_date = expiration_date.strftime("%d/%m/%Y")
            return News(row[0], SenderDao.getUsername(row[1]), row[2], row[3], row[4],creation_date, expiration_date)
        return None

    def get(msgid):
        news = None
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        if row is not None:
            sender = SenderDao.getUsername(row[1])
            connection.close()
            news = News(msgid, sender, row[2], row[3], row[4], row[6], row[7])
        return news

    def isUnique(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        records = cursor.fetchall()
        connection.close()
        return cursor.rowcount == 0

    def insert(newsmail, confirmed):
        sender_id = SenderDao.getId(newsmail.sender)
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        if confirmed:
            statuscode = 2
        else:
            statuscode = 1
        sql = "INSERT INTO newsmail (msgid,sender,title,body,htmlbody,creation_date,expiration_date,statuscode) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (
            newsmail.msgid,
            sender_id,
            newsmail.title,
            newsmail.body,
            newsmail.htmlbody,
            newsmail.creation_date,
            newsmail.expiration_date,
            statuscode
            )
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def updateStatus(msgid, statuscode):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE newsmail set statuscode = %s where msgid = %s"
        val = (statuscode, msgid)
        cursor.execute(sql, val)
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
        if record is not None:
            return record[0]
        return None

    def getSender(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT appuser.username FROM newsmail JOIN appuser ON appuser.id = newsmail.sender where msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        record = cursor.fetchone()
        connection.close()
        if record is not None:
            return record[0]
        return None

    def deleteNews(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "DELETE FROM newsmail WHERE msgid = %s"
        val = (msgid,)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def updateBody(msgid, body, htmlbody):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE newsmail set body = %s,htmlbody = %s where msgid = %s"
        val = (body, htmlbody, msgid)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def updateTitle(msgid, title):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "UPDATE newsmail set title = %s where msgid = %s"
        val = (title, msgid)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def updateExpirationDate(msgid, expiration_date):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        print("hello")
        sql = "UPDATE newsmail set expiration_date = %s where msgid = %s"
        val = (expiration_date, msgid)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()

    def getByTitleAndUser(user, title):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where sender = %s AND title = %s ORDER BY creation_date DESC"
        val = (SenderDao.getId(user), title)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        connection.close()
        if row is not None:
            return News(row[0], SenderDao.getUsername(row[1]), row[2], row[3], row[4], row[6], row[7])
        return None

    def getBody(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT body from newsmail WHERE msgid = %s"
        val = (msgid, )
        cursor.execute(sql, val)
        row = cursor.fetchone()
        connection.close()
        if row is not None:
            return row[0]
        return None

    def getHtmlBody(msgid):
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT htmlbody from newsmail WHERE msgid = %s"
        val = (msgid, )
        cursor.execute(sql, val)
        row = cursor.fetchone()
        connection.close()
        if row is not None:
            return row[0]
        return None

    def getByFirst32(first32_msgid):
        news = None
        actionsDb = ActionsDb()
        connection = actionsDb.connectdb()
        cursor = connection.cursor()
        sql = "SELECT * FROM newsmail where msgid LIKE %s"
        val = ("%"+first32_msgid+"%",)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        if row is not None:
            sender = SenderDao.getUsername(row[1])
            connection.close()
            news = News(row[0], sender, row[2], row[3], row[4], row[6], row[7])
        return news
