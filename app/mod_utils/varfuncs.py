

myDict = {}

myDict['sitename']   = 'localq'

myDict['dbhost']     = 'localhost'
myDict['dbuser']     = ''
myDict['dbpasswd']   = ''
myDict['dbtable']    = ''

def conFunc( varCon ):
	try:
		return myDict[ varCon ]
	except Exception as e:
		print 'errr confunc ' + (str(e))
		return 'blank'
