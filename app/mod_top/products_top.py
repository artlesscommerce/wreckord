from flask import request, session
import json

from app.mod_utils.utils_one import areBadStrings

from app.mod_products.products_one import productInfo
from app.mod_products.products_one import getBalance	
from app.mod_products.products_one import getBalanceAll	
from app.mod_products.products_one import sendAmount
from app.mod_products.products_one import getSendRecLog

from app.mod_products.products_one import prNameToId
from app.mod_products.products_one import addProduct

from app.mod_auth.auth_one import userNameToId


def productPageButton():
	varpr1 = request.form['jsvar1']

	badStrings = [ [ 'product', varpr1, False ] ]
	theRes = areBadStrings( badStrings )

	if theRes != False:
		return json.dumps( { 'username':session['username'], 'errMessage':theRes } )

	s1 = productInfo( varpr1 )
	
	s1['username'] = session['username']
	
	s0j = json.dumps(s1)
	return s0j


def balanceButton():
	s1 = getBalanceAll( session['user_id'] )
	s1['username'] = session['username']
	
	s0j = json.dumps(s1)
	return s0j


def sendAmountButton(  args ):
	username = session['username']

	userTo  = args[0]
	product = args[1] 
	amount  = args[2] 

	badStrings = []
	badStrings.append( [ 'username', userTo  ] )
	badStrings.append( [ 'product',  product ] )
	badStrings.append( [ 'posInt',   amount  ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return  [ 'logic ok', 'bad arg strings', '', { 'username':username, "errMessage":theRes } ]

	product_id = prNameToId( product )

	userBal = getBalance(  session['user_id'], product_id )
	userAvailableVar1 = int( userBal['available'] )
	
	user2_id = userNameToId( userTo )

	s1 = sendAmount( session['user_id'], user2_id, product_id, amount, userAvailable = userAvailableVar1 )
	
	if s1[0] == 'logic ok':
		if s1[1] == 'amount sent':
			s0 = [ 'logic ok', s1[1], json.dumps( args ), { 'username':username, 'okMessage':s1[1] } ]
			return s0
		s0 = [ 'logic ok', s1[1], json.dumps( args ), { 'username':username, 'errMessage':s1[1] } ]
		return s0
	return s1


def sendAmountButtonNew( args ):   # _id
	username = session['username']

	user1_id  = args[0]     # From
	user2_id  = args[1]     # To
	product_id  = args[2] 
	amount    = args[3] 
	sendSort  = args[4] 

	badStrings = []
	badStrings.append( [ 'posInt',  user1_id   ] )
	badStrings.append( [ 'posInt',  user2_id   ] )
	badStrings.append( [ 'posInt',  product_id ] )
	badStrings.append( [ 'posInt',  amount     ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return  [ 'logic ok', 'bad arg strings', '', { 'username':username, "errMessage":theRes } ]

	userBal = getBalance(  user1_id, product_id )
	userAvailableVar1 = int( userBal['available'] )

	s1 = sendAmount( user1_id, user2_id, product_id, amount, userAvailable = userAvailableVar1 )
	
	if s1[0] == 'logic ok':
		if s1[1] == 'amount sent':
			s0 = [ 'logic ok', s1[1], json.dumps( args ), { 'username':username, 'okMessage':s1[1] } ]
			return s0
		s0 = [ 'logic ok', s1[1], json.dumps( args ), { 'username':username, 'errMessage':s1[1] } ]
		return s0
	return s1



def sendAmountFormButton():
	username = session['username']
	
	varpr1 = request.form['jsvar1']
	varTo = request.form['jsvar2']
	print ( varpr1 )
	
	s1 = {}
	if varpr1 != '':
		badStrings = [ [ 'product', varpr1, False ] ]
		theRes = areBadStrings( badStrings )

		if theRes != False:
			return json.dumps( { 'username':session['username'], 'errMessage':theRes } )

		s2 = getBalance( userNameToId( username ), prNameToId( varpr1 ) )
		s2['product'] = varpr1
		s1['balance'] = s2

	s1['userTo'] = varTo
	s1['username'] = username
		
	return json.dumps(s1)


def sendRecLogButton():
	username = session['username']

	startfrom = request.form['jsvar1']
	results   = request.form['jsvar2']
	user2     = request.form['jsvar3']
	prList    = request.form['jsvar4']

	
	badStrings = []
	if user2 != '':		
		badStrings.append( [ 'username', user2, False ] )

	if startfrom == '':
		startfrom = '0'
	else:
		badStrings.append( [ 'posInt', startfrom ] )

	if results == '':
		results = '10'
	else:
		badStrings.append( [ 'posInt', results ] )

	productList = []
	if prList != '':		
		productList = prList.split( '-' )
		for x in productList:
			badStrings.append( [ 'product', x ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return json.dumps( { 'username':session['username'], 'errMessage':theRes } )

	s1 = getSendRecLog( startfrom, results, username, user2, productList )
#	s1 = getSendRecLog( '', '', '', '', ''  )
	s1['username'] = username

	return json.dumps(s1)


def addProductButton( args ):
	prName = args[0]
	prDesc = args[1]
	prCrea = args[2]
	user_id = userNameToId( args[2] )

	var1 = addProduct( prName, prDesc, user_id )
	username = session.get( 'username', '' )
	s0 = [ 'logic ok', var1, json.dumps( args ), { 'username':username, 'okMessage':var1[1] } ]
	return s0

	
