from requests_ntlm import HttpNtlmAuth
import requests
from bs4 import BeautifulSoup
import json
import sys

def getPlans(id): #Performs a post request in order to obtain class plans
	r = requests.post("https://daymap.gihs.sa.edu.au/DayMap/Student/plans/class.aspx?eid=%s" % id, auth=HttpNtlmAuth(sys.argv[1], sys.argv[2]))
	soup = BeautifulSoup(r.text, 'html.parser')
	note = soup.find('div', {'class': 'lpAll'})
	if note != None:
		note = note.text
	if note == None:
		note = "No lesson plans have been entered for this lesson." #Fallback for when there is no lesson plan
	return note

r = requests.get("https://daymap.gihs.sa.edu.au/daymap/student/dayplan.aspx", auth=HttpNtlmAuth(sys.argv[1], sys.argv[2]))
if r.status_code in range(200, 299): #Ensures request is successful
	print("ITWASASUCCESS") #Debug print, removed in PHP
	soup = BeautifulSoup(r.text, 'html.parser')
	diary = soup.find('div', {'class': 'diary'})
	days = []
	for i in soup.findAll('div', {'class': 'diaryDay'}):
		days.append(str(i))
	try:
		diary = str(diary).split(days[1]) #days[1] the second entry in the list in the day that is wanted
		soup = BeautifulSoup(diary[0], 'html.parser')
	except IndexError:
		diary = str(diary).split(days[0]) #days[0] because except on Friday, where this only is one entry in the list.
		soup = BeautifulSoup(diary[0], 'html.parser')
	classes = {} #Beginning to construct a dict for easier parsing Swift side.
	classes["details"] = {}
	classes["classes"] = {}
	classList = [] #Because dicts and JSON are not sorted, and a diary plan has to be sorted, a list is placed into the dict, which will retain order.
	for i in soup.findAll('div', {'class': 'c'}):
		classList.append(i.text) 
	classes["classes"] = classList
	for i in soup.findAll('div', {'data-type': '2'}): #Each lesson in dayplan.aspx has a data-type of 2, so this iterates overthem.
		classID = i['data-id']		
		if classID.isdigit() and len(classID) > 6 and len(classID) < 9: #Ensures the classID is a valid int to protect potential mitm attacks
			note = getPlans(classID)
			classes["details"][i.find('div', {'class': 'c'}).text] = {"id": classID, "class": i.find('div', {'class': 'c'}).text, "note": note.replace('"', "INSERTAPOSTROPHE").replace("'", "INSERTAPOSTROPHE")} #JSON was having a hard time with ' and ". In this case, they are both replaced with the same thing.
	parsedDiary = json.dumps(classes, indent=4, sort_keys=True) #Indent is purely for easier debugging.
	print(parsedDiary)	
elif r.status_code != 200:
	print(r.status_code)
