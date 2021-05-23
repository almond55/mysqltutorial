import mysql.connector
from connect import connect

def create(dbname=None):
    mydb = connect()
    cursor = mydb.cursor()

    try:
        cursor.execute("CREATE DATABASE %s" % dbname)
    except Exception as e:
        print(e)

    #show current databases
    cursor.execute("SHOW DATABASES")

    for x in cursor:
        print(x)


if __name__ == "__main__":
    create('dummytutorial')
