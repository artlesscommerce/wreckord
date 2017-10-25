from flask import Flask, jsonify, Blueprint, request, render_template, session, redirect, url_for

import json
from random import randint
from datetime import datetime
from time import strftime
import time

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

#from app.mod_auth.auth_one import userNameToId

from app.mod_top.locat_top import newLocationButton

from app.mod_top.auth_top import userInfoButton
from app.mod_top.auth_top import listUsersButton
from app.mod_top.auth_top import closeUserButton
from app.mod_top.auth_top import changePassButton
from app.mod_top.auth_top import addUserButton

from app.mod_top.products_top import productPageButton
from app.mod_top.products_top import balanceButton
from app.mod_top.products_top import sendAmountButton
from app.mod_top.products_top import sendAmountButtonNew
from app.mod_top.products_top import sendAmountFormButton
from app.mod_top.products_top import sendRecLogButton
from app.mod_top.products_top import addProductButton



mod_top = Blueprint('top', __name__ )


def topit():
	if 'username' in session:
		print ( 'in session : ',session['username'], session['user_id'] )
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

	return var



@mod_top.route('/ajax/', methods=['POST'])
def ajax():
	print ( 'ajax ooo' )
	buttonType = 'blank'
	try:
		buttonType = request.form['buttontype']
	except Exception as e:
		print( 'oo 114' + (str(e)) )

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
	writeReqs.append( 'addTrade' )
	writeReqs.append( 'deleteTrade' )

	if buttonType in writeReqs:
		qwe =  ajaxWrite( buttonType, session['username'] )
		return qwe

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
	# top_one pastepoint 3
	if buttonType == 'productPage':
		return productPageButton()
	if buttonType == 'balance':
		return balanceButton()
	if buttonType == 'sendAmountForm':
		return sendAmountFormButton()
	if buttonType == 'sendRecLog':
		return sendRecLogButton()

	return json.dumps( {'username':session['username'], } )


def ajaxWrite( buttonType, username, args = None ):
	print ( 'ajaxWrite' )
	
	if buttonType == 'addUser':
		var1 = addUserButton
	if buttonType == 'changePassButton':
		var1 = changePassButton
	if buttonType == 'closeUserButton':
		var1 = closeUserButton
	# top_one pastepoint 4
	if buttonType == 'newLocation':
		var1 = newLocationButton
	if buttonType == 'sendAmount':
		var1 = sendAmountButton

	return lockUnlock( var1, buttonType, username, args )


def lockUnlock( argFunc, buttonType, username, args = None ):
	print ( 'lockUnlock' )
	lockVar = lockTables()
	
	if lockVar != 'okay':
		return json.dumps( { 'username':username, 'errMessage':'table is locked' } )
	
	varAjax = newAjaxRequest( argFunc, buttonType, username, args )

	if varAjax[0] == 'unlock tables':
		# put thimgs here
		unLockTables()
		
		if buttonType == 'deleteTrade':
			return myTradesButton()
		return json.dumps( varAjax[1] )
		
	tableLockNotice( varAjax[0], varAjax[1] )
	
	return json.dumps( { 'username':username, 'errMessage':'table is locked' } )
	#return [ varAjax[0], varAjax[1] ]


def newAjaxRequest( argFunc, buttonType, username, args = None, parent_id = 0 ):
	print ( 'newAjaxRequest', args )
	print ( 'parent_id', parent_id )
	
	if args == None:
		args = getArgs()
	
	dateNow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	dateNowLogic = '0'
	dateNowWrite = '0'
	message = ''
	
	requestId = newRequest( username, parent_id, buttonType, dateNow )
	
	if int(requestId) < 1:
		return [ 'bad write', 'new request' ]

	timerVar1 = int(round(time.time() * 1000))
	var1 = argFunc( args )
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

			print ( 'get side0', args[0], args[1], jsonVar, '\n'  )
			
			if jsonVar.get( 'requestList', None ) != None:
				print ( ' more requests...' )
				print ( ' more requests...', jsonVar['requestList'] )
				for x in jsonVar['requestList']:
					print ( '\nnewReq', x )
					varR1 = 'xrequest list not None'
					if x[1] == 'sendAmount':
						varR1 = newAjaxRequest( sendAmountButtonNew, x[1], x[0], x[2], requestId )
					if x[1] == 'addProduct':
						varR1 = newAjaxRequest( addProductButton, x[1], x[0], x[2], requestId )
					if varR1[0] != 'unlock tables':
						return varR1
						
			return ['unlock tables', jsonVar ]

		else:
			endRequest( requestId, args2, var1[1], 'pass', 'fail', dateNowLogic, dateNowWrite )
			return [ 'bad write', writeVar ]
	else:
		endRequest( requestId, '', message, 'fail', 'false', dateNowLogic, dateNowWrite )
		
		print ( var1 )
		return [ 'bad logic', var1 ]







def getArgs():
	"This returns jsvars"
	varr = []
	varr.append( request.form['jsvar1'] )
	varr.append( request.form['jsvar2'] )
	varr.append( request.form['jsvar3'] )
	varr.append( request.form['jsvar4'] )
	varr.append( request.form['jsvar5'] )
	
	return varr


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
	


