# Author: Daniel Jones
# Date: 8/27/2020
# Description: Python 3 program demonstrating the use of API calls as well as sorting/categorizing data
# to take a look COVID-19 statistics through the United States. Also you can send the information to your personal
# email account.
# Sources cited:
# https://realpython.com/python-requests/#the-get-request
# https://hotter.io/docs/email-accounts/secure-app-gmail/
# https://stackoverflow.com/questions/17759860/python-2-smtpserverdisconnected-connection-unexpectedly-closed
# https://realpython.com/python-send-email/
# https://trinket.io/python/593ce29761
# https://docs.python.org/3/library/smtplib.html#smtplib.SMTP
# http://patorjk.com/software/taag/#p=display&v=2&f=Doom&t=Main%20Menu

import requests
import json
from collections import namedtuple
from requests.exceptions import HTTPError
import csv
import decimal
import operator
import csv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import getpass

# Setting up the State object to save the data from the API
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

# Simple error handling to make sure the response is good
def checkResponse(resp):
	if resp:
		return True
	else:
		return False

# Checks to make sure the API is still up
def noEndpoint():
	print("Endpoint not found... Exiting")
	exit()

# Allows users to get the information extracted from their file in the Downloads directory
# IMPORTANT: If for some reason you've changed the default of where downloads are saved, the
# 'Downloads' part will need to be chnaged in the below code.
def getPath(resp):
	path = os.path.join(os.getenv('USERPROFILE'), 'Downloads\current.csv')
	return path

# Getting the information from the .csv file into the State object
def initStates(fileObject, statesList):
	startLine = 1
	currentLine = 1
	for line in fileObject:
		if (currentLine < startLine):
			currentLine += 1
		else:
			readCSV = csv.reader(fileObject, delimiter=',')
			counter = 1
			# Adding data from each category into an array for each state
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
	# Main menu where the user can see different information
		print("\n\n                                       MAIN MENU                               \n\n")
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

# Function used after a user makes a choice on which data they want to see
def displayTotalCases(statesList):
	subj = "\n---Total Cases by state---\n"
	print(subj)
	for s in statesList:
		print(s.state + ": "  + s.positiveCases + " cases as of " + s.date + '\n')
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			message += (s.state + ": " + s.positiveCases + " cases as of " + s.date + '\n')
		sendEmail(statesList, message, subj)
 
def displayNegTests(statesList):
	subj = "\n---Negative Tests by state---\n"
	print(subj)
	for s in statesList:
		print(s.state + ": "  + s.negativeCases)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			message += (s.state + ": " + s.negativeCases + " negative tests as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

# Sends an email to the user with the email they entered as well as what they want emailed to them
# Need to figure out a way to have email hardcoded, but not in plaintext so users can see
def sendEmail(statesList, message, subj):
	sender_email = "TheCovid19Analyzer@gmail.com"
	receiver_email = input("Please enter your email: ")
	password = getpass.getpass("Sender's Password: ")
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	login = s.login(sender_email, password)
	msg = MIMEMultipart()
	msg['From'] = sender_email
	msg['To'] = receiver_email
	msg['Subject'] = "COVID-19 Analyzer Results"
	msg.attach(MIMEText(message, 'plain'))
	s.send_message(msg)
	del msg

# This is where the API gets called originally, and the other functions are called to get things done
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
		if choice == '1':
			displayTotalCases(statesList)
		elif choice == '2':
			displayNegTests(statesList)
		elif choice == '3':
			print("Choice 2 chosen")
		elif choice == '4':
			print("Choice 2 chosen")
		elif choice == '5':
			print("Choice 2 chosen")
		elif choice == '6':
			print("Choice 2 chosen")
		elif choice == '7':
			print("Choice 2 chosen")
		elif choice == '8':
			print("Choice 2 chosen")
		elif choice == '9':
			print("Choice 2 chosen")
		elif choice == '11':
			print("Choice 2 chosen")
	print("Thank you for using the Covid-Analyzer!")
if __name__ == "__main__":
	main()