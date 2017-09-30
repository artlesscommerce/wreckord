from flask import request, session # render_template, redirect, url_for #Flask, jsonify, Blueprint
import json

from app.mod_utils.utils_one import areBadStrings

from app.mod_products.products_one import productInfo
from app.mod_products.products_one import getBalance
from app.mod_products.products_one import getBalanceAll
from app.mod_products.products_one import sendAmount
from app.mod_products.products_one import getSendRecLog


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
		return  [ 'logic ok', 'bad arg strings', '', { 'username':username, "errMessage":theRes } ]

	s1 = sendAmount( username, userTo, product, amount )
	
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

