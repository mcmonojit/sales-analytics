import mysql.connector
from resources.dev import config

class MySQLClientManager:
    def __init__(self):

        self.connection = mysql.connector.connect(
            user = config.mysql_user,
            password = config.mysql_password,
            host = config.mysql_host,
            database = config.mysql_database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

# TODO:
# what is the utility of cursor
# Why the need to close cursor when closing connection
# How to correctly implement try catch handler on this MySQl connection