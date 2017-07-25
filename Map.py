import sys
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = 100000000000000000000

class Map:

	def __init__(self, mapImage, latUp, longLeft, latBot, longRight):
		if(isinstance(mapImage, str)):
			self.mapImage = Image.open(mapImage)
		else:
			self.mapImage = mapImage
		self.latUp = latUp
		self.longLeft = longLeft
		self.latBot = latBot
		self.longRight = longRight
		
	def getSubMap(self, latUp, longLeft, latBot, longRight):
		coordinates = ((longLeft+180)/360, 1-((latUp+90)/180), (longRight+180)/360, 1-((latBot+90)/180))
		box = (int(coordinates[0]*self.mapImage.size[0]),int(coordinates[1]*self.mapImage.size[1]),int(coordinates[2]*self.mapImage.size[0]),int(coordinates[3]*self.mapImage.size[1]))
		return Map(self.mapImage.crop(box), latUp, longLeft, latBot, longRight)
		
	def view(self):
		self.mapImage.show()
		
	def save(self, name):
		self.mapImage.save(name)
		
	def latLongToPixelCoord(self, lat, long):
		x = ((long-self.longLeft) / (self.longRight-self.longLeft)) * self.mapImage.size[0]
		y = ((lat-self.latUp)/(self.latBot-self.latUp)) *self.mapImage.size[1]
		return (x,y)
		
	def drawPoint(self, color, lat, long):
		coords = self.latLongToPixelCoord(lat, long)
		d = ImageDraw.Draw(self.mapImage)
		d.point(coords,fill=color)
		
	def drawLine(self, color, wid, lat1, long1, lat2, long2):
		coords = self.latLongToPixelCoord(lat1, long1)
		coords2 = self.latLongToPixelCoord(lat2, long2)
		line = []
		line.append(coords)
		line.append(coords2)
		d = ImageDraw.Draw(self.mapImage)
		d.line(line,fill=color, width=wid)