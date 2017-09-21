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


function makePrevNextLinks( rowCount, allRows, startfrom, results, linkVar )
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
function makeProductLink( product )
{
	varr = splitCr1Pr1( product )
	if( varr[0] == '' )
	{
		return '<a href="#productPage&*' + product +'">' + product + '</a>'
	}
	return makeUserLink( varr[0] ) + '.' + '<a href="#productPage&*' + product +'">' + varr[1] + '</a>'
}

	
function splitCr1Pr1( product )
{
	console.log( product )
	cr1 = ''
	pr1 = ''
	varr = product.split( '.' )
	varrLen = varr.length
	if( varrLen == 2 )
	{
		cr1 = varr[0]
		pr1 = varr[1]
	}	
	if( varrLen == 1 )
	{
		pr1 = varr[0]
	}
	rvar = [ cr1, pr1 ]
	return rvar
}
	

function crprJoin( cr1, pr1 )
{
	if( cr1 == '' )
	{
		return pr1
	}
	return cr1 + '.' + pr1
}


function balanceTableFromList( balanceList, inUse = false, headings = true )
{
	console.log( balanceList )
	newvar2 = ''
	listlength = balanceList.length
	for ( j = 0 ; j < listlength ; j++ )
	{
		if( j == 0 )
		{
			varup  = ''

			if( ( inUse == true ) && ( headings == true ) )
			{
				varup += '<table class="red" id="marketstable">'
				varup += '<tr>'
				varup += '<td class="red">score</td>'
				varup += '<td class="red">available</td>'
				varup += '<td class="red">in use</td>'
				varup += '</tr>'
			}

			if( ( inUse == true ) && ( headings == false ) )
			{
				console.log( 'qqqq' )
				varup += '<table class="red" id="marketstable">'   // table type
			}


			if( ( inUse == false ) && ( headings == false ) )
			{
				varup += '<table class="red60" id="marketstable">'   // table type
			}

			if( ( inUse == false ) && ( headings == true ) )
			{
				varup += '<table class="red60" id="marketstable">'   // table type
				varup += '<tr>'
				varup += '<td class="red">score</td>'
				varup += '<td class="red">available</td>'
				varup += '</tr>'
			}
			newvar2 += varup
		}
		newvar2 += '<tr><td class="red">'

		newvar2 += makeProductLink( balanceList[j]['product'] ) ;
		newvar2 += '</td>'
		newvar2 += '<td class="red">'
		
		newvar2 += balanceList[j]['available'];
		newvar2 += '</td>'

		if( inUse )
		{
			newvar2 += '<td class="red">'
			newvar2 += balanceList[j]['in use'];
			newvar2 += '</td>'
			newvar2 += '</tr>'
		}
			
		if( j == listlength - 1 )
		{
			newvar2 += '</table>'
		}
	}
	return newvar2
}

