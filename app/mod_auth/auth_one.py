from flask import Blueprint, request, render_template, session, redirect, url_for

import bcrypt
from pymysql import escape_string
import json
from time import gmtime, strftime, time

from app.mod_utils.utils_one import areBadStrings

from app.mod_utils.dbconnect import connection
from app.mod_utils.dbconnect import a2q
from app.mod_utils.dbconnect import readcon

mod_auth = Blueprint('auth', __name__ ) #url_prefix='/auth'


@mod_auth.route('/signin/', methods=['POST'])
def signin():
	username = request.form['username'].lower()
	secretpw = request.form['secret']

	badStrings = [ [ 'username', username, False ] ]
	badStrings.append( [ 'password', secretpw  ] )

	theRes = areBadStrings( badStrings )
	if theRes != False:
		return 'bad pass : ' + str( theRes )

	varCheckPw = checkPassword( username, secretpw )
	if varCheckPw[0] == True:
		session['logged_in'] = True
		session['username'] = username
		session['user_id'] = varCheckPw[1]
		thestyle = 'style-dark.css'
		session['cssStyle'] = url_for('static',filename=thestyle)
		print ( 'add to signinLog...' + username )
		return  "loggedin"
	return 'bad pass'


@mod_auth.route('/logout/', methods=['GET'])
def logout():
	print ('logout!')
	session.clear()
	return redirect(url_for('index'))


@mod_auth.route('/newuser', methods=['GET'])
def newuser():
	if 'username' in session:
		return logout()
	return render_template('auth/newuser.html', sitename='localq'  )




def checkPassword( username, password1 ):
	"this returns true of the password and user are good, false otherwise"
	try:
		pw1Bytes = password1.encode('utf-8')
#		c, conn = connection()
#		c.execute("SELECT hashword, closeDate, id FROM user2 WHERE loginName = %s ", (escape_string(username)) )
		q1 = 'SELECT hashword, closeDate, id FROM user WHERE name = %s '
		args = [ username ]
		c = readcon( q1, args )

		fo = c.fetchone()
		if fo == None:
			return [ False, 0 ]

		closedate = fo[1]

		if closedate != None:
			return [ False, 0 ]

		hwBytes = fo[0].encode('utf-8')

		if bcrypt.hashpw( pw1Bytes, hwBytes) == hwBytes:
			return [ True, fo[2] ]

		return [ False, 0 ]
	except Exception as e:
		print ('oo 91 ' + (str(e)) )
		return [ False, 0 ]

	return [ False, 0 ]


def addUser( username, password1, password2 ):
	"add a new user"
	if password1 != password2:
		return [ 'logic ok', 'passwords do not match' ]

	try:
#		c, conn = connection()
#		c.execute( 'select id from user2 where loginName = "' + username + '"' )
		q1 = 'select id from user where name = %s '
		args = [ username ]
		c = readcon( q1, args )
		row = c.fetchone()
		if row != None :
			return [ 'logic ok', 'user name is taken' ]
		
		pw1Bytes = password1.encode('utf-8')
		newHash = bcrypt.hashpw( pw1Bytes , bcrypt.gensalt())
		dateNow = strftime("%Y-%m-%d %H:%M:%S")
		q1 = 'INSERT INTO user ( name, hashword, createDate ) VALUES ( %s, %s, %s )'
		args = [ username, newHash, dateNow ]
		a2q( q1, args )

		return [ 'logic ok', 'user added' ]

	except Exception as e:
		return 'oo 115 :' + (str(e))



def changePassword( username, oldPass, newPass1, newPass2 ):
	"this changes a user's password"

	if newPass1 != newPass2:
		return [ 'logic ok', 'new passwords don\'t match' ]

	try:
		if checkPassword( username, oldPass )[ 0 ]:
#			c, conn = connection()
			newHash = bcrypt.hashpw( newPass1.encode('utf-8') , bcrypt.gensalt())
			q1 = "update user set hashword = %s where name = %s "
			args = [ newHash, username ]
			a2q( q1, args )
			return [ 'logic ok', "password changed" ]
		return [ 'logic ok', "password not changed" ]

	except Exception as e:
		print ( 'oo 141 ' + (str(e)) )
		return 'logic error : ' + (str(e))


def closeUser( username, pass1 ):
	return 'user not closed'


def userExists(username):
	try:
#		c, conn = connection()
#		c.execute("SELECT closeDate FROM user2 WHERE loginName = %s ", username )

		q1 = 'SELECT closeDate FROM user WHERE name = %s '
		args = [ username ]
		c = readcon( q1, args )

		rowa = c.fetchone()
		
		if rowa == None:
			return 'no user'

		closedate = rowa[0]
		if closedate != None:
			return "user closed!"

		return True

	except Exception as e:
		return 'oo' + (str(e))
	return False




def userExists_id( user_id ):
	try:
		q1 = 'SELECT closeDate FROM user WHERE id = %s '
		args = [ user_id ]
		c = readcon( q1, args )

		rowa = c.fetchone()
		
		if rowa == None:
			return 'no user'

		closedate = rowa[0]
		if closedate != None:
			return "user closed!"

		return True

	except Exception as e:
		return 'oo' + (str(e))
	return False



def userCreateDate( username ):
	try:
#		c, conn = connection()
##		c.execute("SELECT createDate FROM user2 WHERE loginName = %s ", username )

		q1 = 'SELECT createDate FROM user WHERE name = %s  '
		args = [ username ]
		c = readcon( q1, args )

		rowa = c.fetchone()
		
		if rowa == None:
			return 'no user'
		
		return rowa[0]
		
	except Exception as e:
		print(  'oo' + (str(e)) )
	return False


def userInfo( username ):
	'return an array of user info'
	s0 = {}
	s0['otherUser'] = username
	
	varExists = userExists( username )
	
	if varExists != True:
		s0['status'] = varExists
		return s0

	s0['status'] = 'okay'
	s0['createDate'] = str( userCreateDate( username ) )
	
	return s0


def listUsers():
	'return a list of users'
	try:
#		c, conn = connection()
#		c.execute( 'SELECT loginName FROM users1', [] )
#		c.execute( 'SELECT loginName FROM user2' )

		q1 = 'SELECT name FROM user'
		c = readcon( q1, [] )


		myRowCount = c.rowcount
		myList = []
		row = c.fetchone()
		while row is not None:
			myList.append( row[0] )
			row = c.fetchone()

		return { 'count': myRowCount, 'userList':myList }

	except Exception as e:
		print ( 'oo ' + (str(e)) )
	return -1


def userNameToId( username ):
	q1 = 'SELECT id FROM user where name = %s'
	c = readcon( q1, [ username ] )
	row = c.fetchone()
	if row is not None:
		return row[0]
	return 0


def userIdToName( user_id ):
	q1 = 'SELECT name FROM user where id = %s'
	c = readcon( q1, [ user_id ] )
	row = c.fetchone()
	if row is not None:
		return row[0]
	return 0

