import mysql.connector
from connectdb import connect

def select(table=None, fields=None, where=None, limit=None, orderby=None):
    # fields = list
    # where = dict {'type': 'content'}
    # limit = int
    # orderby = field type(str)
    mydb = connect()
    cursor = mydb.cursor()

    if fields:
        fields = (',').join(fields)
    else:
        fields = '*'

    sql = "SELECT %s FROM %s" % (fields, table)

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

    if orderby:
        sql += " ORDER BY %s" % orderby

    if limit:
        sql += " LIMIT %s" % limit
    
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)

    result = cursor.fetchall()
    for x in result:
        print(x)

if __name__ == "__main__":
    select('staff', fields=["name"], orderby="name")
