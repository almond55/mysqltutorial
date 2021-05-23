import mysql.connector
from cred import USERNAME, PASSWORD

def connect():
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        password=PASSWORD
    )

    return mydb
