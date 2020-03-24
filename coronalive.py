########### IMPORTING THE REQURIED LIBRARIES ###########

from bs4 import BeautifulSoup as soup
import requests
from random import choice
from terminaltables import AsciiTable

########## DECLARING THE GLOBAL VARIABLES #############

BASE_URL = "https://www.worldometers.info/coronavirus"
MAX_TIMEOUT = 3

######## DECLARING THE CLASS FOR SCRAPING SSLPROXIES.COM ########

class _proxy:

	PROXY_URL = 'https://sslproxies.org/'
	page = None

	def __init__( self ):
		self.page = soup( requests.get( self.PROXY_URL ).text, 'lxml' )
    
	def getSSLProxyDictionary( self ):
 
		return {
		'https': choice( list( map( lambda x:x[ 0 ] + ':' + x[ 1 ], list( zip( map( lambda x:x.text, self.page.find( 'table' ).findAll( 'td' )[ ::8 ] ), map( lambda x:x.text, self.page.find( 'table' ).findAll( 'td' )[ 1::8 ] ) ) ) ) ) )
		}

proxy = _proxy()

######## DEFINING THE PROXY ROTATION METHOD ##########

def _loadDataByIPRotation( url ):
	count = 0
	response = None
	while count < 10:
		try:
			proxyDictionary = proxy.getSSLProxyDictionary()
			print( 'Retry {} Using Proxy : {}'.format( count, proxyDictionary ) )
			response = requests.get( url, proxies = proxyDictionary, timeout = MAX_TIMEOUT )
			break
		except:
			pass
		count=count+1
	return response

######## GETTING THE HTML PAGE THROUGH GET REQUEST ########

try:
  resp = requests.get( BASE_URL, timeout = MAX_TIMEOUT )
  page = soup( resp.text, 'lxml' ) 
except:
	print( "\n\n ###### STARTING RANDOM PROXIES #######" );
	resp = _loadDataByIPRotation( BASE_URL )
	page = soup( resp.text, 'lxml' )

########## EXTRACTING THE TABLE ###########

try:
	table = page.find( "table",{
	  "id": "main_table_countries_today" 
	} )
except:
	print( "\n\n NO DATA RECIEVED !!" )
	exit();

table_heading = [ item.text.strip() for item in table.thead.tr if item != "\n" ]

table_content = []
for rows in table.tbody:
  data = [ item.text.strip() for item in rows if item != "\n" ]
  if data:
    table_content.append( data[ : -2 ] )

table_content.insert( 0, table_heading[ : -2 ] )

table = AsciiTable(table_content)


print(table.table)