class TrackPoint:

		Colors = {'ET' : (170,170,170),'TD' : (28,84,255),'TS' : (109,195,67),'C1' : (255,195,9),'C2' : (255,115,9),'C3' : (232,59,12),'C4' : (232,12,174),'C5' : (189,0,255)}
		
		def __init__(self, hurricane, date, time, nature, latitude, longitude, wind, pressure, center=None, trackType=None, currentBasin=None, ne34=None, se34=None, sw34=None, nw34=None, ne50=None, se50=None, sw50=None, nw50=None, ne64=None, se64=None, sw64=None, nw64=None):
			self.hurricane = hurricane
			self.date = date
			self.time = time
			self.nature = nature
			self.latitude = latitude
			self.longitude = longitude
			self.wind = wind
			self.pressure = pressure
			self.center = center
			self.trackType = trackType
			self.currentBasin = currentBasin
			self.ne34 = ne34
			self.se34 = se34
			self.sw34 = sw34
			self.nw34 = nw34
			self.ne50 = ne50
			self.se50 = se50
			self.sw50 = sw50
			self.nw50 = nw50
			self.ne64 = ne64
			self.se64 = se64
			self.sw64 = sw64
			self.nw64 = nw64
		
		def getColor(self):
			if (self.nature == "ET" or self.nature == "EX"):
				return TrackPoint.Colors['ET'];
			
			if(self.nature == "DS" or self.nature == "TD") :
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

	def __init__(self, serialNumber = None, season = None, num = None, basin = None, subBasin = None, name= None, numPoints = None):
		self.serialNumber = serialNumber
		self.season = season
		self.num = num
		self.basin = basin
		self.subBasin = subBasin
		self.name = name
		self.numPoints = numPoints
		self.trackPoints = []
	""""
	def __init__(self, basin, num, season, name, numPoints):
		self.basin = basin
		self.num = num
		self.season = season
		self.name = name
		self.numPoints = numPoints
		self.trackPoints = []
	"""
	def addTrackPoint(self, hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType, currentBasin):
		self.trackPoints.append(TrackPoint(hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType, currentBasin))
		
	def addHurdatTrackPoint(self, date, time, recordID, nature, latitude, longitude, wind, pressure, ne34, se34, sw34, nw34,ne50, se50, sw50, nw50, ne64, se64, sw64, nw64):
		self.trackPoints.append(TrackPoint(self, date, time, recordID, nature, latitude, longitude, wind, pressure, ne34, se34, sw34, nw34,ne50, se50, sw50, nw50, ne64, se64, sw64, nw64))
	
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
		times = ['18:00:00','12:00:00','00:00:00','06:00:00','0000','0600','1200','1800']
		ace = 0.0
		for p in self.trackPoints:
			if (p.time[10:] in times or p.time in times) and (p.nature == 'TS' or p.nature=='HU') and p.wind>= 35.0:
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
		return (81.0,-180.0,-68.5,180.0)

	@staticmethod
	def readData(data):
		hurricaneList = []
		with open('data/' + data,'r') as f:
			tempSerNum = ""
			hurrNum = -1
			for text in f:
				text = text.replace(" ","").split(",")
				if(text[0] != tempSerNum):
					hurrNum += 1
					#serialNumber, season, num, basin, subBasin, name
					hurricaneList.append(Hurricane(serialNumber = text[0], season = int(text[1]), num = int(text[2]), basin = text[3], subBasin = text[4], name = text[5]))
					tempSerNum = text[0]
				#hurricane, time, nature, latitude, longitude, wind, pressure, center, trackType
				date = text[6][:10]
				time = text[6][10:]
				nature = text[7]
				latitude = float(text[8])
				longitude = float(text[9])
				wind = float(text[10])
				pressure = float(text[11])
				center =  text[12]
				trackType = text[13]
				currentBasin = text[14]
				hurricaneList[hurrNum].trackPoints.append(TrackPoint(hurricaneList[hurrNum], date, time, nature, latitude, longitude, wind, pressure,  center=center, trackType=trackType, currentBasin=currentBasin))
		return hurricaneList

	def didLandfall(self):
		for p in self.trackPoints:
			if p.recordID == 'L':
				return True
		return False

	def getLandfalls(self):
		land = []
		for p in self.trackPoints:
			if p.recordID == 'L':
				land.append(p)
		return land

	def getStrongestLandfall(self):
		max = 0
		maxP = None
		for p in self.getLandfalls():
			if p.wind > max:
				max = p.wind
				maxP = p
		return maxP

	@staticmethod
	def readHurdat():
		hurricaneList = []
		f = open('data/hurdat.csv', 'r')
		line = f.readline()
		hurrNum = -1
		while line:
			text = line.split(',')
			if len(text) < 10:
				hurrNum += 1
				#basin, num, season, name, numPoints
				hurricaneList.append(Hurricane(basin=text[0][:2], num=int(text[0][2:4]), season=int(text[0][4:]), name=text[1], numPoints=int(text[2])))
			else:
				date = text[0]
				time = text[1]
				recordID = text[2]
				nature = text[3]
				latitude = float(text[4])
				longitude = float(text[5])
				wind = int(text[6])
				pressure = int(text[7])
				ne34 = int(text[8])
				se34 = int(text[9])
				sw34 = int(text[10])
				nw34 = int(text[11])
				ne50 = int(text[12])
				se50 = int(text[13])
				sw50 = int(text[14])
				nw50 = int(text[15])
				ne64 = int(text[16])
				se64 = int(text[17])
				sw64 = int(text[18])
				nw64 = int(text[19])
				hurricaneList[hurrNum].trackPoints.append(TrackPoint(date, time, recordID, nature, latitude, longitude, wind, pressure, ne34=ne34, se34=se34, sw34=sw34, nw34=nw34, ne50=ne50, se50=se50, sw50=sw50, nw50=nw50, ne64=ne64, se64=se64, sw64=sw64, nw64=nw64))
			line = f.readline()
		f.close()
		return hurricaneList