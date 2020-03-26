########### IMPORTING THE REQURIED LIBRARIES ###########

from setuptools import setup

########### READING THE README.md FILE ###########

def getReadmeFileContents():
	with open( "README.md" ) as file:
		contents = file.read()
	return contents

########### SETTING UP THE NECESSARY PACKAGE DESCRIPTION ###########

setup(
	name = "coronastat",
	version = "1.0.0",
	description = "A python package to display countrywise and statewise ( India ) statistics of coronavirus ( COVID-19 ) in the terminal in tabular fashion",
	long_description = getReadmeFileContents(),
	long_description_content_type = "text/markdown",
	url = "https://github.com/theNocturnalGuy/coronastat",
	author = "Rahul Gupta",
	author_email = "rahulgupta0097@gmail.com",
	license = "MIT",
	classifiers = [
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.7",
	],
	packages = [ "corona" ],
	include_package_data = True,
	install_requires = [ "requests", "terminaltables", "bs4" ],
	entry_points = {
		"console_scripts": [
			"coronastat = corona.__init__:main",
		]
	}
)