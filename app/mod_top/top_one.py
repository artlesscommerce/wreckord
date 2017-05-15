from flask import Flask, jsonify, Blueprint, request, render_template, session, redirect, url_for

import json
from random import randint

from app.mod_auth.auth_one import changeStyle
from app.mod_auth.auth_one import changePassword
from app.mod_utils.utils_one import areBadStrings
from app.mod_utils.varfuncs import conFunc

mod_top = Blueprint('top', __name__, url_prefix='/top')


@mod_top.route('/topit/', methods=['GET'])
def topit():
	if 'username' in session:
		print 'inseess2',session['username'] 
		var = randint( 100, 10100 )
		var = '?v=' + str( var )#'localq'
		return render_template('top/loggedin.html', mycssfile=session['cssStyle'], sitename=conFunc( 'sitename' ),\
		name=session['username'], random=var )
	print 'topit now'
	return render_template('top/loggedout.html', sitename= conFunc( 'sitename' ) )


#@mod_top.route('/about/', methods=['GET'])
def about1():
	return render_template('top/about.html' )


@mod_top.route('/ajax/', methods=['POST'])
def ajax():
	buttontype = 'blank'
	try:
		buttontype = request.form['buttontype']
	except Exception as e:
		print 'oo ' + (str(e))

	print 'topx!!1', buttontype

	logged_in_var = False

	if 'username' in session:
		if 'logged_in' in session:
			if session['logged_in'] == True :
				logged_in_var = True

	if logged_in_var != True:
		return 'not_logged_in!'

	if buttontype == 'testme':
		return json.dumps( {'username':session['username'], 'errMessage':'yay' } )
	if buttontype == 'colours':
		return colours()
	if buttontype == 'changePassButton':
		return changePassButton()
	return json.dumps( {'username':session['username'], 'errMessage':'badbuttontype' } )


def changePassButton():
	"change users password"
	username = session['username']

	badStrings = [ [ 'password', request.form['jsvar1']] ]
	badStrings.append( [ 'password', request.form['jsvar2'] ] )
	badStrings.append( [ 'password', request.form['jsvar3'] ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return json.dumps( { 'username':username, 'errMessage':theRes } )

	s1 = changePassword( username, request.form['jsvar1'], request.form['jsvar2'], request.form['jsvar3'] )

	if s1 == "password changed":
		s0 = { 'username':username, "okMessage":s1 }
	else:
		s0 = { 'username':username, "errMessage":s1 }

	return json.dumps(s0)


def colours():
	"This returns colours"
	tempVar = 'style-dark.css'
	if request.form['jsvar1'] == 'light':
		tempVar = 'style-light.css'

	tempVar2 = url_for('static',filename = tempVar )

	session['cssStyle'] = tempVar2
	changeStyle( tempVar )
	s0 = {'username':session['username'], 'message':'session colour changed' }

	return json.dumps( s0 )

