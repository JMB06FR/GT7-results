# 2025-05-15
# Python 3.11.9
# Small scraper for the https:/www.dg-edge.com/players/PLAYERID pages allowing to get all the results of the events for a player
# Will create a csv file which can be imported in excel and then you can see your progress
# Dislaimer: Provided as it is :)
# Feel free to make it better !!!
#
# Author: Jean-Michel Becar jm@becar.com  JMB06FR
#
#
# Note: Sometimes when importing the csv file in Excel the columns DeltaGPerc and DeltaLocalP are not well formatted to percentage 
# Just format those 2 columns to percentage with 2 decimals and that will fix it
#
# 20/05/2025 JMB Added the progress bar 
# 21/05/2025 JMB Added the test if player exists or not 
# 22/05/2025 JMB Added close of the file and a nicer error messages

#!/usr/bin/python3
import requests
import sys
import os
from urllib.request import Request, urlopen
from pprint import pprint
from pyquery import PyQuery

# The API endpoint
url = "https://admin.dg-edge.com/api/b.players.retrievePlayerEvents"

# Data to be sent
params = {
    "onlineId": "",
    "page": 1,
    "language": "EN",
    "version": 90,
    "cookieVersion": "",
    "ajax_referer": "",
    "ss_id": "lmbjgjrmvk6o4cjifpdnp059jh"
}

#
# Extract the values from a list recursively
#
def get_vals(nested, key):
    result = []
    if isinstance(nested, list) and nested != []:   #non-empty list
        for lis in nested:
            result.extend(get_vals(lis, key))
    elif isinstance(nested, dict) and nested != {}:   #non-empty dict
        for val in nested.values():
            if isinstance(val, (list, dict)):   #(list or dict) in dict
                result.extend(get_vals(val, key))
        if key in nested.keys():   #key found in dict
            result.append(nested[key])
    return result

#
# Simple progress bar
#
def progressbar(current_value,total_value,bar_lengh,progress_char): 
    percentage = int((current_value/total_value)*100)                                                # Percent Completed Calculation 
    progress = int((bar_lengh * current_value ) / total_value)                                       # Progress Done Calculation 
    loadbar = "Progress: [{:{len}}]{}%".format(progress*progress_char,percentage,len = bar_lengh)    # Progress Bar String
    print(loadbar, end='\r')      

#
# Main part of the script 
#
if __name__ == "__main__":

	# check if we have all the arguments we have the player and the name of the file
	if len(sys.argv) < 3:
		print('Oops! we are missing parameters: python scrapedge.py playerID ouputfile.csv')
		exit()

	# Arguments passed
	# should be the pseudo used in GT7 and not the PSN ID
	player = sys.argv[1]
	outputFile = sys.argv[2]

	# if the output file doesn't exist it will be created with the header line titles
	if not os.path.isfile(outputFile):  
		with open(outputFile, "a", encoding='utf-8') as result_file: 
			result_file.write('Date'+'|'+'Week'+'|'+'Year'+'|'+'Event'+'|'+'Type'+'|'+'Group'+'|'+'Tyres'+'|'+'Track'+'|'+'Car'+'|'+'GPosition'+'|'+'CPosition'+'|'+'lapTime'+'|'+'DeltaG'+'|'+ 'DeltaGPerc'+'|'+'DeltaL'+'|'+'DeltaLocalP'+'|Player')   

	# if the file already exist the lines will be concatanated one after each other
	# one line per event  
	with open(outputFile, "a", encoding='utf-8') as result_file: 
	
		# Let's prepare the paramaters for the API call
		params['onlineId'] = player
		params['ajax_referer'] = "/players/" + player
		lastPage = params['page']
		p = 0
		while p < (int(lastPage)):
			p=p+1
			params["page"] = p
		
			# A POST request to the API
			response = requests.post(url, json=params)
		
			# Get the response
			data = response.json()
		
			# let's see how many pages of results that player has
			# and test if the player exists or not
			lastPage = get_vals(data, 'lastPage')
			if len(lastPage):
				lastPage = lastPage [0]
			else:
				print('Oops! That player doesn\'t look like it exists. Try again ....')
				exit()
				
			# let's show some progress to the user
			progressbar(p,lastPage,30,'■')
		
			# Extract the data 
			week = get_vals(data, 'week')
			year = get_vals(data, 'year')
			eventDate = get_vals(data, 'timestamp') 
			eventType = get_vals(data, 'eventType')	
			dailyType = get_vals(data, 'dailyType')
			carType = get_vals(data, 'carType')
			tyres = get_vals(data, 'tyres')
			track = get_vals(data, 'track')
			fullName = get_vals(track, 'fullName')
			car = get_vals(data, 'playerResult')
			carName = get_vals(car,'name')
			globalPosition = get_vals(data, 'globalPosition')
			countryPosition = get_vals(data, 'countryPosition')
			lapTime = get_vals(data, 'time')
			deltaGlobal = get_vals(data, 'deltaGlobal')
			deltaGlobalPerc = get_vals(data, 'deltaGlobalPerc')
			deltaLocal = get_vals(data, 'deltaLocal')
			deltaLocalPerc = get_vals(data, 'deltaLocalPerc')

			# Write the data into the output file
			for i in range(len(week)):
				myLine = '\n'+ str(eventDate[i]) +'|'+ str(week[i])+'|'+str(year[i])+'|'+str(eventType[i])+'|'+str(dailyType[i])+'|'+str(carType[i])+'|'+str(tyres[i])+'|'+str(fullName[i])+'|'+str(carName[i])+'|'+str(globalPosition[i])+'|'+str(countryPosition[i])+'|'+str(lapTime[i])+'s|'+str(deltaGlobal[i])+'s|'+ str(deltaGlobalPerc[i])+'%|'+str(deltaLocal[i])+'s|'+str(deltaLocalPerc[i])+'%|'+ player 
				result_file.write(myLine)

		# The End.
		result_file.close()
		print('\nEnjoy your data!\n')
		exit()
		
