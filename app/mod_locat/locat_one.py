from flask import Flask, Blueprint, render_template
from pymysql import escape_string
from time import  strftime 

from app.mod_utils.dbconnect import a2q
from app.mod_utils.dbconnect import readcon

mod_locat = Blueprint('locat', __name__)


@mod_locat.route('/map/', methods=[ 'GET'] )
def mapmess():
	return render_template('locat/map.html' ) #, sitename='localq'  'POST',


def setLocation( user_id, addStr, addLat, addLng ):
	'sets the users location'
	print( 'setLocation : ', user_id, addStr, addLat, addLng )
	dateNow = strftime("%Y-%m-%d %H:%M:%S")
	q1  = "INSERT INTO userLocation ( user_id, status1, addStr, addLat, addLng, dateTime ) VALUES ( "
	q1 += '(%s),(%s),(%s),(%s),(%s),(%s) ) '

	q3 = "update userLocation set status1 = 'old' where ( user_id = %s  )"
	args = [ username ]
	a2q( q3, args )
	if ( addStr + addLat + addLng ) != '' :
		args = [ user_id, 'active', (addStr.encode('utf-8')), escape_string(addLat), escape_string(addLng ), dateNow ]
		a2q( q1, args )

		return [ 'logic ok', "new location set" ]

	return [ 'logic ok', "blank args" ]


def getLocation( username ):
	'returns current location'

	q1 = '''
	select userLocation.addStr from userLocation 
	join user on userLocation.user_id = user.id
	where name = %s and userLocation.status1 = 'active'
	'''
	
	args = [ username ]
	c = readcon( q1, args )
			
	row = c.fetchone()
	if row == None:
		return ''

	if row != None:
		return row[0]

