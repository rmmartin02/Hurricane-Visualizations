import sys
from Cyclone import Hurricane, TrackPoint
	
	

hurricaneList = []

with open('data/all.csv','r') as f:
	for text in f:
		text = text.replace(" ","").split(",")
		if len(text)>13 and text[13] not in hurricaneList:
			hurricaneList.append(text[13])
	print(hurricaneList)

"""
timeDict = {}
with open(sys.argv[1],'r') as f:
	for text in f:
		text = text.split(",")
		text = text[6].split(" ")
		if(text[1] not in timeDict):
			timeDict[text[1]] = 1
		else:
			timeDict[text[1]] = timeDict[text[1]] + 1
print(sorted(timeDict.items(), key=lambda x:x[1]))
"""
"""
basinList = []
with open(sys.argv[1],'r') as f:
	for text in f:
		text = text.replace(' ','').split(",")
		text = text[16].replace('\n','')
		if(text not in basinList):
			basinList.append(text)
print(basinList)
"""
"""
#how many storms active in a basin at once
dates = {}
hurricaneList = Hurricane.readData(sys.argv[1])
for hurr in hurricaneList:
	for p in hurr.trackPoints:
		if p.time not in dates:
			dates[p.time] = 1
		else:
			dates[p.time] = dates[p.time] + 1
print(sorted(dates.items(), key=lambda x:x[1]))
"""
"""
maxlat = -180
maxlong = -90
minlat = 180
minlong = 90
hurricaneList = Hurricane.readData(sys.argv[1])
for hurricane in hurricaneList:
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
print(maxlat,minlong,minlat,maxlong)
#All 81.0 -180.0 -68.5 180.0
#NA 80.3 -109.5 7.2 28.0
"""
"""
hurricaneList = Hurricane.readData(sys.argv[1])
max = 0
hurr = hurricaneList[0]
for h in hurricaneList:
	ace = h.getACE()
	if ace>max:
		max = ace
		hurr = h
print(max, hurr.name, hurr.season, hurr.serialNumber)
"""