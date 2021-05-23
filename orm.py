import mysql.connector
from cred import USER, PASSWORD

class DBError(Exception):
    TABLE_ERROR = "Table name not supplied, aborting"
    DB_ERROR = "Database name not supplied, aborting"

class MysqlORM():
    def __init__(self, dbname=None):
        if dbname:
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user=USER,
                    password=PASSWORD,
                    database=dbname,
                )
            except Exception as e:
                print(e)
        else:
            mydb = mysql.connector.connect(
                host="localhost",
                user=USER,
                password=PASSWORD,
            )

        self.mydb = mydb

    def createdb(self, dbname=None):
        if not dbname:
            raise DBError(DBError.DB_ERROR)
        sql = "CREATE DATABASE %s" % dbname
        cursor = self.mydb.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)

        #use
        self.usedb(dbname)

    def usedb(self, dbname=None):
        if not dbname:
            raise DBError(DBError.DB_ERROR)

        cursor = self.mydb.cursor()

        try:
            cursor.execute("USE %s" % dbname)
            print("Using %s database" % dbname)
        except Exception as e:
            print(e)

    def dropdb(self, dbname=None):
        if not dbname:
            raise DBError(DBError.DB_ERROR)
        
        cursor = self.mydb.cursor()
        
        # if within a db, need to change first.
        if self.mydb.database:
            cursor.execute("USE mysql")

        cursor.execute("DROP DATABASE %s" % dbname)
        print("%s database dropped" % dbname)

    def create_table(self, table_name=None, schema_dict=None):
        # checks if in a database first
        if not self.mydb.database:
            raise DBError(
                "Currently not using a database. Please use one first."
            )
        if self.mydb.database == 'mysql':
            raise DBError(
                "Please use or create another database before creating a table."
            )
        # checks for table name
        if not table_name:
            #raise DBError("Table name not supplied, aborting")
            raise DBError(DBError.TABLE_ERROR)

        if not schema_dict:
            raise DBError("Schema dictionary not supplied, aborting")

        cursor = self.mydb.cursor()
        #schema_dict should be in dictionary, with name as key and type as value

        schema_params = None
        for field in schema_dict:
            field_type = schema_dict[field]
            if not schema_params:
                schema_params = "%s %s" % (field, field_type)
            else:
                schema_params += ", %s %s" % (field, field_type)

        sql = "CREATE TABLE %s (%s)" % (table_name, schema_params)

        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)

    def drop_table(self, table_name=None):
        if not table_name:
            raise DBError(DBError.TABLE_ERROR)

        cursor = self.mydb.cursor()

        try:
            cursor.execute("DROP TABLE %s" % table_name)
            print("%s table dropped." % table_name)
        except Exception as e:
            print(e)


    def insert(self, table_name=None, fields=None, data=None):
        #data should be mysql standard datatypes and its rules
        if not table_name:
            raise DBError(DBError.TABLE_ERROR)

        if not fields:
            raise DBError("Fields list not supplied, aborting.")

        if not data:
            raise DBError(
                "Data list to be inserted not supplied, aborting."
            )

        cursor = self.mydb.cursor()

        field_list = None
        val_list = None
        for field in fields:
            if not field_list:
                field_list = field
                val_list = "%s"
            else:
                field_list += ", %s" % field
                val_list += ", %s"

        sql = "INSERT INTO %s (%s)" % (table_name, field_list)
        sql += " VALUES (%s)" % val_list

        try:
            cursor.executemany(sql, data)
            self.mydb.commit()
        except Exception as e:
            print(e)

        print(cursor.rowcount, "record(s) inserted.")

    def select(
        self, 
        table_name=None, 
        fields=None, 
        limit=None, 
        where=None, 
        orderby=None
    ):
        if not table_name:
            raise DBError(DBError.TABLE_ERROR)

        cursor = self.mydb.cursor()

        # fields supplied in a list
        field_query = None
        if not fields:
            field_query = '*'
        else:
            for field in fields:
                if not field_query:
                    field_query = field
                else:
                    field_query += ", %s" % field

        sql = "SELECT %s FROM %s" % (field_query, table_name)

        #where should be supplied in dict type: value, multiples supported
        #defaults to AND query
        if where:
            for lookup in where:
                if 'WHERE' in sql:
                    sql += " AND"
                else:
                    sql += " WHERE"
                sql += " %s = '%s'" % (lookup, where[lookup])

        if orderby:
            sql += " ORDER BY %s" % orderby

        if limit:
            sql += " LIMIT %s" % limit
        
        cursor.execute(sql)
        result = cursor.fetchall()
        for x in result:
            print(x)

    def delete(self, table_name=None, where=None):
        # where is a dictionary. See select. Accept single only
        if not table_name:
            raise DBError(DBError.TABLE_ERROR)

        if not where:
            raise DBError("Filter not supplied, aborting")

        if len(where) > 1:
            raise DBError("Please provide one query filter only")

        cursor = self.mydb.cursor()

        for query in where:
            sql = "DELETE FROM %s WHERE %s = " % (table_name, query)
            sql += "%s"
            target = (where[query], )

        cursor.execute(sql, target)
        self.mydb.commit()

        print(cursor.rowcount, "records(s) deleted")

    def update(self, table_name=None, where=None, setdata=None):
        # where and setdata dictionaries
        if not table_name:
            raise DBError(DBError.TABLE_ERROR)

        if not where:
            raise DBError("Filter not supplied, aborting")

        if len(where) > 1:
            raise DBError("Please provide one query filter only")

        if not setdata:
            raise DBError("No edit data supplied, aborting")

        cursor = self.mydb.cursor()

        sql = "UPDATE %s" % table_name
        
        for data in setdata:
            if 'SET' in sql:
                sql += ","
            else:
                sql += " SET"
            sql += " %s = " % data
            sql += "%s"

        for lookup in where:
            sql += " WHERE %s = " % lookup
        sql += "%s"

        # start val as list to append it
        val = []
        for value in setdata.values():
            val.append(value)

        val.append(where[lookup])

        #necessary to change to tuple to escape sql injection
        val = tuple(val)

        try:
            cursor.execute(sql, val)
            self.mydb.commit()
        except Exception as e:
            print(e)

        print(cursor.rowcount, "record(s) affected")


