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

with open('stormdata.csv','r') as f:
	for text in f:
		text = text.replace(" ","").split(",")
		if(text[7] not in hurricaneList):
			hurricaneList.append(text[7])
	print(hurricaneList)
