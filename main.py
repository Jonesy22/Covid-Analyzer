# Author: Daniel Jones
# Date: 8/27/2020
# Description: Python 3 program demonstrating the use of API calls as well as sorting/categorizing data
# to take a look COVID-19 statistics through the United States. 
# Sources cited:
# https://realpython.com/python-requests/#the-get-request
import requests
from requests.exceptions import HTTPError
import csv
import decimal
import operator
import csv
import os

class State():
	def __init__(self, date, state, positiveCases, negative, currentHosp, totalHosp, currentICU, totalICU,
					recovered, dataGrade, deaths, totalTests):
		self.date = date
		self.state = state
		self.positiveCases = positiveCases
		self.negativeCases = negative
		self.currentHosp = currentHosp
		self.totalHosp = totalHosp
		self.currentICU = currentICU
		self.totalICU = totalICU
		self.recovered = recovered
		self.dateGrade = dataGrade
		self.deaths = deaths
		self.totalTests = totalTests

def checkResponse(resp):
	if resp:
		return True
	else:
		return False

def noEndpoint():
	print("Endpoint not found... Exiting")
	exit()

def getPath(resp):
	path = os.path.join(os.getenv('USERPROFILE'), 'Downloads\current.csv')
	return path

def initStates(fileObject, statesList):
	startLine = 1
	currentLine = 1
	for line in fileObject:
		if (currentLine < startLine):
			currentLine += 1
		else:
			readCSV = csv.reader(fileObject, delimiter=',')
			counter = 1
			for row in readCSV:
				statesList.append( State(row[0], row[1], row[2], row[3], row[5], row[6], row[7], row[8], row[11], row[12], row[16], row[19]))
				counter += 1
	return statesList


def welcomeScreen():
	print(""" _   _  _____    _____            _     _             ___              _                    
| | | |/  ___|  /  __ \          (_)   | |           / _ \            | |                   
| | | |\ `--.   | /  \/ _____   ___  __| |  ______  / /_\ \_ __   __ _| |_   _ _______ _ __ 
| | | | `--. \  | |    / _ \ \ / / |/ _` | |______| |  _  | '_ \ / _` | | | | |_  / _ \ '__|
| |_| |/\__/ /  | \__/\ (_) \ V /| | (_| |          | | | | | | | (_| | | |_| |/ /  __/ |   
 \___(_)____(_)  \____/\___/ \_/ |_|\__,_|          \_| |_/_| |_|\__,_|_|\__, /___\___|_|   
                                                                          __/ |             
                                                                         |___/          """)
def userMenu():
		
		print("                                       MAIN MENU                               ")
		print("1) Total Cases (All states)")
		print("2) Negative Tests (All states)")
		print("3) Currently Hospitalized (All states)")
		print("4) Total Hospitalized (All states)")
		print("5) Current in ICU (All states)")
		print("6) Total in ICU (All states)")
		print("7) Total Recovered (All states)")
		print("8) Total Hospitalized (All states)")
		print("9) Total Deaths (All states)")
		print("10) Total Deaths (All states)")
		print("11) Choose a state to analyze")
		print("0) Exit the analyzer")
		choice = input("--> ")
		return choice

def displayData(choice, statesList):
	if choice == '1':
		for s in statesList:
			print(s.state + ": "  + s.positiveCases)

def main():
	statesList = []
	choice = '15'
	resp = requests.get('https://api.covidtracking.com/v1/states/current.csv')
	if (not checkResponse(resp)):
		noEndpoint()
	fileObject = open(getPath(resp), "r")
	initStates(fileObject, statesList)
	welcomeScreen()
	while choice != '0':
		choice = userMenu() 
		displayData(choice, statesList)

if __name__ == "__main__":
	main()