import numpy as np
import numpy.random
import matplotlib.pyplot as plt

import sys
from Map import Map
from Cyclone import Hurricane, TrackPoint
	

hurricaneList = []

with open(sys.argv[1],'r') as f:
	tempSerNum = ""
	hurrNum = -1
	for text in f:
		text = text.replace(" ","").split(",")
		if(text[0] != tempSerNum):
			hurrNum += 1
			hurricaneList.append(Hurricane(text[0], int(text[1]), int(text[2]), text[3], text[4], text[5]))
			tempSerNum = text[0]
		hurricaneList[hurrNum].addTrackPoint(hurricaneList[hurrNum], text[6], text[7], float(text[8]), float(text[9]), float(text[10]), float(text[11]), text[12], text[15])

map = Map("worldMap.jpg", 90.0, -180.0, -90.0, 180.0)
maxlat = -180
maxlong = -90
minlat = 180
minlong = 90
latlongDict = {}
for hurricane in hurricaneList:
	oldlat = hurricane.trackPoints[0].latitude
	oldlong = hurricane.trackPoints[0].longitude
	for point in hurricane.trackPoints:
		newlat = point.latitude
		newlong = point.longitude
		if(newlat>maxlat):
			maxlat = newlat
		elif(newlat<minlat):
			minlat = newlat
		if(newlong>maxlong):
			maxlong = newlong
		elif(newlong<minlong):
			minlong = newlong
		map.drawPoint((255,0,0),newlat,newlong)
		
		key = str(newlat) + ' ' + str(newlong)
		if(key in latlongDict):
			latlongDict[key] = latlongDict[key] + 1
		else:
			latlongDict[key] = 1
	 	
		oldlat = newlat
		oldlong = newlong
map = map.getSubMap(maxlat, minlong, minlat, maxlong)
#map.view()

#construct 2d array of all possible lat,long positions
#then go through points and count how many are at each position
latlong = [[0]*int((maxlat-minlat) * 10) for _ in range(int(maxlong-minlong)*10)]

	
print(latlong)
 
#https://pythonspot.com/en/generate-heatmap-in-matplotlib/