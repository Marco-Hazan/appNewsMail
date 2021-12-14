import yaml
import psycopg2
import mysql.connector
import functions.News
from functions.config import Config

def connectionPostgres():
    # Connect to an existing database
    connection = psycopg2.connect(user = Config.getInnested("database","user_db"),
                                  password= Config.getInnested("database","password_db"),
                                  host = Config.getInnested("database","host"),
                                  port = Config.getInnested("database","port"),
                                  database = Config.getInnested("database","db_name"))
    cursor = connection.cursor()
    cursor.execute("Set search_path to newsmail;")
    return connection

def connectionMysql():
    connection = mysql.connector.connect(user = Config.getInnested("database","user_db").__str__(), password = config['database']['password_db'].__str__(),
                          host = Config.get("database","host").__str__(),
                          database = Config.get("database","db_name").__str__())
    return connection

class ActionsDb:

    def connectdb(self):
        dbms = Config.getInnested("database","dbms")
        if dbms == 'postgresql':
            conn = connectionPostgres()
            return conn
        elif dbms == 'mysql-server':
            conn = connectionMysql()
            return conn
