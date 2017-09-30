from flask import request, session # render_template, redirect, url_for #Flask, jsonify, Blueprint, 
import json

from app.mod_locat.locat_one import setLocation

def newLocationButton( args ):
	username = session['username']
	addStr = args[0]
	addLat = args[1] 
	addLng = args[2] 

	s1 = setLocation( username, addStr, addLat, addLng )

	if s1[0] == "logic ok":
		if s1[1] == "new location set":
			s0 = [ 'logic ok', s1[1], json.dumps( args ), { 'username':username, "okMessage":s1[1] } ]
			return s0
		s0 = [ 'logic ok', s1[1], json.dumps( args ), { 'username':username, "errMessage":s1[1] } ]

		return s0

	return s1
