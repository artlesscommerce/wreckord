

okCharsName = "abcdefghijklmnopqrstuvwxyz0123456789"							   # product, username
okCharsPaWo = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"	   # password
minLength = 2
maxLength = 25


def areBadStrings( varr ):
	count = 0
	vlen = len( varr )

	while count < vlen:
		if varr[count][0] == 'username':
			myCheck = checkString( 'username', varr[count][1], okCharsName, minLength, maxLength, True, varr[count][2] )
			if myCheck != True:
				return myCheck
		if varr[count][0] == 'password':
			myCheck = checkString( 'password', varr[count][1], okCharsPaWo, minLength, maxLength, False, False )
			if myCheck != True:
				return myCheck
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
