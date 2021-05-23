import mysql.connector
from connectdb import connect

def insert(table=None, fields=None, data=None):
    # table = str
    # fields = list
    # data = list of tuples
    mydb = connect()
    cursor = mydb.cursor()

    # the number of substitutions equal to fields
    val_list = []
    for x in fields:
        val_list.append("%s")

    # joining up the fields
    fields = (',').join(fields)

    sql = "INSERT INTO %s (%s) VALUES " % (table, fields)
    sql += "(%s)" % (',').join(val_list)

    try:
        cursor.executemany(sql, data)
        mydb.commit()
        print(cursor.rowcount, "record(s) inserted into %s." % table)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    insert('staff', fields=['name', 'id'], data=[('Amin',100), ('Suresh',102), ('Lee',433)])
