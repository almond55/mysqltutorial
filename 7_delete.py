import mysql.connector
from connectdb import connect

def delete(table=None, where=None):
    # fields = list
    # where = dict {'type': 'content'}
    # limit = int
    # orderby = field type(str)
    mydb = connect()
    cursor = mydb.cursor()

    sql = "DELETE FROM %s" % table

    if where:
        for lookup in where:
            if "WHERE" not in sql:
                sql += " WHERE "
            else:
                sql += " AND "
            if "%" in where[lookup]:
                sql += "%s LIKE '%s'" % (lookup, where[lookup])
            else:
                sql += "%s = '%s'" % (lookup, where[lookup])
    
    try:
        cursor.execute(sql)
        mydb.commit()
    except Exception as e:
        print(e)

    print(cursor.rowcount, "row(s) deleted from %s." % table)

if __name__ == "__main__":
    delete('staff', where={"id":"4%"})
