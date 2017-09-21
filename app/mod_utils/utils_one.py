

okCharsName = "abcdefghijklmnopqrstuvwxyz0123456789"							   # product, username
okCharsPaWo = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"	   # password
minLength = 2
maxLength = 25


def areBadStrings( varr ):
	count = 0
	vlen = len( varr )

	
	print ( 'qq', varr , 'zz' )
			
	while count < vlen:
		if varr[count][0] == 'username':
			print ( 'qq', varr[count][1] , 'zz' )
			myCheck = checkString( 'username', varr[count][1], okCharsName, minLength, maxLength, startWithLetter = True )
			if myCheck != True:
				return myCheck
		if varr[count][0] == 'password':
			myCheck = checkString( 'password', varr[count][1], okCharsPaWo, minLength, maxLength, False, False )
			if myCheck != True:
				return myCheck
		# utils_one pastepoint 1
		if varr[count][0] == 'product':
			if varr[count][1] == '':
				return 'product is blank'
			cr1pr1 = varr[count][1].split('.')
			if len( cr1pr1 ) == 1:
				check1 = checkString( 'product', cr1pr1[0], okCharsName, minLength, maxLength, True, False )
				if check1 != True:
					return check2
			if len( cr1pr1 ) == 2:
				check1 = checkString( 'username', cr1pr1[0], okCharsName, minLength, maxLength, True, True )
				if check1 != True:
					return check1
				check2 = checkString( 'product', cr1pr1[1], okCharsName, minLength, maxLength, True, False )
				if check2 != True:
					return check2
		count += 1
	return False


def checkString( typeString, varString, okChars, minLength, maxLength, startWithLetter = False, canBeBlank = False ):
	if ( varString == '' ) and ( canBeBlank == True ):
		return True
	if len(varString) > maxLength or len(varString) < minLength :
		return typeString + ' : length must not be less than ' + str(minLength) + ' or greater than ' + str(maxLength)
	if startWithLetter:
		letter = varString[0]
		if not letter in "abcdefghjklmnopqrstuvwxyz":
			return typeString + ' must begin with abcdefghjklmnopqrstuvwxyz'
	for letter in varString:
		if not letter in okChars:
			return typeString + ' must contain only ' + okChars
	return True
