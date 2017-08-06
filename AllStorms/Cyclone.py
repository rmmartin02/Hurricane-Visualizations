class TrackPoint:

		Colors = {'ET' : (170,170,170),'TD' : (28,84,255),'TS' : (109,195,67),'C1' : (255,195,9),'C2' : (255,115,9),'C3' : (232,59,12),'C4' : (232,12,174),'C5' : (189,0,255)}
		
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
		
		def getColor(self):
			if (self.nature == "ET"):
				return TrackPoint.Colors['ET'];
			
			if(self.nature == "DS") :
				return TrackPoint.Colors['TD'];
			
			if (self.wind >= 137.0):
				return TrackPoint.Colors['C5'];
			
			if (self.wind >= 113.0):
				return TrackPoint.Colors['C4'];
			
			if (self.wind >= 96.0):
				return TrackPoint.Colors['C3'];
			
			if (self.wind >= 83.0):
				return TrackPoint.Colors['C2'];
			
			if (self.wind >= 64.0):
				return TrackPoint.Colors['C1'];
			
			if (self.wind >= 34.0):
				return TrackPoint.Colors['TS'];
			
			return TrackPoint.Colors['TD'];
    

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
	
	def getMinPressure(self):
		min = 2000
		for point in self.trackPoints:
			if(point.pressure<min and point.pressure > 800):
				min = point.pressure
		return min
		
	def getACE(self):
		times = ['18:00:00','12:00:00','00:00:00','06:00:00']
		ace = 0.0
		for p in self.trackPoints:
			if p.time[10:] in times and p.nature == 'TS' and p.wind>= 35.0:
				ace += (p.wind * p.wind)/10000
		return ace
		
	def getBasinCoords(basin):
		if basin == 'all':
			return (81.0,-180.0,-68.5,180.0)
		if basin == 'na':
			return (80.3,-109.5,7.2,28.0)
		if basin == 'wp':
			return (69.0,-179.97,0.1,179.99)
		if basin == 'si':
			return (-0.4,17.77,-48.7,135.22)
		if basin == 'sp':
			return (-3.2,-180.0,-68.5,180.0)
		if basin == 'ni':
			return (81.0,32.0,0.7,99.94)
		if basin == 'ep':
			return (61.8,-179.99,1.9,180.0)
		if basin == 'sa':
			return (-19.0,-50.1,-38.0,-30.5)
	
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
				latitude = float(text[8])
				longitude = float(text[9])
				wind = float(text[10])
				pressure = float(text[11])
				center =  text[12]
				trackType = text[13]
				currentBasin = text[14]
				hurricaneList[hurrNum].addTrackPoint(hurricaneList[hurrNum], time, nature, latitude, longitude, wind, pressure, center, trackType, currentBasin)
		return hurricaneList