from flask import request, session # render_template, redirect, url_for #Flask, jsonify, Blueprint
import json

from app.mod_utils.utils_one import areBadStrings
from app.mod_utils.dbconnect import getAutoIncrement
from app.mod_locat.locat_one import getLocation

from app.mod_auth.auth_one import changePassword
from app.mod_auth.auth_one import closeUser
from app.mod_auth.auth_one import userInfo
from app.mod_auth.auth_one import listUsers
from app.mod_auth.auth_one import addUser

from app.mod_products.products_one import addProduct



def userInfoButton():
	"This returns current user information"

	varuser = request.form['jsvar1']

	badStrings = [ [ 'username', varuser, False ] ]
	theRes = areBadStrings( badStrings )

	if theRes != False:
		return json.dumps( {'username':username, 'errMessage':theRes } )

	s1 = userInfo( varuser )
	# top_one pastepoint 1
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

	s0 = [ 'logic ok', 'user not closed', '', { 'username':username, "okMessage":'user not closed' } ]
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
		return  [ 'logic ok', 'bad arg strings', '', { 'username':username, "errMessage":theRes } ]

	s1 = changePassword( username, args[0], args[1], args[2] )

	if s1[0] == "logic ok":
		if s1[1] == "password changed":
			s0 = [ 'logic ok', s1[1], '',  { 'username':username, "okMessage":s1[1] } ]
			return s0
		s0 = [ 'logic ok', s1[1], '', { 'username':username, "errMessage":s1[1] } ]
		return s0

	return s1


def addUserButton( args ):
	"add new user"

	badStrings = [ [ 'username', args[0], False ] ]
	badStrings.append( [ 'password', args[1] ] )
	badStrings.append( [ 'password', args[2] ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return  [ 'logic ok', 'bad arg strings', '', { 'username':'unknown', "errMessage":theRes } ]

	s1 = addUser( args[0], args[1], args[2] )

	if s1[0] == 'logic ok':
		if s1[1] == 'user added':

			requestList = []
			requestType = 'addProduct'
			argsR = [ args[0] + '.euro', 'one euro', args[0] ]
			requestList.append( [ 'unknown' ,requestType, argsR ] )
			argsR = [ args[0] + '.mbtc', 'one mbtc', args[0] ]
			requestList.append( [ 'unknown' ,requestType, argsR ] )

			s0 = [ 'logic ok', s1[1], json.dumps( [args[0]] ), { "newMessage":s1[1], 'requestList':requestList } ]
			return s0

		s0 = [ 'logic ok', s1[1], json.dumps( [args[0]] ), { "newMessage":s1[1], 'requestList':None } ]
		return s0

	return s1

