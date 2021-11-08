import confuse
import psycopg2
import mysql.connector
import functions.News

config = confuse.Configuration('appNewsMail')
config.set_file('/var/www/appNewsMail/master/config.yaml')

def connectionPostgres():
    # Connect to an existing database
    connection = psycopg2.connect(user = config['database']['user_db'],
                                  password= config['database']['password_db'],
                                  host = config['database']['host'],
                                  port = config['database']['port'],
                                  database = config['database']['db_name'])
    cursor = connection.cursor()
    cursor.execute("Set search_path to newsmail;")
    return connection

def connectionMysql():
    connection = mysql.connector.connect(user = config['database']['user_db'].__str__(), password = config['database']['password_db'].__str__(),
                          host = config['database']['host'].__str__(),
                          database = config['database']['db_name'].__str__())
    return connection

class ActionsDb:

    def connectdb(self):
        dbms = config['database']['dbms'].get()
        if dbms == 'postgresql':
            conn = connectionPostgres()
            print(conn)
            return conn
        elif dbms == 'mysql-server':
            conn = connectionMysql()
            print(conn)
            return conn
