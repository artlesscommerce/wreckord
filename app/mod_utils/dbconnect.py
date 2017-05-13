
import pymysql
def connection():
    conn = pymysql.connect(host="localhost",
                           user = "localuser",
                           passwd = "",
                           db = "mytables", autocommit = True    )
    c = conn.cursor()

    return c, conn
