from datetime import datetime
from time import sleep
import pymysql
import json
from app.mod_utils.varfuncs import conFunc

writeQueue     = []
lockTheTables  = False


def connection():
    conn = pymysql.connect(host=    conFunc( 'dbhost' ),
                           user =   conFunc( 'dbuser' ),
                           passwd = conFunc( 'dbpasswd' ),
                           db =     conFunc( 'dbtable' ) ) #,  autocommit = True    )
    c = conn.cursor()

    return c, conn


def readcon( q1, args ):
	try:
		c, conn = connection()
		c.execute( q1, args )
		
		return c

	except Exception as e:
		print(  'oo 29 ' + (str(e)), q1  )

	return None


def newRequest( username, parent_id, buttonType, dateNow ):
	print( 'newRequest         :', dateNow, username, buttonType )
	lastRow = 0
	try:
		q1 = 'insert into requestLog ( username, parent_id, buttonType, dateTime ) values ( %s, %s, %s, %s )'

		args2 = [ username, parent_id, buttonType, dateNow ]

		c, conn = connection()
		
		
		c.execute( q1, args2 )
		conn.commit()
		lastRow = c.lastrowid

	except Exception as e:
		print ( 'oo 64' + (str(e)) )
		return  "write error"

	return lastRow


def endRequest( requestId, argsVar, message, logic, write, dateNowLogic, dateNowWrite ):
	dateNow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	print( 'endRequest         :', dateNow, requestId, message, logic, write, dateNowLogic, dateNowWrite )
	try:
		q1  = 'update requestLog set args1 = %s, message1 = %s, logicStatus = %s, writeStatus = %s, logicTime = %s, '
		q1 += ' writeTime = %s, endTime = %s where id = %s '

		dateNow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
#		dateNow = strftime("%Y-%m-%d %H:%M:%S")
		args = [ argsVar, message, logic, write, dateNowLogic, dateNowWrite, dateNow, requestId ]

		c, conn = connection()
		c.execute( q1, args )
		conn.commit()

	except Exception as e:
		print ( 'oo 54' + (str(e)) )
		return  "write error"

	return 'okay'


def a2q( q1, args ):   # addToWriteQueue
	print( 'a2q---addToWriteQueue' )
	q1Args = { 'q1':q1, 'args':args }
	writeQueue.append( q1Args )


def writeToTables( requestId, username ):
	print( 'writeToTables      :', requestId, len( writeQueue ) )
	
	c, conn = connection()
	for x in writeQueue:
		var1 = writeQuery( c, conn, requestId, username, x['q1'], x['args'] )
		if var1 != 'write okay':
			return 'write error'
	
	conn.commit();
	writeQueue.clear()
	
	print( 'writeToTables exit :', str( requestId ) )
	return 'okay'


def lockTables():
	print( 'lockTables' )
	if lockTheTables == False:
		return 'okay'

	count = 0
	while getLocked() != 'false':
		print ( 'lockTables count : ', count )
		count = count + 1
		sleep(0.1) # Time in seconds.
		if count == 20:
			return 'timed out'
	print ( 'lockTables ... : ' )
	setLocked('true')
	return 'okay'


def unLockTables():
	print( 'unLockTables' )
	setLocked( 'false' )


def getLocked():
	'returns writelock value'
	try:
		c, conn = connection()
		q1 = 'select theValue from valuepairs where thekey = %s '
		c.execute( q1 , 'writeLock'  )
		row = c.fetchone()
		
		if row is not None:
			return row[0]
		else:
			return 'error'
	except Exception as e:
		print( str(e) )


def setLocked( strLocked ):
	'set writelock to true'
	try:
		c, conn = connection()
		q1 = 'update valuepairs set thevalue = %s where thekey = %s '
		c.execute( q1 , ( strLocked, 'writeLock'  ) )

	except Exception as e:
		print( str(e) )


def tableLockNotice( noticeMessage, message = '' ):
	print( 'tableLockNotice ', noticeMessage, message  )


def writeQuery( c, conn, requestId, username, q1, args ):
	print( 'writeQuery         :' , q1,  requestId ) #args,

	try:
#		c, conn = connection()
		c.execute( q1, args )
#		conn.commit();
		return addToQueryLog( c, conn, requestId, username, q1, args )

	except Exception as e:
		print ( 'oo 93' + (str(e)) )
		return  "write error"

	return  "write okay"


def addToQueryLog( c, conn, requestId, username, query1, args ):
	print( 'addToQueryLog      :' , requestId, ':', username, query1,  ) #args

	try:
		q1 = 'insert into writeLog ( request_id, username, query1, args1, dateTime ) values ( %s, %s, %s, %s, %s )'
		dateNow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
		args2 = [ requestId, username, query1, str( args ), dateNow ]
#		c, conn = connection()
		c.execute( q1, args2 )
		return  "write okay"

	except Exception as e:
		print ( 'oo 155 :' + (str(e)) )
		return  "write error"



def getAutoIncrement( tableName ):
	q1 = '''
	SELECT `AUTO_INCREMENT`
	FROM  INFORMATION_SCHEMA.TABLES
	WHERE TABLE_SCHEMA = 'dbschema'
	AND   TABLE_NAME   = %s ;
	'''
	c = readcon( q1, [ tableName ] )
	row = c.fetchone()
	if row is not None:
		return row[0]
	return 0


