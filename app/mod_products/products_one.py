from time import strftime
from datetime import datetime

from app.mod_utils.dbconnect import readcon
from app.mod_utils.dbconnect import a2q

from app.mod_auth.auth_one import userExists


maxLimit = 500000


def addProduct( product, description ):
	"add a new product"
	try:
		var1 = productExists( product )
		if var1 != 'no product':
			return 'product is not free'
		dateNow = strftime("%Y-%m-%d %H:%M:%S")
		q1  = 'INSERT INTO products1 ( productName, detail, dateTime ) VALUES ( %s, %s, %s )'
		args = [ product, description, dateNow ]
		a2q( q1, args )
		return 'product added'

	except Exception as e:
		print ( 'oo 27' + (str(e)) )
		return 'error'


def productExists( product ):
	try:
		q1 = "SELECT uniqueX, status1 FROM products1 WHERE productName = %s "
		args = [ product ]
		c = readcon( q1, args )
		fo = c.fetchone()
		if fo == None:
			return 'no product'
		if fo[1] == 'okay':
			return 'product is okay'
		return 'product is ' + str( fo[1] )

	except Exception as e:
		print ( 'oo' + (str(e)) )
		return 'error'


def getProductsUserList( username ):
	return [ username + '.mbtc', username + '.euro' ]


def getProductsBlankList( username ):
	return [ 'mbtc', 'euro' ]


def getProductsOtherList( username ):
	myList = []
	q1 = 'select product from scores1 where who1 = %s '
	args = [ username ]
	try:
		c = readcon( q1, args )
		row = c.fetchone()
		while row is not None:
			crpr = splitCr1Pr1( row[0] )
			if crpr[0] != username:
				myList.append( row[0] )
			row = c.fetchone()

	except Exception as e:
		print ( 'oo 65 ' + (str(e)) )
		return 'error'

	return myList	
	

def getBalanceAll( username ):
	print ( 'get balance' )
	userList  = getProductsUserList( username )
	blankList = getProductsBlankList( username )
	otherList = getProductsOtherList( username )

	uList = getBalanceOfList( username, userList  )
	bList = getBalanceOfList( username, blankList )
	oList = getBalanceOfList( username, otherList )

	return { 'userList':uList, 'blankList':bList, 'otherList':oList }


def getBalanceOfList( username, productList ):
	myList = []
	print ( productList )
	for x in productList:
		y = getBalance( username, x )
		y['product'] = x
		myList.append( y )
	return myList


def productInfo( productName ):
	q1 = 'select detail, datetime from products1 where productName = (%s) and status1 = "okay" '
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



def getBalance( user, product):
	cr1pr1 = splitCr1Pr1( product )
	available = 0
	inuse     = 0
	
	exists = productExists( product )
	if exists != 'product is okay':
		myList = { 'message':exists }
		return { 'message':exists } #myList
	
	myList = {}
	try:
		q1 = 'select amount from scores1 where who1 = %s and product = %s '
		args = [ user, product ]

		c = readcon( q1, args )
		row = c.fetchone()
		if row is not None:
			amount = row[0]
			if cr1pr1[0] == user:
				available = maxLimit - amount
				inuse     = amount
			else:
				available = amount

		else:
			if cr1pr1[0] == user:
				available = maxLimit
				inuse     = 0
		myList[ 'message' ] = 'okay' # 'product does not exist'
		myList[ 'available' ] = available
		myList[ 'in use' ]    = inuse
		
	except Exception as e:
		print( 'oo 114; ' +   (str(e)) )
		return 'error'

	return myList 


def getCanPay( user, product, amount ):
	var1 = getBalance(user, product) ['available']
	if int( var1 ) < int( amount ):
		return False
	
	return True


def sendAmount( user, userTo, product, amount, sendSort = 'ordinary' ):
	print( 'sendAmount         :', user, product, amount, sendSort )

	if user == userTo:
		return [ 'logic ok', 'users are the same' ]

	
	exists1 = productExists( product )
	if exists1 != 'product is okay':
		return [ 'logic ok', exists1 ]


	exists1 = userExists( userTo )
	if exists1 != True:
		return [ 'logic ok', exists1 ]
		
	
	var1 = getCanPay( user, product, amount )

	varAvail = getBalance(user, product) ['available']
	if int( varAvail ) < int( amount ):
		print( 'cant insufficient funds', int( varAvail ) , int( amount ) )
		return [ 'logic ok', 'insufficient funds' ]

	varRecer = getBalance(userTo, product) ['available']

	newVarAvail = int( varAvail ) - int( amount )
	newVarRecer = int( varRecer ) + int( amount )

	print ( 'canPayaaa:',  newVarAvail,  newVarRecer )

	# newVarAvail update / create / delete
	cr1 = splitCr1Pr1( product )[0]
	if cr1 == user:
		newVarAvail = maxLimit - newVarAvail

	updateScoresRow( newVarAvail, user, product )
	
	# newVarRecer update / create / delete
	cr2 = splitCr1Pr1( product )[0]
	if cr2 == userTo:
		newVarRecer = maxLimit - newVarRecer
	
	updateScoresRow( newVarRecer, userTo, product )

	# add to send rec log 
	# user userTo, product amount sendsort, dateNow

	addToSendRecLog( user, userTo, product, amount, sendSort )

	print ( 'canPayzzzz:',  newVarAvail,  newVarRecer )
	
	return [ 'logic ok', 'amount sent' ]


def updateScoresRow( newVar, user, product ):
	if newVar == 0:
		# sales inTrade maybe ok
		q1 = 'delete from scores1 where who1 = %s and product = %s'
		args = [ user, product ]
	else:  # newVarAvail > 0
		q2 = 'select uniqueX from scores1 where who1 = %s and product = %s'
		args2 = [ user, product ]
		try:
			c = readcon( q2, args2 )
			row = c.fetchone()
			if row is not None:
				q1 = 'update scores1 set amount = %s  where who1 = %s and product  = %s'
				args = [ newVar, user, product ]
			else:
				q1 = 'insert into scores1 ( who1, product, amount )  values ( %s, %s, %s )'
				args = [ user, product, newVar ]
		except Exception as e:
			print( 'oo 223 ; ' +   (str(e)) )
			return 'error'

	a2q( q1, args )


def addToSendRecLog( user, userTo, product, amount, sendSort ):
	print( 'addToSendRecLog    :', user, userTo, product, amount, sendSort )
	dateNow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

	q1 = 'insert into sendRecLog ( user, userTo, product, amount, sendSort, dateTime )  values ( %s, %s, %s, %s, %s, %s )'

	args = [ user, userTo, product, amount, sendSort, dateNow ]
	a2q( q1, args )
#	getSendRecLog( '', '', '', '' )


def getSendRecLog( startfrom, results, user1, user2, productList ):
	print ( 'getSendRecLog', startfrom, results, user1, user2, productList )
	q1 = 'select user, userTo, product, amount, sendSort, dateTime from sendRecLog '
	q2 = 'select uniqueX from sendRecLog '
	
	print ( productList )

	argExts = []
	args = []

	if user1 != '':
		argExts.append( ' ( user = %s or userTo = %s ) ' )
		args.append( user1 )
		args.append( user1 )
		
	if user2 != '':
		argExts.append( ' ( sendSort = "ordinary" and ( ( user = %s and userTo = %s ) or ( userTo = %s and user = %s ) ) ) ' )
		args.append( user1 )
		args.append( user2 )
		args.append( user2 )
		args.append( user1 )
		
	if len( productList ) > 0:
		argExts.append( ' ( product in %s ) ' )
		args.append( productList )

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
	q1 += ' order by dateTime desc, uniqueX desc limit %s, %s '
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




'''
add product 
productExists
productInfo
get list of users own products
get list of users others products
get balance
send product

add to sendreclog
getsendrec log 0 10 user1 user2 [listofprds]

'''

#productInfo55()
#print( getProductsOtherList( 'z1' ) )
#print( getBalanceAll( 'z1' ) )
