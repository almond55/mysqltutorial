import mysql.connector
from connect import connect

def drop(dbname=None):
    mydb = connect()
    cursor = mydb.cursor()

    try:
        cursor.execute("DROP DATABASE %s" % dbname)
    except Exception as e:
        print(e)

    #show current databases
    cursor.execute("SHOW DATABASES")

    for x in cursor:
        print(x)


if __name__ == "__main__":
    drop('dummytutorial')
