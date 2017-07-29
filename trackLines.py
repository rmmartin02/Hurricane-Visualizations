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

#NEED TO FIX DATA (COASTLINE BIAS, TIME DIFFERENCES)
print("Cleaning data")
times = ['18:00:00','12:00:00','00:00:00','06:00:00']
removed = 0
h = 0
print(len(hurricaneList))
while h < len(hurricaneList):
	t = 0
	while t < len(hurricaneList[h].trackPoints):
		if hurricaneList[h].trackPoints[t].wind<0.0:
			removed += 1
			del hurricaneList[h].trackPoints[t]
		else:
			t = t+1
	if len(hurricaneList[h].trackPoints) == 0 or hurricaneList[h].trackPoints[0].time[5:7]!='08':
		del hurricaneList[h]
	else:
		h = h + 1
print("Removed " + str(removed) + " points from data")
print(len(hurricaneList))
		
map = Map("images\worldMap.jpg", 90.0, -180.0, -90.0, 180.0)
maxlat = -180
maxlong = -90
minlat = 180
minlong = 90
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
		if (newlong>90 and oldlong<-90) or (oldlong>90 and newlong<-90):
			print("over date line")
		else:
			map.drawLine((255,0,0,),1,oldlat,oldlong,newlat,newlong)
		oldlat = newlat
		oldlong = newlong
map = map.getSubMap(maxlat, minlong, minlat, maxlong)
map.view()