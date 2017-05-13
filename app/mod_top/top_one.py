from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from flask import Flask, request, jsonify, render_template, session, url_for, redirect

import json
from random import randint

from app.mod_utils.utils_one import echos


mod_top = Blueprint('top', __name__, url_prefix='/top')


@mod_top.route('/topit/', methods=['GET'])
def topit():
	if 'username' in session:
		print 'inseess2',session['username'] 
		var = randint( 100, 10100 )
		var = '?v=' + str( var )
		return render_template('top/loggedin.html', mycssfile=session['cssStyle'], sitename='localq', name=session['username'], random=var )
	else:
		echos()
		print 'nopwe2'
		#session['username'] = 'bounce'
	print 'topit now'
	return render_template('top/loggedout.html', sitename='localq' )


@mod_top.route('/ajax/', methods=['POST'])
def ajax():
	print 'yo!!', request.form['jsvar1']
	if request.form['buttontype'] == 'testme':
		return json.dumps( {'username':session['username'], 'what':'yay' } )
	if request.form['buttontype'] == 'colours':
		return colours()



def colours():
	"This returns colours"
	#check bad sting
	tempVar = url_for('static',filename='style-dark.css')
	if request.form['jsvar1'] == 'light':
		tempVar = url_for('static',filename='style-light.css')

	session['cssStyle'] = tempVar
	s0 = {'username':session['username'], 'message':'session colour changed' }

	return json.dumps( {'username':session['username'], 'message':'session colour changed' } )

