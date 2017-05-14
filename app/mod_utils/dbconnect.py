
import pymysql

from varfuncs import conFunc
def connection():
    conn = pymysql.connect(host=    conFunc( 'dbhost' ),
                           user =   conFunc( 'dbuser' ),
                           passwd = conFunc( 'dbpasswd' ),
                           db =     conFunc( 'dbtable' ), autocommit = True    )
    c = conn.cursor()

    return c, conn
