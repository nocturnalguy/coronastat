########### IMPORTING THE REQURIED LIBRARIES ###########

from __future__ import print_function
from terminaltables import AsciiTable
import sys, time

########## DECLARING THE GLOBAL VARIABLES #############

WORLD_URL = "https://www.worldometers.info/coronavirus"
INDIA_URL = "https://www.mohfw.gov.in/"
MAX_TIMEOUT = 3
PROXY_TIMEOUT = 3

########## DECLARING STYLES ##########

class style:
	PURPLE = "\033[95m"
	CYAN = "\033[96m"
	DARKCYAN = "\033[36m"
	BLUE = "\033[94m"
	GREEN = "\033[92m"
	YELLOW = "\033[93m"
	RED = "\033[91m"
	BOLD = "\033[1m"
	UNDERLINE = "\033[4m"
	ITALIC = "\033[3m"
	END = "\033[0m"

######### EXTRACTING NUMBER FROM STRING  #########

def extractNumbers( string ):
	dig = ""
	for c in string: 
		if c.isdigit():
			dig += c
	return dig

######### DISPLAYING THE COUNTRYWISE STATISTICS #########

def displayWorldInfo( corona ):
	print( "\nFetching data. Please wait...\n" );
	page = corona.getPageResponse( WORLD_URL )
	if not page:
		print( "\nSorry, couldn't fetch any information for you." )
		print( "\nMaybe you don't have a working internet connection or\nthe source are blocking the application\n" )
		exit()
	counts = corona.extractCounts( page, "w" )
	table = corona.extractTableData( page, "w" )
	print( style.RED + style.BOLD + counts.table + style.END + "\n" )
	print( table.table )

######### DISPLAYING THE STATEWISE STATISTICS #########

def displayCountryInfo( corona ):
	print( "\nFetching data. Please wait...\n" );
	page = corona.getPageResponse( INDIA_URL )
	if not page:
		print( "\nSorry, couldn't fetch any information for you." )
		print( "\nMaybe you don't have a working internet connection or\nthe source are blocking the application\n" )
		exit()
	counts = corona.extractCounts( page, "c" )
	table = corona.extractTableData( page, "c" )
	print( style.RED + style.BOLD + counts.table + style.END + "\n" )
	print( table.table )

######### DISPLAYING THE HELP #########

def displayHelp():
	print( "\nUsage : coronastat [ OPTIONS ]\n" );
	print( "Commands : " );
	table = [
		[ "Options", "Functions" ],
		[ "-h, --help", "Opens the help for this CLI tool." ],
		[ "-c, --country", "Opens statewise COVID-19 statistics ( only India's data is possible till now )." ],
		[ "-w, --world", "Opens countrywise COVID-19 statistics." ]
	]

	table = AsciiTable( table )
	print( table.table )

######### DISPLAYING THE ASCII ART #########

def displayASCIIArt():
	print( 
		style.CYAN + style.ITALIC + style.BOLD + 
		'''\n
	
   ██████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗ █████╗ ███████╗████████╗ █████╗ ████████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██████╔╝██║   ██║██╔██╗ ██║███████║███████╗   ██║   ███████║   ██║   
  ██║     ██║   ██║██╔══██╗██║   ██║██║╚██╗██║██╔══██║╚════██║   ██║   ██╔══██║   ██║   
  ╚██████╗╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║██║  ██║███████║   ██║   ██║  ██║   ██║   
   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   
   Developed by: Rahul Gupta                                                                                   
		\n'''
		+ style.END
	);

######### DISPLAYING THE LOADING ANIMATION #########

def displayLoadingAnim():
	for _ in range( 3 ):
		loader="\\|/-\\|/-"
		for l in loader:
			sys.stdout.write( l )
			sys.stdout.flush()
			sys.stdout.write( '\b' )
			time.sleep( 0.2 )