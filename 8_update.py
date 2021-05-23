import mysql.connector
from connectdb import connect

def update(table=None, setdata=None, where=None):
    # setdata = dict {'type': 'content'}
    # where = dict {'type': 'content'}

    mydb = connect()
    cursor = mydb.cursor()

    sql = "UPDATE %s" % table
    val = []

    for data in setdata:
        if "SET" not in sql:
            sql += " SET "
        else:
            sql += ", "
        sql += "%s = " % data
        sql += "%s"
        val.append(setdata[data])

    for lookup in where:
        if "WHERE" not in sql:
            sql += " WHERE "
        else:
            sql += " AND "
        if "%" in where[lookup]:
            sql += "%s LIKE " % (lookup)
        else:
            sql += "%s = " % (lookup)
        sql += "%s"
        val.append(where[lookup])

    val = tuple(val)
    
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        print(e)

    print(cursor.rowcount, "row(s) affected from %s." % table)

if __name__ == "__main__":
    update('staff', setdata={'name': 'Ronald'}, where={"id":"100"})
