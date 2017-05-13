from flask import Blueprint, request, render_template, \
                  session, redirect, url_for

import bcrypt
from pymysql import escape_string
import json
from time import gmtime, strftime, time

from app.mod_utils.utils_one import areBadStrings

from app.mod_utils.dbconnect import connection
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signin/', methods=['POST'])
def signin():
	username = request.form['username']
	secretpw = request.form['secret']

	badStrings = [ [ 'username', username, False ] ]
	badStrings.append( [ 'password', secretpw  ] )

	theRes = areBadStrings( badStrings )
	if theRes != False:
		return 'bad pass'
		return  theRes

	if checkPassword( username, secretpw ) == True:
		session['logged_in'] = True
		session['username'] = username
		session['cssStyle'] = url_for('static',filename='style-dark.css')
		return  "loggedin"
	return 'bad pass'



@mod_auth.route('/logout/', methods=['GET'])
def logout():
	print 'logout!'
	session.clear()
	return redirect(url_for('index'))

@mod_auth.route('/newuser', methods=['GET'])
def newuser():
	if 'username' in session:
		return logout()
	return render_template('auth/newuser.html', sitename='localq'  )

@mod_auth.route('/newuser2', methods=['POST'])
def newuser2():
	username = request.form['jsvar1']
	password1 = request.form['jsvar2']
	password2 = request.form['jsvar3']

	badStrings = [ [ 'username', username, False ] ]
	badStrings.append( [ 'password', password1 ] )
	badStrings.append( [ 'password', password2 ] )

	theRes = areBadStrings( badStrings )

	if theRes != False:
		return json.dumps( { 'newMessage':theRes } )

	var = addUser( username, password1, password2 )
	
	return json.dumps( { 'newMessage':var } )
	



def checkPassword( username, pass1 ):
	"this returns true of the password and user are good, false otherwise" 
	try:
		c, conn = connection()
		c.execute("SELECT hashword, closeDate FROM users1 WHERE loginName = %s ", (escape_string(username)) )
		print c._last_executed
		fo = c.fetchone()
		if fo == None:
			return  False

		closedate = fo[1]

		if closedate != None:
			return False

		hw = fo[0]

		if bcrypt.hashpw( str( pass1 ), hw) == hw:
			return  True
		
		return  False
	except Exception as e:
		print 'oo ' + (str(e))
		return False

	return False


def addUser( username, password1, password2 ):
	"add a new user"
	
	if password1 != password2:
		return "passwords do not match"

	try:
		c, conn = connection()
		c.execute( 'select uniqueX from users1 where loginName = "' + username + '"' )
		row = c.fetchone()
		if row != None :
			return 'user name is taken'

		newHash = bcrypt.hashpw( str( password1 ) , bcrypt.gensalt())
		dateNow = strftime("%Y-%m-%d %H:%M:%S")
		c.execute( 'INSERT INTO users1 ( loginName, hashword, createDate ) VALUES ( "' + username + '", "' + newHash + '", "' + dateNow + '" ) ' )
#		addToQueryLog( username, c._last_executed )
		
		return 'user added'
		
	except Exception as e:
		return 'oo' + (str(e))

