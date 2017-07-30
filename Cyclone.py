class TrackPoint:
		def __init__(self, hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType, currentBasin):
			self.hurricane = hurricane
			self.time = time
			self.nature = nature
			self.latitude = latitude
			self.longitude = longitude
			self.wind = wind
			self.pressure = pressure
			self.center = center
			self.trackType = trackType
			self.currentBasin = currentBasin
    

class Hurricane:

	def __init__(self, serialNumber, season, num, basin, subBasin, name):
		self.serialNumber = serialNumber
		self.season = season
		self.num = num
		self.basin = basin
		self.subBasin = subBasin
		self.name = name
		self.trackPoints = []
		
	def addTrackPoint(self, hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType, currentBasin):
		self.trackPoints.append(TrackPoint(hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType, currentBasin))
	
	def getMaxWind(self):
		max = 0
		for point in self.trackPoints:
			if(point.wind>max):
				max = point.wind
		return max
	
	def readData(data):
		hurricaneList = []
		with open(data,'r') as f:
			tempSerNum = ""
			hurrNum = -1
			for text in f:
				text = text.replace(" ","").split(",")
				if(text[0] != tempSerNum):
					hurrNum += 1
					#serialNumber, season, num, basin, subBasin, name
					hurricaneList.append(Hurricane(text[0], int(text[1]), int(text[2]), text[3], text[4], text[5]))
					tempSerNum = text[0]
				#hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType
				time = text[6]
				nature = text[7]
				latitude = float(text[14])
				longitude = float(text[15])
				wind = float(text[8])
				pressure = float(text[9])
				center =  text[10]
				trackType = text[13]
				currentBasin = text[16]
				hurricaneList[hurrNum].addTrackPoint(hurricaneList[hurrNum], time, nature, latitude, longitude, wind, pressure, center, trackType, currentBasin)
		return hurricaneList