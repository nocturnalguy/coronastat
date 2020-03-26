########### IMPORTING THE REQURIED LIBRARIES ###########

from .corona import Corona
from .utils import *
import sys

######### DRIVER METHOD ##########

def main():
	corona = Corona();
	args = sys.argv

	displayLoadingAnim()
	displayASCIIArt()

	if( len( args ) == 1 or args[ 1 ] == "-h" or args[ 1 ] == "--help" ):
		displayHelp()
	elif( args[ 1 ] == "-w" or args[ 1 ] == "--world" ):
		displayWorldInfo( corona )
	elif( args[ 1 ] == "-c" or args[ 1 ] == "--country" ):
		displayCountryInfo( corona )

if __name__ == "__main__":
	main()
