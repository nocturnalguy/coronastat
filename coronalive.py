########### IMPORTING THE REQURIED LIBRARIES ###########

from bs4 import BeautifulSoup as soup
import requests
import sys
from random import choice
from terminaltables import AsciiTable

########## DECLARING THE GLOBAL VARIABLES #############

WORLD_URL = "https://www.worldometers.info/coronavirus"
INDIA_URL = "https://www.mohfw.gov.in/"
MAX_TIMEOUT = 3
PROXY_TIMEOUT = 3

######## DECLARING THE CLASS FOR SCRAPING SSLPROXIES.COM ########

class _proxy:

	PROXY_URL = 'https://sslproxies.org/'
	page = None

	def __init__( self ):
		self.page = soup( requests.get( self.PROXY_URL ).text, 'lxml' )
    
	def getSSLProxyDictionary( self ):
 
		return {
		'https': choice( list( map( lambda x:x[ 0 ] + ':' + x[ 1 ], list( zip( map( lambda x:x.text, self.page.find( 'table' ).findAll( 'td' )[ :: 8 ] ), map( lambda x:x.text, self.page.find( 'table' ).findAll( 'td' )[ 1 :: 8 ] ) ) ) ) ) )
		}

######## DECLARING THE CLASS FOR GETTING COVID-19 DATA ########

class Corona:
	proxy = _proxy()

	######## DEFINING THE PROXY ROTATION METHOD ##########
	
	def _loadDataByIPRotation( self, url ):
		count = 0
		response = None
		while count < 10:
			try:
				proxyDictionary = self.proxy.getSSLProxyDictionary()
				print( 'Retry {} Using Proxy : {}'.format( count, proxyDictionary ) )
				response = requests.get( url, proxies = proxyDictionary, timeout = PROXY_TIMEOUT )
				break
			except:
				pass
			count=count+1
		return response

	######## GETTING THE HTML PAGE THROUGH GET REQUEST ########

	def getPageResponse( self, url ):
		try:
		  resp = requests.get( url, timeout = MAX_TIMEOUT )
		  page = soup( resp.text, 'lxml' ) 
		except:
			print( "\n\n ###### STARTING RANDOM PROXIES #######" );
			resp = self._loadDataByIPRotation( url )
			page = soup( resp.text, 'lxml' )

		return page

	########## EXTRACTING THE TABLE ###########

	def extractTableData( self, page, choice = "w" ):
		table = None
		table_heading = None
		table_content = None

		if choice == "w":
			try:
				table = page.find( "table",{
				  "id": "main_table_countries_today" 
				} )

				# table_heading = [ item.text.strip() for item in table.thead.tr if item != "\n" ]

				table_heading = [ "Country", "Confirmed\nCases", "New Cases", "Confirmed\nDeaths", "New Deaths", "Recovered", "Active cases", "Serious/Critical\ncases" ];

				table_content = []
				for rows in table.tbody:
				  data = [ item.text.strip() for item in rows if item != "\n" ]
				  if data:
				    table_content.append( data[ : -2 ] )

				table_content.insert( 0, table_heading )
				table = AsciiTable( table_content )
			except:
				print( "\n\n NO DATA RECIEVED !!" )
				exit();

		elif choice == "c":
			try:
				table = page.findAll( "div",{
					"class": "table-responsive" 
				} )[ 7 ]

				# table_heading = [ item.text.strip() for item in table.thead.tr if item != "\n" ]

				table_heading = [ "Sl. No.", "States/\nUnion Territories", "Confirmed cases\n( Indian National )", "Confirmed cases\n( Foreign National )", "Cured/Discharged/Migrated", "Death" ];

				table_content = []
				for rows in table.tbody:
				  data = [ item.text.strip() for item in rows if item != "\n" ]
				  if data:
				    table_content.append( data )

				table_content.insert( 0, table_heading )
				table = AsciiTable( table_content[ : -1 ] )
			except:
				print( "\n\n NO DATA RECIEVED !!" )
				exit();
		return table


######### DRIVER METHOD ##########

def main():
	corona = Corona();
	args = sys.argv

	if( args[ 1 ] == "-w" or args[ 1 ] == "--world" ):
		page = corona.getPageResponse( WORLD_URL )
		table = corona.extractTableData( page, "w" )
		print( table.table )
	elif( args[ 1 ] == "-c" or args[ 1 ] == "--country" ):
		page = corona.getPageResponse( INDIA_URL )
		table = corona.extractTableData( page, "c" )
		print( table.table )
	elif( args[ 1 ] == "-h" or args[ 1 ] == "--help" ):
		print( "\n usage : coronalive [ OPTIONS ]\n" );
		print( " options : " );
		print( " coronalive -h/--help		Opens the help for this CLI tool." );
		print( " coronalive -c/--country 	Opens statewise COVID-19 statistics ( only India's data is possible till now )." );
		print( " coronalive -w/--world 		Opens countrywise COVID-19 statistics.\n" );

if __name__ == "__main__":
	main()

