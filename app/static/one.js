function ajaxRequest()
{
	try
	{
		var request = new XMLHttpRequest()
	}
	catch(e1)
	{
		try
		{
			request = new ActiveXObject("Msxml2.XMLHTTP")
		}
		catch(e2)
		{
			try
			{
				request = new ActiveXObject("Microsoft.XMLHTTP")
			}
			catch(e3)
			{
				request = false
			}
		}
	}
	return request
}


function makeUserLink( username )
{
	return '<a href="#userInfo&*' + username +'">' + username + '</a>'
}


function makePrevNextLinks( allRows, startfrom, results, linkVar )
{
	v1 = ( 1 * startfrom ) + 1
	v2 = ( 1 * results ) + ( 1 * startfrom )
	if( v2 > allRows )
	{
		v2 = allRows
	}
	varTop = 'displaying results ' + v1 + ' to ' + v2 + ' of ' + allRows
	
	v3 = ( 1 * results ) + ( 1 * startfrom )
	nexLink  = '<a href="#' + linkVar + '&*' + v3 +'&*' + results + '">next</a>'

	if( v3 >= allRows )
	{
		nexLink = ''
	}

	preLink = ''
	if( startfrom < 1 )
	{
		preLink = ''
	}
	else
	{
		v4 =  ( 1 * startfrom ) - ( 1 * results )
		if( v4 < 1 )
		{
			v4 = 0
		}
		preLink  = '<a href="#' + linkVar + '&*' + v4 +'&*' + results + '">prev</a>'
	}

	newvar2  = '<center><div id="prenex">'
	newvar2 += '<div id="pre">'
	newvar2 += preLink
	newvar2 += '</div>'
	newvar2 += '<div id="nex">'
	newvar2 += nexLink
	newvar2 += '</div>'
	newvar2 += '</div></center>'

	varr = [ varTop, newvar2 ]
	return varr
}


// one.js pastepoint 1



