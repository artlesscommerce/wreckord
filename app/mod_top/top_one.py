from flask import Flask, jsonify, Blueprint, request, render_template, session, redirect, url_for

import json
from random import randint
from datetime import datetime
from time import strftime
import time

from app.mod_auth.auth_one import changePassword
from app.mod_auth.auth_one import closeUser
from app.mod_auth.auth_one import userInfo
from app.mod_auth.auth_one import listUsers
from app.mod_auth.auth_one import addUser
from app.mod_utils.utils_one import areBadStrings
from app.mod_utils.dbconnect import newRequest
from app.mod_utils.dbconnect import endRequest
from app.mod_utils.dbconnect import a2q
from app.mod_utils.dbconnect import writeToTables
from app.mod_utils.dbconnect import lockTables
from app.mod_utils.dbconnect import unLockTables
from app.mod_utils.dbconnect import tableLockNotice
from app.mod_utils.varfuncs import conFunc

# top_one pastepoint 1
from app.mod_locat.locat_one import setLocation
from app.mod_locat.locat_one import getLocation
from app.mod_products.products_one import productInfo
from app.mod_products.products_one import addProduct
from app.mod_products.products_one import getBalance
from app.mod_products.products_one import getBalanceAll
from app.mod_products.products_one import sendAmount
from app.mod_products.products_one import getSendRecLog

mod_top = Blueprint('top', __name__ )


def topit():
	if 'username' in session:
		print ( 'in session : ',session['username'] )
		var = randint( 100, 10100 )
		var = '?v=' + str( var )#'localq'
		return render_template('top/loggedin.html', mycssfile=session['cssStyle'], sitename=conFunc( 'sitename' ),\
		name=session['username'], random=var )
	print ( 'not in session' )
	session.clear()
	return render_template('top/loggedout.html', sitename= conFunc( 'sitename' ) )


@mod_top.route('/about/', methods=['GET'])
def about1():
	return render_template('top/about.html' )



@mod_top.route('/input/', methods=[ 'POST', 'GET'])
def input1():
	if 'username' in session:
		if 'logged_in' in session:
			if session['logged_in'] == True :
				if request.method == 'POST':
					print( 'newpost', session['username'] )
					return ajax()

				if request.method == 'GET':
					return render_template('top/inputapi.html' )
	return 'not logged in'



@mod_top.route('/newuser2', methods=['POST'])
def newuser2():
	username = request.form['jsvar1'].lower()
	password1 = request.form['jsvar2']
	password2 = request.form['jsvar3']

	args = [ username, password1, password2 ]
	
	var = ajaxWrite( 'addUser', 'unknown', args )

	return var #json.dumps( { 'newMessage':var } )


@mod_top.route('/ajax/', methods=['POST'])
def ajax():
	buttonType = 'blank'
	try:
		buttonType = request.form['buttontype']
	except Exception as e:
		print( 'oo ' + (str(e)) )

	print ('\ntop ajax', buttonType )

	logged_in_var = False

	if 'username' in session:
		if 'logged_in' in session:
			if session['logged_in'] == True :
				logged_in_var = True

	if logged_in_var != True:
		session.clear()
		return 'not_logged_in!'

	writeReqs = [ 'changePassButton', 'closeUserButton' ]
	# top_one pastepoint 2
	writeReqs.append( 'newLocation' )
	writeReqs.append( 'sendAmount' )
	
	if buttonType in writeReqs:
		return ajaxWrite( buttonType, session['username'] )

	if buttonType == 'testme':
		return json.dumps( {'username':session['username'], 'errMessage':'yay' } )
	if buttonType == 'testyu':
		return json.dumps( {'username':session['username'], 'okMessage':'huh' } )
	if buttonType == 'listUsers':
		return listUsersButton()
	if buttonType == 'userInfo':
		return userInfoButton()
	if buttonType == 'colours':
		return colours()
	# top_one pastepoint 7
	if buttonType == 'productPage':
		return productPageButton()
	if buttonType == 'balance':
		return balanceButton()
	if buttonType == 'sendAmountForm':
		return sendAmountFormButton()
	if buttonType == 'sendRecLog':
		return sendRecLogButton()

	return json.dumps( {'username':session['username'], } )
#	return json.dumps( {'username':session['username'], 'errMessage':'badButtonType' + buttonType } )


def ajaxWrite( buttonType, username, args = None ):
	print ( 'ajaxWrite' )
	lockVar = lockTables()
	
	if lockVar != 'okay':
		return json.dumps( { 'username':username, 'errMessage':'table is locked' } )

	
	if args == None:
		args = getArgs()
	
	dateNow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	dateNowLogic = '0'
	dateNowWrite = '0'
	message = ''
	
	
	requestId = newRequest( username, buttonType, dateNow )
	
	if requestId < 1:
		return json.dumps( { 'username':username, 'errMessage':'error' } )

	timerVar1 = int(round(time.time() * 1000))

	if buttonType == 'addUser':
		var1 = addUserButton( args )
	if buttonType == 'changePassButton':
		var1 = changePassButton( args )
	if buttonType == 'closeUserButton':
		var1 = closeUserButton( args )
	# top_one pastepoint 3
	if buttonType == 'newLocation':
		var1 = newLocationButton( args )
	if buttonType == 'sendAmount':
		var1 = sendAmountButton( args )

	timerVar2 = int(round(time.time() * 1000))

	dateNowLogic = str( timerVar2 - timerVar1 )

	if var1[0] == 'logic ok':
		message = var1[1]
		args2   = var1[2]
		jsonVar = var1[3]

		timerVar1 = timerVar2
		writeVar = writeToTables( requestId, username )
		timerVar2 = int(round(time.time() * 1000))
		dateNowWrite = str( timerVar2 - timerVar1 )

		if writeVar == 'okay':
			endRequest( requestId, args2, var1[1], 'pass', 'pass', dateNowLogic, dateNowWrite )
			unLockTables()
			return jsonVar
		else:
			endRequest( requestId, args2, var1[1], 'pass', 'fail', dateNowLogic, dateNowWrite )
			tableLockNotice( 'bad write', writeVar )
			return 'error'
	else:
		endRequest( requestId, '', message, 'fail', 'false', dateNowLogic, dateNowWrite )
		print ( var1 )
		tableLockNotice( 'bad logic', var1 )
		return 'error'


def getArgs():
	"This returns jsvars"
	varr = []
	varr.append( request.form['jsvar1'] )
	varr.append( request.form['jsvar2'] )
	varr.append( request.form['jsvar3'] )
	varr.append( request.form['jsvar4'] )
	varr.append( request.form['jsvar5'] )
	
	return varr
	

def userInfoButton():
	"This returns current user information"

	varuser = request.form['jsvar1']

	badStrings = [ [ 'username', varuser, False ] ]
	theRes = areBadStrings( badStrings )

	if theRes != False:
		return json.dumps( {'username':username, 'errMessage':theRes } )

	s1 = userInfo( varuser )
	# top_one pastepoint 4
	s1['location'] = getLocation( varuser )
	
	s1['username'] = session['username']
	
	s0j = json.dumps(s1)
	return s0j


def listUsersButton():
	"This returns list of users"

	s1 = listUsers()

	s1['username'] = session['username']

	s0j = json.dumps(s1)
	return s0j


def closeUserButton( args ):
	username = session['username']

	s0 = [ 'logic ok', 'user not closed', json.dumps( { 'username':username, "okMessage":'user not closed' } ) ]
	return s0
# skip logic
	pw1 = request.form['jsvar1']

	badStrings = [ [ 'password', pw1 ] ]
	theRes = areBadStrings( badStrings )
	if theRes != False:
		return json.dumps( { 'username':username, 'errMessage':theRes } )

	s1 = closeUser( username, pw1 )

	if s1[0] == "okay":
		s0 = { 'username':username, "okMessage":s1[1] }
	else:
		s0 = { 'username':username, "errMessage":s1 }
	return json.dumps(s0)


def changePassButton( args ):
	"change users password"
	username = session['username']

	badStrings = [ [ 'password',  args[0] ] ]
	badStrings.append( [ 'password', args[1] ] )
	badStrings.append( [ 'password', args[2] ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return  [ 'logic ok', 'bad arg strings', json.dumps( { 'username':username, "errMessage":theRes } ) ]

	s1 = changePassword( username, args[0], args[1], args[2] )

	if s1[0] == "logic ok":
		if s1[1] == "password changed":
			s0 = [ 'logic ok', s1[1], json.dumps( '' ), json.dumps( { 'username':username, "okMessage":s1[1] } ) ]
			return s0
		s0 = [ 'logic ok', s1[1], json.dumps( '' ), json.dumps( { 'username':username, "errMessage":s1[1] } ) ]
		return s0

	return s1


def addUserButton( args ):
	"add new user"

	badStrings = [ [ 'username', args[0], False ] ]
	badStrings.append( [ 'password', args[1] ] )
	badStrings.append( [ 'password', args[2] ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return  [ 'logic ok', 'bad arg strings', json.dumps( { 'username':'unknown', "errMessage":theRes } ) ]

	s1 = addUser( args[0], args[1], args[2] )

	if s1[0] == 'logic ok':
		if s1[1] == 'user added':
			# top_one pastepoint 6
			varPr1 = addProduct( args[0] + '.euro', 'one euro' )
			varPr2 = addProduct( args[0] + '.mbtc', 'one mbtc' )
			if ( varPr1 == 'product added' ) and ( varPr2 == 'product added' ):
				s0 = [ 'logic ok', s1[1], json.dumps( [args[0]] ), json.dumps( { "newMessage":s1[1] } ) ]
			return s0
		s0 = [ 'logic ok', s1[1], json.dumps( [args[0]] ), json.dumps( { "newMessage":s1[1] } ) ]
		return s0

	return s1


def colours():
	"This returns colours"
	tempVar = 'style-dark.css'
	if request.form['jsvar1'] == 'light':
		tempVar = 'style-light.css'

	tempVar2 = url_for('static',filename = tempVar )

	session['cssStyle'] = tempVar2
#	changeStyle( tempVar )
	s0 = {'username':session['username'], 'message':'session colour changed' }

	return json.dumps( s0 )

# top_one pastepoint 5
def newLocationButton( args ):
	username = session['username']
	addStr = args[0]
	addLat = args[1] 
	addLng = args[2] 

	s1 = setLocation( username, addStr, addLat, addLng )

	if s1[0] == "logic ok":
		if s1[1] == "new location set":
			s0 = [ 'logic ok', s1[1], json.dumps( args ), json.dumps( { 'username':username, "okMessage":s1[1] } ) ]
			return s0
		s0 = [ 'logic ok', s1[1], json.dumps( args ), json.dumps( { 'username':username, "errMessage":s1[1] } ) ]

		return s0

	return s1


def productPageButton():
	varpr1 = request.form['jsvar1']

	print ( varpr1 )
	
	badStrings = [ [ 'product', varpr1, False ] ]
	theRes = areBadStrings( badStrings )

	if theRes != False:
		return json.dumps( { 'username':session['username'], 'errMessage':theRes } )

	s1 = productInfo( varpr1 )
	
	s1['username'] = session['username']
	
	s0j = json.dumps(s1)
	return s0j


def balanceButton():
	s1 = getBalanceAll( session['username'] )
	
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
		return  [ 'logic ok', 'bad arg strings', '', json.dumps( { 'username':username, "errMessage":theRes } ) ]

#		return json.dumps( 'logic ok', { 'username':session['username'], 'errMessage':theRes } )

#	s1 = sendAmount( username, 'zz', 'z1.euro', '1' )
#	s1 = sendAmount( session['username'], 'zz', 'z2.euro', '2' )
#	s1 = sendAmount( session['username'], 'z2', 'z2.euro', '2' )
#	s1 = sendAmount( session['username'], 'z2', 'z2.euro', '50' )

	s1 = sendAmount( username, userTo, product, amount )
	
	if s1[0] == 'logic ok':
		if s1[1] == 'amount sent':
			s0 = [ 'logic ok', s1[1], json.dumps( args ), json.dumps( { 'username':username, 'okMessage':s1[1] } ) ]
			return s0
		s0 = [ 'logic ok', s1[1], json.dumps( args ), json.dumps( { 'username':username, 'errMessage':s1[1] } ) ]
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

		s2 = getBalance( username, varpr1 )
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

