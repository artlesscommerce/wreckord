

myDict = {}

myDict['sitename']   = 'localq'
'''
myDict['dbhost']     = 'localhost'
myDict['dbuser']     = 'tablecuser'
myDict['dbpasswd']   = 'tablecpass'
myDict['dbtable']    = 'tablec'
'''
myDict['dbhost']     = 'localhost'
myDict['dbuser']     = 'user10'
myDict['dbpasswd']   = 'dbpassoct'
myDict['dbtable']    = 'dbschema2'

def conFunc( varCon ):
	try:
		return myDict[ varCon ]
	except Exception as e:
		print ( 'errr confunc ' + (str(e)) )
		return 'blank'
