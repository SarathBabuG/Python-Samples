import sys, json, base64
import MySQLdb

db_host   = "localhost"
db_name   = "database"
db_user   = "user"
db_passwd = "password_base64_encrypted"

dbconn = None

def cursorFilter(func):

    def wrapper(*args, **kwargs):
        global dbconn
        if not dbconn:
            ''' Create the database connection only once '''
            dbconn = MySQLdb.connect(host = db_host, user = db_user, passwd = base64.decodestring(db_passwd), db = db_name)

        try:
            cursor = dbconn.cursor()
            try:
                result = func(cursor, *args, **kwargs)
            finally:
                cursor.close()
            dbconn.commit()
        except:
            dbconn.rollback()
            raise
        return result
    return wrapper


@cursorFilter
def execute_query(cursor, query, *args):
    try:
        cursor.execute(query, (args))
        if query.lower().startswith("select"):
            return cursor.fetchall()
        return True
    except Exception, emsg:
        print "execute_query error: %s" % (emsg)
        return False


execute_query("select * from sample;")
