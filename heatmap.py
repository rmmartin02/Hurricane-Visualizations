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
longlat = [[0]*(int((maxlat-minlat) * 10)+1) for _ in range(int((maxlong-minlong)*10)+1)]
for key in latlongDict:
	c = key.split(' ')
	longlat[int((float(c[1])-minlong)*10)][int((float(c[0])-minlat)*10)] = latlongDict[key]
	
compressed = [[0]*(int(len(longlat[0])/5)+1) for _ in range(int(len(longlat)/5)+1)]
max = 0
for i in range(0,len(longlat),5):
	for j in range(0,len(longlat[0]),5):
		sum = 0
		for l in range(i,i+5):
			if(l==len(longlat)):
				break
			for k in range(j,j+5):
				if(k == len(longlat[0])):
					break
				sum += longlat[l][k]
		if(sum>max):
			max = sum
		print(len(compressed),len(compressed[0]),int(i/5),int(j/5))
		compressed[int(i/5)][int(j/5)] = sum

for i in compressed:
	for j in i:
		j = float(j)/float(max)

print(compressed)

arr = np.array(compressed)
plt.imshow(arr)
plt.show()
 
#https://pythonspot.com/en/generate-heatmap-in-matplotlib/