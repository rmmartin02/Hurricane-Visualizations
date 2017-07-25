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

maxWind = 0
minPressure = 2000
for hurr in hurricaneList:
	for point in hurr.trackPoints:
		if(point.wind > maxWind):
			maxWind = point.wind
			maxWindHurr = point.hurricane
		if(point.pressure < minPressure and point.pressure > 0):
			minPressure = point.pressure
			minPressureHurr = point.hurricane
print(maxWindHurr.name + " " + str(maxWindHurr.season) + ": " + str(maxWind) + " " + minPressureHurr.name + " " + str(minPressureHurr.season) + ": " + str(minPressure))