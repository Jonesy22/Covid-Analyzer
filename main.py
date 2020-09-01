# Author: Daniel Jones
# Date: 8/27/2020
# Description: Small python3 program demonstrating the use of API calls as well as sorting/categorizing data
# to take a look COVID-19 statistics through the United States. 
# Sources cited:
# https://realpython.com/python-requests/#the-get-request
import requests
from requests.exceptions import HTTPError
import csv
import decimal
import operator
import json
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
		print("Successful GET request.")
	else:
		print("Endpoint not found.")
	return resp


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

def userMenu(fileObject, statesList):
	tempVar = 2
	
def main():
	statesList = []
	resp = requests.get('https://api.covidtracking.com/v1/states/current.csv')
	checkResponse(resp)
	fileObject = open(getPath(resp), "r")
	initStates(fileObject, statesList)
	userMenu(fileObject, statesList)


if __name__ == "__main__":
	main()