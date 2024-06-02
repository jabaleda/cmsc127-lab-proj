
# import os
import mysql.connector as database

# connect to database
connection = database.connect(
    user="root",                                        # Uses root user
    password="poi",                                     # ! Change this to your password
    host="127.0.0.1",
    database="projectdb"                                # ! Change this to the name of project database you use
)

cursor = connection.cursor()