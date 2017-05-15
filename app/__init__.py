# Import flask and template operators
from flask import Flask, render_template

from app.mod_auth.auth_one import signin
from app.mod_top.top_one import topit
from app.mod_top.top_one import about1

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

@app.route('/')
def index():
	print 'app index'
	return topit()

@app.route('/about')
def about():
	return about1()#'aboutz!'


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.mod_auth.auth_one import mod_auth as auth_module
from app.mod_top.top_one import mod_top as top_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(top_module)

