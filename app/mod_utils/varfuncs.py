

myDict = {}

myDict['sitename']   = 'localq'

myDict['dbhost']     = 'localhost'
myDict['dbuser']     = 'tablecuser'
myDict['dbpasswd']   = 'tablecpass'
myDict['dbtable']    = 'tablec'

def conFunc( varCon ):
	try:
		return myDict[ varCon ]
	except Exception as e:
		print ( 'errr confunc ' + (str(e)) )
		return 'blank'
