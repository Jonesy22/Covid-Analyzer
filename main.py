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
		self.dataGrade = dataGrade
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
		print("8) Total Deaths (All states)")
		print("9) Choose a state to analyze")
		print("0) Exit the analyzer")
		choice = input("--> ")
		return choice

# Function used after a user makes a choice on which data they want to see
def displayTotalCases(statesList):
	subj = "\n---Total Cases by state---\n"
	print(subj)
	for s in statesList:
		if s.positiveCases < '1':
			s.positiveCases = 'N/A'
		print(s.state + ": "  + s.positiveCases + " cases as of " + s.date + '\n')
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.positiveCases < '1':
				s.positiveCases = 'N/A'
			message += (s.state + ": " + s.positiveCases + " cases as of " + s.date + '\n')
		sendEmail(statesList, message, subj)
 
def displayNegTests(statesList):
	subj = "\n---Negative Tests by state---\n"
	print(subj)
	for s in statesList:
		if s.negativeCases < '1':
			s.negativeCases = 'N/A'
		print(s.state + ": "  + s.negativeCases)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.negativeCases < '1':
				s.negativeCases = 'N/A'
			message += (s.state + ": " + s.negativeCases + " negative tests as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

def currentlyHospitalized(statesList):
	subj = "\n---Currently Hospitalized---\n"
	print(subj)
	for s in statesList:
		if s.currentHosp < '1':
			s.currentHosp = 'N/A'
		print(s.state + ": "  + s.currentHosp)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.currentHosp < '1':
				s.currentHosp = 'N/A'
			message += (s.state + ": " + s.currentHosp + " currently hospitalized as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

def totalHospitalized(statesList):
	subj = "\n---Total Hospitalized---\n"
	print(subj)
	for s in statesList:
		if s.totalHosp < '1':
			s.totalHosp = 'N/A'
		print(s.state + ": "  + s.totalHosp)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.totalHosp < '1':
				s.totalHosp = 'N/A'
			message += (s.state + ": " + s.totalHosp + " total hospitalized as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

def currentICU(statesList):
	subj = "\n---Currently in ICU---\n"
	print(subj)
	for s in statesList:
		if s.currentICU < '1':
			s.currentICU = 'N/A'
		print(s.state + ": "  + s.currentICU)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.currentICU < '1':
				s.currentICU = 'N/A'
			message += (s.state + ": " + s.currentICU + " currently in ICU as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

def totalICU(statesList):
	subj = "\n---Total in ICU---\n"
	print(subj)
	for s in statesList:
		if s.totalICU < '1':
			s.totalICU = 'N/A'
		print(s.state + ": "  + s.totalICU)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.totalICU < '1':
				s.totalICU = 'N/A'
			message += (s.state + ": " + s.totalICU + " total in ICU as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

def totalRecovered(statesList):
	subj = "\n---Total Recovered---\n"
	print(subj)
	for s in statesList:
		if s.reocvered < '1':
			s.recovered = 'N/A'
		print(s.state + ": "  + s.recovered)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.recovered < '1':
				s.recovered = 'N/A'
			message += (s.state + ": " + s.recovered + " total in ICU as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

def totalDeaths(statesList):
	subj = "\n---Total Deaths---\n"
	print(subj)
	for s in statesList:
		if s.deaths < '1':
			s.deaths = 'N/A'
		print(s.state + ": "  + s.deaths)
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		message = ''
		for s in statesList:
			if s.deaths < '1':
				s.deaths = 'N/A'
			message += (s.state + ": " + s.deaths + " total in ICU as of " + s.date + '\n')
		sendEmail(statesList, message, subj)

def analyzeState(statesList):
	stateChosen = input("Which state would you like to see the stats of? (EX: WA/wa/Wa/wA, not case sensitive): ").upper()
	print("\n---Statistics for the state of " + stateChosen + "---\n")
	for s in statesList:
		if stateChosen == s.state:
			if s.positiveCases < '1': s.positiveCases = "N/A"
			if s.negativeCases < '1': s.negativeCases = "N/A"
			if s.currentHosp < '1': s.currentHosp = "N/A"
			if s.totalHosp < '1': s.totalHosp = "N/A"
			if s.currentICU < '1': s.currentICU = "N/A"
			if s.totalICU < '1': s.totalICU = "N/A"
			if s.recovered < '1': s.recovered = "N/A"
			if s.deaths < '1': s.deaths = "N/A"
			print("Total positive cases: " + s.positiveCases)
			print("Negative tests: " + s.negativeCases)
			print("Currently in hospital: " + s.currentHosp)
			print("Total hospitalized: " + s.totalHosp)
			print("Currently in ICU: " + s.currentICU)
			print("Total in ICU: " + s.totalICU)
			print("Total recovered: " + s.recovered)
			print("Total deaths: " + s.deaths)
			print("Data quality/Reliability grade: " + s.dataGrade + "\n")
	yesOrNo = input("\nWould you like to receive an email with this information? (Y/N): ").lower()
	if yesOrNo == "y":
		for s in statesList:
			if stateChosen == s.state:
				if s.positiveCases < '1': s.positiveCases = "N/A"
				if s.negativeCases < '1': s.negativeCases = "N/A"
				if s.currentHosp < '1': s.currentHosp = "N/A"
				if s.totalHosp < '1': s.totalHosp = "N/A"
				if s.currentICU < '1': s.currentICU = "N/A"
				if s.totalICU < '1': s.totalICU = "N/A"
				if s.recovered < '1': s.recovered = "N/A"
				if s.deaths < '1': s.deaths = "N/A"
				subj = ''
				message = ''
				message += ("---Statistics for the state of " + stateChosen + "---" + "\nTotal positive cases: " + s.positiveCases + "\nNegative tests: " + s.negativeCases + "\nCurrently in hospital: " + s.currentHosp + 
				"\nTotal hospitalized: " + s.totalHosp + "\nCurrently in ICU: " + s.currentICU + "\nTotal in ICU: " + s.totalICU + "\nTotal recovered: " + s.recovered + 
				"\nTotal deaths: " + s.deaths + "\nData quality/Reliability grade: " + s.dataGrade + "\n")
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
	sendSuccessful = s.send_message(msg)
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
			currentlyHospitalized(statesList)
		elif choice == '4':
			totalHospitalized(statesList)
		elif choice == '5':
			currentICU(statesList)
		elif choice == '6':
			totalICU(statesList)
		elif choice == '7':
			totalRecovered(statesList)
		elif choice == '8':
			totalDeaths(statesList)
		elif choice == '9':
			analyzeState(statesList)
	print("Thank you for using the Covid-Analyzer!")
if __name__ == "__main__":
	main()