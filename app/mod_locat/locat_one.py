from flask import Flask, Blueprint, render_template
from pymysql import escape_string
from time import  strftime 
from app.mod_utils.dbconnect import connection
from app.mod_utils.dbconnect import a2q

mod_locat = Blueprint('locat', __name__)


@mod_locat.route('/map/', methods=[ 'GET'] )
def mapmess():
	return render_template('locat/map.html' ) #, sitename='localq'  'POST',


def setLocation( username, addStr, addLat, addLng ):
	'sets the users location'
	print( 'setLocation : ', username, addStr, addLat, addLng )
	dateNow = strftime("%Y-%m-%d %H:%M:%S")
	q1  = "INSERT INTO userLocations ( user, status1, addStr, addLat, addLng, dateTime ) VALUES ( "
	q1 += '(%s),(%s),(%s),(%s),(%s),(%s) ) '

	try:
		q3 = "update userLocations set status1 = 'old' where ( user = %s  )"
		args = [ username ]
		a2q( q3, args )
		if ( addStr + addLat + addLng ) != '' :
			args = [ username, 'active', (addStr.encode('utf-8')), escape_string(addLat), escape_string(addLng ), dateNow ]
			a2q( q1, args )

			return [ 'logic ok', "new location set" ]

		return [ 'logic ok', "blank args" ]

	except Exception as e:
		print( 'oo 44 ' + ( str(e) ) )
		return 'logic error: ' + str(e)


def getLocation( username ):
	'returns current location'

	q1  = 'SELECT addStr FROM userLocations where '
	q1 += '( user = "' + username + '" and status1 = "active" ) order  by dateTime desc'
	
	try:
		c, conn = connection()
		c.execute( q1 )
		
		row = c.fetchone()
		if row == None:
			return ''

		if row != None:
			return row[0]

	except Exception as e:
		print( 'oo' + (str(e)) )
	return ''
