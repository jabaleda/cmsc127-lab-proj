import os
import mysql.connector as database

# username = os.environ.get("DB_USER", "root")
# password = os.environ.get("DB_PASSWORD", "mariadb")

# connect to database
connection = database.connect(
    user="root",                                        # Uses root user
    password="poi",                                     # ! Change this to your password
    host='localhost',
    database="projectdb"                                # ! Change this to the name of project database you use
)

cursor = connection.cursor()