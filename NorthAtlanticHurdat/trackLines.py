import sys
from Map import Map
from Cyclone import Hurricane, TrackPoint
	

hurricaneList = Hurricane.readData(sys.argv[1])

#NEED TO FIX DATA (COASTLINE BIAS, TIME DIFFERENCES)
print("Cleaning data")
times = ['18:00:00','12:00:00','00:00:00','06:00:00']
removed = 0
h = 0
print(len(hurricaneList))
while h < len(hurricaneList):
	t = 0
	#164 is "cat 6"
	hurDel = hurricaneList[h].didLandfall()
	#hurDel = False
	while t < len(hurricaneList[h].trackPoints):
		#hurricaneList[h].trackPoints[t].time[10:] not in times
		#hurricaneList[h].trackPoints[t].pressure>900 or hurricaneList[h].trackPoints[t].pressure<800
		if hurricaneList[h].trackPoints[t].wind<=0.0:
			removed += 1
			del hurricaneList[h].trackPoints[t]
		else:
			t = t+1
	# or hurricaneList[h].trackPoints[0].time[5:7]!='08'
	if len(hurricaneList[h].trackPoints) == 0 or not hurDel:
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
	oldPoint = hurricane.trackPoints[0]
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
		if (newlong>90 and oldPoint.longitude<-90) or (oldPoint.longitude>90 and newlong<-90):
			print("over date line")
		elif(oldPoint.getColor()!=(0,0,0)):
			map.drawLine(oldPoint.getColor(),1,oldPoint.latitude,oldPoint.longitude,newlat,newlong)
		oldPoint = point
print(maxlat,minlat,maxlong,minlong)
map = map.getSubMap(maxlat, minlong, minlat, maxlong)
map.mapImage = map.mapImage.convert("RGB")
if len(sys.argv)>2:
	map.save("images/TrackLines/"+sys.argv[2])
else:
	map.view()