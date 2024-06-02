import os
import mysql.connector as database

username = os.environ.get("DB_USER", "root")
password = os.environ.get("DB_PASSWORD", "mariadb")

# connect to database
connection = database.connect(
    user=username,                                        # Uses root user
    password=password,                                     # ! Change this to your password
    host='localhost',
    database="cmsc127project"                                # ! Change this to the name of project database you use
)

cursor = connection.cursor()