
function makeProductLink( product )
{
	varr = splitCr1Pr1( product )
	if( varr[0] == '' )
	{
		return '<a href="#productPage&*' + product +'">' + product + '</a>'
	}
	return makeUserLink( varr[0] ) + '.' + '<a href="#productPage&*' + product +'">' + varr[1] + '</a>'
}


function roundToPlaces(num, nume, blankZero = '0')
{
	if(isNaN( num ) || num == '' || num == 'None' ) 
	{
		return blankZero ;	
	}
	if(num == 0 ) 
	{
		return 0 ;
	}
	return +(Math.round(num + "e+" + nume )  + "e-" + nume );
}


function splitCr1Pr1( product )
{
	cr1 = ''
	product1 = ''
	varr = product.split( '.' )
	varrLen = varr.length
	if( varrLen == 2 )
	{
		cr1 = varr[0]
		product1 = varr[1]
	}	
	if( varrLen == 1 )
	{
		product1 = varr[0]
	}
	rvar = [ cr1, product1 ]
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


function sendRecLogPage( jvar )
{
	pagevar = ''
	if ( jvar['rows'].length > 0 )
	{
		myLinks = makePrevNextLinks( jvar['allRows'], jvar['startfrom'], jvar['results'], 'sendRecLog' )
		pagevar += myLinks[0] + '<br><br>'

		for (var i = 0; i < jvar['rows'].length; i++)
		{	
			if ( i == 0 )
			{
				pagevar += '<table>'
			}
			
			userToVar = jvar['rows'][i]['sendSort']
			if ( jvar['rows'][i]['sendSort'] == 'ordinary' )
			{
				userToVar = makeUserLink( jvar['rows'][i]['userTo'] )
			}
			
			pagevar +=  '<tr>'
			pagevar +=  '<td>'

			pagevar += roundToPlaces( jvar['rows'][i]['amount'] * 0.001, 3 )
			pagevar +=  '</td>'
			pagevar +=  '<td>'
			pagevar +=  makeProductLink( jvar['rows'][i]['product'] )
			pagevar +=  '</td>'
			pagevar +=  '<td>'
			pagevar +=  jvar['rows'][i]['sentRecvd']
			pagevar +=  '</td>'
			pagevar +=  '<td>'
			pagevar +=  userToVar
			pagevar +=  '</td>'
			pagevar +=  '<td>'
			t1 = jvar['rows'][i]['dateTime'].split( ' ' )
			pagevar +=  t1[0] + '<br>'
			pagevar +=  '</td>'
			pagevar +=  '<td>'
			pagevar += t1[1].split( '.' )[0]
			pagevar +=  '</td>'

			if ( i == jvar['rows'].length - 1 )
			{
				pagevar += '</table>'
				pagevar += '<br>' + myLinks[1] + '<br>'
			}
		}
	}
	else
	{
		pagevar = 'there is nothing here'
	}
	return pagevar
}


function balanceTableFromList( balanceList, inUse = false, headings = true )
{
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
		newvar2 += roundToPlaces( balanceList[j]['available'] * 0.001, 3 );
		newvar2 += '</td>'

		if( inUse )
		{
			newvar2 += '<td class="red">'
			newvar2 += roundToPlaces( balanceList[j]['in use'] * 0.001, 3 );
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



function sendAmountFormPage( jvar )
{
	pagevar = ''
	varPr = ''
	
	if ( typeof jvar['balance'] !== 'undefined')
	{
		if ( typeof jvar['balance']['product'] !== 'undefined') 
		{
			pagevar = balanceTableFromList( [jvar['balance']], inUse = false, headings = true )
			varPr = jvar['balance']['product']
		}
	}

	varTo = jvar['userTo']

	sendFormVar = '<TABLE >'
	
	sendFormVar += '<tr class="trq"><td>to</td><td><input type="text" id="nameto" value="'
	sendFormVar += varTo
	sendFormVar += '" maxlength="25"></td></tr>'

	sendFormVar += '<tr class="trq"><td>creator.product</td><td><input type="text" value="'
	sendFormVar += varPr
	sendFormVar += '" id="cr1pr1" maxlength="25"></td></tr>'

	sendFormVar += '<tr class="trq"><td>amount</td><td><input type="text" value="'
	sendFormVar += '1'
	sendFormVar += '" id="amount1" maxlength="25"></td></tr>'

	varww  = 'document.getElementById(\'nameto\').value, document.getElementById(\'cr1pr1\').value, '
	varww += 'document.getElementById(\'amount1\').value * 1000'
	newvar2 = '<button name="button100" id="foo" onclick="robotButton( \'sendAmount\', ' + varww + ' ) ;" >Send</a>';
	
	sendFormVar += '<tr class="trq"><td></td><td id="buttonhere">'
	sendFormVar += newvar2
	sendFormVar += '</td></tr></TABLE >'

}

function productPage( )
{
	productpagevar = '<table id="productpageTable" class="blue"><tr><td>creator</td><td></td></tr><tr><td>product</td>\
					  <td></td></tr><tr><td>create date</td><td></td></tr>\
					  <tr><td>details</td><td></td></tr></table>'

	if( jvar['message'] == 'okay' )
	{
		pagevar = '<b>' + jvar['cr1'] + ' ' + jvar['pr1'] + '</b><br><br>'

		pagevar += productpagevar + '<br>'

		crpr = jvar['cr1'] + '.' + jvar['pr1']
		crpr = crprJoin( jvar['cr1'], jvar['pr1'] )
		
		pagevar += '<a href="#sendAmountForm&*' + crpr +'&*'
		pagevar += '">send to</a>' + '<br>'
	
		document.getElementById('content').innerHTML = pagevar

		var myTable = document.getElementById( 'productpageTable' );

		uservar = ''
		if( jvar['cr1'] == '' )
		{
			uservar = 'localhost'
		}
		else
		{
			uservar = makeUserLink( jvar['cr1'] )
		}

		myTable.rows[0].cells[1].innerHTML = uservar 

		myTable.rows[1].cells[1].innerHTML = jvar['pr1']
		myTable.rows[2].cells[1].innerHTML = jvar['description']
		myTable.rows[3].cells[1].innerHTML = jvar['dateTime']
	}
	else
	{
		document.getElementById('content').innerHTML = jvar['message']
	}
}
