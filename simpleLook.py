import sys
class TrackPoint:
		def __init__(self, hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType):
			self.hurricane = hurricane
			self.time = time
			self.nature = nature
			self.latitude = latitude
			self.longitude = longitude
			self.wind = wind
			self.pressure = pressure
			self.center = center
			self.trackType = trackType

class Hurricane:

	def __init__(self, serialNumber, season, num, basin, subBasin, name):
		self.serialNumber = serialNumber
		self.season = season
		self.num = num
		self.basin = basin
		self.subBasin = subBasin
		self.name = name
		self.trackPoints = []
		
	def addTrackPoint(self, hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType):
		self.trackPoints.append(TrackPoint(hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType))
	
	
"""
hurricaneList = []

with open('stormdata.csv','r') as f:
	for text in f:
		text = text.replace(" ","").split(",")
		if(text[7] not in hurricaneList):
			hurricaneList.append(text[7])
	print(hurricaneList)
"""
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
basinDict = {}
with open(sys.argv[1],'r') as f:
	for text in f:
		text = text.split(",")
		if(text[3] not in basinDict):
			basinDict[text[3]] = 1
		else:
			basinDict[text[3]] = basinDict[text[3]] + 1
print(sorted(basinDict.items(), key=lambda x:x[1]))