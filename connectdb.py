import mysql.connector
from cred import USERNAME, PASSWORD, DATABASE

def connect():
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )

    return mydb
