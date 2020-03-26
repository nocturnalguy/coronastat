########### IMPORTING THE REQURIED LIBRARIES ###########

from __future__ import print_function
from bs4 import BeautifulSoup as soup
from random import choice
from terminaltables import AsciiTable
from .proxy import _proxy
from .utils import *
import requests

######## DECLARING THE CLASS FOR GETTING COVID-19 DATA ########

class Corona:
	proxy = _proxy()

	######## GETTING THE HTML PAGE THROUGH GET REQUEST ########

	def getPageResponse( self, url ):
		page = None
		try:
		  resp = requests.get( url, timeout = MAX_TIMEOUT )
		  page = soup( resp.text, 'lxml' ) 
		except requests.ConnectionError:
			print( "\n###### STARTING RANDOM PROXIES #######\n" );
			resp = self.proxy.loadDataByIPRotation( url )
			page = soup( resp.text, 'lxml' )

		return page

	def extractCounts( self, page, choice = "w" ):
		total_cases = None
		total_deaths = None
		total_cured = None

		if( choice == "w" ):
			total_cases = page.findAll( "div", {
				"id": "maincounter-wrap"
			} )[ 0 ].div.text.strip()

			total_deaths = page.findAll( "div", {
				"id": "maincounter-wrap"
			} )[ 1 ].div.text.strip()

			total_cured = page.findAll( "div", {
				"id": "maincounter-wrap"
			} )[ 2 ].div.text.strip()

		elif( choice == "c" ):
			total_cases = int( extractNumbers( page.findAll( "div",{
				"class": "table-responsive" 
			} )[ 7 ].tbody.findAll( "tr" )[ -2 : -1 ][ 0 ].findAll( "td" )[ 1 ].text.strip() ) )

			total_cases += int( page.findAll( "div",{
				"class": "table-responsive" 
			} )[ 7 ].tbody.findAll( "tr" )[ -2 : -1 ][ 0 ].findAll( "td" )[ 2 ].text.strip() )

			total_deaths = int( page.findAll( "div",{
				"class": "table-responsive" 
			} )[ 7 ].tbody.findAll( "tr" )[ -2 : -1 ][ 0 ].findAll( "td" )[ 4 ].text.strip() )

			total_cured = int( page.findAll( "div",{
				"class": "table-responsive" 
			} )[ 7 ].tbody.findAll( "tr" )[ -2 : -1 ][ 0 ].findAll( "td" )[ 3 ].text.strip() )

		counts = AsciiTable( [ 
			[ "Total Cases", "Total Deaths", "Total Cured" ],
			[ total_cases, total_deaths, total_cured ]
		] )
		return counts

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

				table_heading = [ "Country", "Confirmed\nCases", "New Cases", "Confirmed\nDeaths", "New Deaths", "Recovered", "Active cases", "Serious/\nCritical cases" ];

				table_content = []
				for rows in table.tbody:
				  data = [ item.text.strip() for item in rows if item != "\n" ]
				  if data:
				    table_content.append( data[ : -2 ] )

				table_content.insert( 0, table_heading )
				table = AsciiTable( table_content )
			except:
				print( "\nSource page format has changed." )
				exit();

		elif choice == "c":
			try:
				table = page.findAll( "div",{
					"class": "table-responsive" 
				} )[ 7 ]

				# table_heading = [ item.text.strip() for item in table.thead.tr if item != "\n" ]

				table_heading = [ "Sl. No.", "States/\nUnion Territories", "Confirmed cases\n( Indian National )", "Confirmed cases\n( Foreign National )", "Cured/Discharged/\nMigrated", "Death" ];

				table_content = []
				for rows in table.tbody:
				  data = [ item.text.strip() for item in rows if item != "\n" ]
				  if data:
				    table_content.append( data )

				table_content.insert( 0, table_heading )
				table = AsciiTable( table_content[ : -2 ] )
			except:
				print( "\nSource page format has changed." )
				exit();
		return table

