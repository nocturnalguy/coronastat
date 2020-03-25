########### IMPORTING THE REQURIED LIBRARIES ###########

from __future__ import print_function
from bs4 import BeautifulSoup as soup
from random import choice
from utils import PROXY_TIMEOUT 
import requests

######## DECLARING THE CLASS FOR SCRAPING SSLPROXIES.COM ########

class _proxy:

	PROXY_URL = 'https://sslproxies.org/'
	page = None

	def __init__( self ):
		self.page = soup( requests.get( self.PROXY_URL ).text, 'lxml' )
    
	def _getSSLProxyDictionary( self ):
 
		return {
		'https': choice( list( map( lambda x:x[ 0 ] + ':' + x[ 1 ], list( zip( map( lambda x:x.text, self.page.find( 'table' ).findAll( 'td' )[ :: 8 ] ), map( lambda x:x.text, self.page.find( 'table' ).findAll( 'td' )[ 1 :: 8 ] ) ) ) ) ) )
		}

	######## DEFINING THE PROXY ROTATION METHOD ##########
	
	def loadDataByIPRotation( self, url ):
		count = 0
		response = None
		while count < 10:
			try:
				proxy_dictionary = self._getSSLProxyDictionary()
				print( 'Retry {} Using Proxy : {}'.format( count, proxy_dictionary ) )
				response = requests.get( url, proxies = proxy_dictionary, timeout = PROXY_TIMEOUT )
				break
			except:
				pass
			count=count+1
		return response


