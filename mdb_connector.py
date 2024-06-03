import os
import mysql.connector as database

username = os.environ.get("DB_USER", "root")                # use your root
password = os.environ.get("DB_PASSWORD", "mariadb")         # change this to the password of your root

# connect to database
connection = database.connect(
    user=username,                                       
    password=password,                                     
    host='localhost',
    database="cmsc127project"                          
)

cursor = connection.cursor()

def reconnect():
    global connection, cursor
    if not connection.is_connected():
        connection.reconnect()
        cursor = connection.cursor()
