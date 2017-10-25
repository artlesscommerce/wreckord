from time import strftime
from datetime import datetime

from app.mod_utils.dbconnect import readcon
from app.mod_utils.dbconnect import a2q
from app.mod_utils.dbconnect import getAutoIncrement

from app.mod_auth.auth_one import userExists
from app.mod_auth.auth_one import userExists_id
from app.mod_auth.auth_one import userNameToId
from app.mod_auth.auth_one import userIdToName

maxLimit = 500000


def addProduct( product, description, productCreator = '0' ):
	"add a new product"
	try:
		var1 = productExistsName( product )
		if var1 != 'no product':
			return 'product is not free'
		dateNow = strftime("%Y-%m-%d %H:%M:%S")

		q1  = 'INSERT INTO product ( user_id, name, detail, dateTime ) VALUES ( %s, %s, %s, %s )'
		args = [ productCreator, product, description, dateNow ]
		a2q( q1, args )
		return 'product added'

	except Exception as e:
		print ( 'oo 27' + (str(e)) )
		return 'error'


def productExists( prId ):
	print ( 'pr exists', prId  )
	try:
		q1 = "SELECT status1 FROM product WHERE id = %s "
		c = readcon( q1, [ prId ] )
		fo = c.fetchone()
		if fo == None:
			return 'no product'
		if fo[0] == 'okay':
			return 'product is okay'
		return 'product is ' + str( fo[0] )

	except Exception as e:
		print ( 'oo' + (str(e)) )
		return 'error'


def productExistsName( prName ):
	print ( 'pr exists name', prName  )
	try:
		q1 = "SELECT status1 FROM product WHERE name = %s "
		c = readcon( q1, [ prName ] )
		fo = c.fetchone()
		if fo == None:
			return 'no product'
		if fo[0] == 'okay':
			return 'product is okay'
		return 'product is ' + str( fo[0] )

	except Exception as e:
		print ( 'oo' + (str(e)) )
		return 'error'


def getProductsUserList( user_id ):
	# select all from product where user_id = user_id
	username = userIdToName( user_id )
	pr1 = prNameToId( username + '.mbtc' )
	pr2 = prNameToId( username + '.euro' )
	return [ pr1, pr2 ]


def getProductsBlankList():
	# select all from product where user_id = 0
	return [ 1, 2 ]
#	return [ 'mbtc', 'euro' ]


def getProductsOtherList( user_id ):
	myList = []
	q1 = 'select product_id from score where user_id = %s '
	args = [ user_id ]
	try:
		c = readcon( q1, args )
		row = c.fetchone()
		while row is not None:
			crpr = getPrCrId( row[0] )
#			crpr = splitCr1Pr1( row[0] )
			if int( crpr ) != int( user_id ):
				if int( crpr ) != 0:
					myList.append( row[0] )
			row = c.fetchone()
				myList.append( row[0] )
			row = c.fetchone()

	except Exception as e:
		print ( 'oo 65 ' + (str(e)) )
		return 'error'

	return myList	
	

def getBalanceAll( user_id ):
	print ( 'get balance' )
	userList  = getProductsUserList(  user_id )
	blankList = getProductsBlankList()
	otherList = getProductsOtherList( user_id )

	uList = getBalanceOfList( user_id, userList, int(user_id)  )
	bList = getBalanceOfList( user_id, blankList, 0  )
	oList = getBalanceOfList( user_id, otherList )

	return { 'userList':uList, 'blankList':bList, 'otherList':oList }



def getBalanceOfList( user_id, productList, prCrId = None ):
	print ( 'qqq', productList ) # productList in id
	myList = []
	print ( productList )
	for x in productList:
		if prCrId == None:
			prCrId2 = getPrCrId( x )
			y = getBalance( user_id, x, prCrId2 )
		else:
			y = getBalance( user_id, x, prCrId )
		y['product'] = prIdToName( x )
		myList.append( y )
	return myList


# change 
def productInfo( productName ):
	q1 = 'select detail, datetime from product where name = (%s) and status1 = "okay" '
	args = [ productName ]
	try:
		c = readcon( q1, args )
		row = c.fetchone()
		if row is not None:
			cr1pr1 = splitCr1Pr1( productName )
			myList2 = { 'message':'okay', 'cr1':cr1pr1[0], 'pr1':cr1pr1[1], 'description':str(row[0]), 'dateTime':str(row[1]) }
			return myList2
		return { 'message':'not found' }
	except Exception as e:
		print( 'oo 64; ' +   (str(e)) )
		return { 'message':'error' }


def splitCr1Pr1( product ):
	cr1 = ''
	pr1 = ''
	varr = product.split( '.' )
	if len(varr) == 2:
		cr1 = varr[0]
		pr1 = varr[1]
		
	if len(varr) == 1:
		pr1 = varr[0]
	return [ cr1, pr1 ]


def getPrCrId( idPr ):
	print('zxc')
#	return '10'
	q1 = 'SELECT user_id FROM product where id = %s'
	c = readcon( q1, [ idPr ] )
	row = c.fetchone()
	if row is not None:
		return row[0]
	return 0



def getBalance( user_id, product_id, prCrId = None ):
	print ( 'getBalance ', user_id, product_id, prCrId )

	available = 0
	inuse     = 0
	total     = 0
	inTrade   = 0
	
	if prCrId == None:
		prCrId = getPrCrId( product_id )
	
	exists = productExists( product_id )
	if exists != 'product is okay':
		print ( exists )
		return { 'message':exists }
	
	myList = {}
	try:
		q1 = 'select amount from score where user_id = %s and product_id = %s '
		args = [ user_id, product_id ]

		c = readcon( q1, args )
		row = c.fetchone()
		if row is not None:
			amount  = row[0]
			if int( prCrId ) == int( user_id ):
				available = maxLimit - amount
				inuse     = amount
			else:
				available = amount

		else:
			if int( prCrId ) == int( user_id ):
				available = maxLimit
				inuse     = 0

		myList[ 'message' ] = 'okay'
		myList[ 'available' ] = available
		myList[ 'in use' ]    = inuse
		
	except Exception as e:
		print( 'oo 114; ' +   (str(e)) )
		return 'error'

	return myList


def getCanPay( user_id, product_id, amount ):
	var1 = getBalance( user_id, product_id ) ['available']
	if int( var1 ) < int( amount ):
		return False
	
	return True


def prNameToId( pr1 ):
	q1 = 'SELECT id FROM product where name = %s'
	c = readcon( q1, [ pr1 ] )
	row = c.fetchone()
	if row is not None:
		return row[0]
	return 0


def prIdToName( pr_id ):
	q1 = 'SELECT name FROM product where id = %s'
	c = readcon( q1, [ pr_id ] )
	row = c.fetchone()
	if row is not None:
		return row[0]
	return 0


def sendAmount( user1_id, user2_id, product_id, amount, sendSort = 'ordinary', userAvailable = None ):
	print( 'sendAmountNew ::', user1_id, user2_id, product_id, amount, sendSort, userAvailable )
	if user1_id == user2_id:
		return [ 'logic ok', 'users are the same' ]
	exists1 = productExists( product_id )
	if exists1 != 'product is okay':
		return [ 'logic ok', exists1 ]
	exists1 = userExists_id( user2_id )
	if exists1 != True:
		return [ 'logic ok', exists1 ]
	prCrId = getPrCrId( product_id )
	if userAvailable == None:
		userBal = getBalance( user1_id, product_id )
		userAvailable = int( userBal['available'] )
	if int( userAvailable ) < int( amount ):
		print( 'cant insufficient funds', int( userAvailable ) , int( amount ) )
		return [ 'logic ok', 'insufficient funds' ]
	varRecer = getBalance( user2_id, product_id )['available']
	newVarTotal = int( userAvailable ) - int( amount )
	newVarRecer = int( varRecer ) + int( amount )
	if prCrId == user1_id:
		newVarTotal = maxLimit - newVarTotal
	updateScoresRow( newVarTotal, user1_id, product_id )
	if prCrId == user2_id:
		newVarRecer = maxLimit - newVarRecer
	updateScoresRow( newVarRecer, user2_id, product_id )
	addToSendRecLog( user1_id, user2_id, product_id, amount, sendSort )
	return [ 'logic ok', 'amount sent' ]


def updateScoresRow( newVar, userId, idPr ):
	if newVar == 0:
		# sales inTrade maybe ok
		q1 = 'delete from score where user_id = %s and product_id = %s'
		args = [ userId, idPr ]
	else:  # newVarAvail > 0
		q2 = 'select id from score where user_id = %s and product_id = %s'
		args2 = [ userId, idPr ]
		try:
			c = readcon( q2, args2 )
			row = c.fetchone()
			if row is not None:
				q1 = 'update score set amount = %s  where user_id = %s and product_id  = %s'
				args = [ newVar, userId, idPr ]
			else:
				q1 = 'insert into score ( user_id, product_id, amount )  values ( %s, %s, %s )'
				args = [ userId, idPr, newVar ]
		except Exception as e:
			print( 'oo 223 ; ' +   (str(e)) )
			return 'error'

	a2q( q1, args )


def addToSendRecLog( user, userTo, product_id, amount, sendSort ):
	print( 'addToSendRecLog    :', user, userTo, product_id, amount, sendSort )
	dateNow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

	q1 = 'insert into sendRecLog ( user1_id, user2_id, product_id, amount, sendSort, dateTime )  values ( %s, %s, %s, %s, %s, %s )'

	args = [ user, userTo, product_id, amount, sendSort, dateNow ]
	a2q( q1, args )
#	getSendRecLog( '', '', '', '' )


def getSendRecLog( startfrom, results, user1, user2, productList ):
	print ( 'getSendRecLog', startfrom, results, user1, user2, productList )
	
	q1 = '''
	SELECT u1.name as userFrom, u2.name as userTo, product.name,
	amount, sendSort, sendRecLog.dateTime
	FROM sendRecLog 
	INNER JOIN user u1 ON user1_id = u1.id 
	INNER JOIN user u2 ON user2_id = u2.id 
	INNER JOIN product ON product_id = product.id
	'''

	q2 = '''
	SELECT sendRecLog.id
	FROM sendRecLog
	INNER JOIN user u1 ON user1_id = u1.id 
	INNER JOIN user u2 ON user2_id = u2.id 
	INNER JOIN product ON product_id = product.id
	'''

	print ( productList )

	argExts = []
	args = []

	if user1 != '':
		argExts.append( ' ( u1.name = %s or  u2.name = %s  ) ' )
		args.append( user1 )
		args.append( user1 )
	
	extStr = ' where '
	count = 0

	for x in argExts:
		extStr +=  ' ' + x
		count = count + 1
		if count < len( argExts ):
			extStr += ' and '
		if count == len( argExts ):
			print ( 'azaza', q1,  extStr )
			q1 +=  extStr
			q2 +=  extStr

	print ( 'exstr', extStr )
	print ( 'q1   ', q1 )
	print ( 'args ', args )

	args2 = list(args)

	q1 += ' order by sendRecLog.dateTime desc, sendRecLog.id desc'
	q1 += '  limit %s, %s '
	args.extend( [ int( startfrom ), int(results) ] )

	try:
		c = readcon( q2, args2 )
		myRowCount2 = c.rowcount
		print( 'myRowCount2', myRowCount2 )

		myList = []
		c = readcon( q1, args )
#		myRowCount = c.rowcount
		row = c.fetchone()
		while row is not None:
			row2 = {}
			sentRecvd = 'received from'
			if user1 == row[0]:
				sentRecvd = 'sent to'

			userToVar = row[1]
			if row[4] != 'ordinary':
				userToVar = row[4]
			
			row2['user'    ] = row[0]
			row2['userTo'  ] = userToVar
			row2['product' ] = row[2]
			row2['amount'  ] = row[3]
			row2['sentRecvd'] = sentRecvd
			row2['sendSort'] = row[4]
			row2['dateTime'] = str( row[5] )
			myList.append( row2 )
			row = c.fetchone()

		return { 'rows':myList, 'allRows':myRowCount2, 'startfrom':startfrom, 'results':results, 'userTo':user2, 'products':productList }

	except Exception as e:
		print( 'oo 223 ; ' +   (str(e)) )
		return { 'qqqq': 'error'}

