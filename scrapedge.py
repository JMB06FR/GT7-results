# 2025-05-15
# Python 3.11.9
# Small scraper for the https:/www.dg-edge.com/players/PLAYERID pages allowing to get all the results of the events for a player
# Will create a csv file which can be imported in excel and then you can see your progress :)
# Dislaimer: Provided as it is :)
# Feel free to make it better !!!
# Author: Jean-Michel Becar jm@becar.com
#
#
# Note: Sometimes when importing the csv file in Excel the columns DeltaGPerc and DeltaLocalP are not well formatted to percentage 
# Just format those 2 columns to percentage and that will fix it


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

# Extract the values from a list recursively
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

# total arguments
n = len(sys.argv)

# check if we have all the arguments we have the player and the name of the file
if n < 3:
	print('\n usage: python scrapedge.py playerID ouputfile.csv')
else:

	# Arguments passed
	# should be the pseudo used in GT7 and not the PSN ID
	player = sys.argv[1]
	outputFile = sys.argv[2]

	# initiate the numbe rof lines we will write in the file
	mline = 0

  	# if the output file doesn't exist it will be created with the header line titles
	if not os.path.isfile(outputFile):  
		with open(outputFile, "a", encoding='utf-8') as result_file: 
			result_file.write('Date'+'|'+'Week'+'|'+'Year'+'|'+'Event'+'|'+'Type'+'|'+'Group'+'|'+'Tyres'+'|'+'Track'+'|'+'Car'+'|'+'GPosition'+'|'+'CPosition'+'|'+'lapTime'+'|'+'DeltaG'+'|'+ 'DeltaGPerc'+'|'+'DeltaL'+'|'+'DeltaLocalP'+'|Player')   

	# if the file already exist the lines will be concatanated one after each other
	# one line per event  
	with open(outputFile, "a", encoding='utf-8') as result_file: 
	
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
		
			# let's see how many pages that player has
			lastPage = get_vals(data, 'lastPage')
			lastPage = lastPage [0]
			
			# let's show some progress to the user
			print('...')
		
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

			for i in range(len(week)):
				myLine = '\n'+ str(eventDate[i]) +'|'+ str(week[i])+'|'+str(year[i])+'|'+str(eventType[i])+'|'+str(dailyType[i])+'|'+str(carType[i])+'|'+str(tyres[i])+'|'+str(fullName[i])+'|'+str(carName[i])+'|'+str(globalPosition[i])+'|'+str(countryPosition[i])+'|'+str(lapTime[i])+'s|'+str(deltaGlobal[i])+'s|'+ str(deltaGlobalPerc[i])+'%|'+str(deltaLocal[i])+'s|'+str(deltaLocalPerc[i])+'%|'+ player 
				mline = mline+1
				result_file.write(myLine)
		
