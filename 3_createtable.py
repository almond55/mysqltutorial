import mysql.connector
from connectdb import connect

def create(table=None, data=None):
    # data = dict. type follows sql type to the letter
    mydb = connect()
    cursor = mydb.cursor()

    schema = None
    for item in data:
        if not schema:
            schema = "%s %s" % (item, data[item])
        else:
            schema += ", %s %s" % (item, data[item])

    sql = "CREATE TABLE %s (%s)" % (table, schema)

    try:
        cursor.execute(sql)
        print("Table %s created." % table)
    except Exception as e:
        print(e)

    try:
        cursor.execute("DESCRIBE %s" % table)
        for x in cursor:
            print(x)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    create('staff', {'name': 'VARCHAR(255)', 'id': 'INT'})
