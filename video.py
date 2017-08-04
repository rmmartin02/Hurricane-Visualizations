import sys
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = 100000000000000000000
from Map import Map
from Cyclone import Hurricane, TrackPoint
from collections import OrderedDict
"""
#create ordered dict of times with list of points for each
times = ['18:00:00','12:00:00','00:00:00','06:00:00']
dates = OrderedDict()
hurricaneList = Hurricane.readData(sys.argv[1])

for hurr in hurricaneList:
	for p in hurr.trackPoints:
		if p.time[10:] in times:
			if p.time not in dates:
				dates[p.time] = [p]
			else:
				dates[p.time].append(p)
				
active = []
max = 0
while len(dates) != 0:
	map = Map("images\worldMap.jpg", 90.0, -180.0, -90.0, 180.0)
	#all
	map = map.getSubMap(81.0,-180.0,-68.5,180.0)
	values = dates.popitem(last=False)
	time = values[0]
	points = values[1]
	curr = []
	for p in points:
		curr.append(p.hurricane)
		map.drawSquare(p.getColor(),50,p.latitude,p.longitude)
		if p.hurricane not in active:
			active.append(p.hurricane)
		else:
			i = 0
			end = p.hurricane.trackPoints.index(p)
			oldPoint = p.hurricane.trackPoints[i]
			while i<end:
				newPoint = p.hurricane.trackPoints[i+1]
				if (newPoint.longitude>90 and oldPoint.longitude<-90) or (oldPoint.longitude>90 and newPoint.longitude<-90):
					print("over date line")
				else:
					if(oldPoint.getColor()==(0,0,0)):
						map.drawLine((28,84,255),10,oldPoint.latitude,oldPoint.longitude,newPoint.latitude,newPoint.longitude)
					else:
						map.drawLine(oldPoint.getColor(),10,oldPoint.latitude,oldPoint.longitude,newPoint.latitude,newPoint.longitude)
				i += 1
				oldPoint = p.hurricane.trackPoints[i]
	addedHeight = int(((9/16)*map.mapImage.size[0]) - map.mapImage.size[1])
	print(addedHeight)
	newImage = Image.new('RGBA', (map.mapImage.size[0],map.mapImage.size[1]+(addedHeight)),(255,255,255))
	newImage.paste(map.mapImage, box=(0,0,map.mapImage.size[0],map.mapImage.size[1]))
	newImage.resize((3840,2160))
	d = ImageDraw.Draw(newImage)
	basins = ['EP','SP','NA','SA','NI','SI','WP']
	#left,up,right,low
	for i in range(len(basins)):
		# font = ImageFont.truetype(<font-file>, <font-size>)
		font = ImageFont.truetype("arial.ttf", 300)
		# draw.text((x, y),"Sample Text",(r,g,b))
		cor = [newImage.size[0]*(i/len(basins)),newImage.size[1]-addedHeight,newImage.size[0]*((i+1)/len(basins)),newImage.size[1]]
		d.text((cor[0], cor[1]),basins[i],(0,0,0),font=font)
		width = 10
		for i in range(width):
			d.rectangle(cor,outline=(0,0,0))
			cor = [cor[0]+1,cor[1]-1,cor[2]-1,cor[3]-1]
	newImage.show()
	#save image
	active = curr
	if len(active) > max:
		max = len(active)
print(max)
"""
"""
for hurricane in hurricaneList:
	oldPoint = hurricane.trackPoints[0]
	for point in hurricane.trackPoints:
		newlat = point.latitude
		newlong = point.longitude
		if (newlong>90 and oldPoint.longitude<-90) or (oldPoint.longitude>90 and newlong<-90):
			print("over date line")
		else:
			if(oldPoint.getColor()==(0,0,0)):
				map.drawLine((28,84,255),1,oldPoint.latitude,oldPoint.longitude,newlat,newlong)
			else:
				map.drawLine(oldPoint.getColor(),1,oldPoint.latitude,oldPoint.longitude,newlat,newlong)
		oldPoint = point
"""
map = Map("images\worldMap.jpg", 90.0, -180.0, -90.0, 180.0)
	#all
map = map.getSubMap(81.0,-180.0,-68.5,180.0)
addedHeight = int(((9/16)*map.mapImage.size[0]) - map.mapImage.size[1])
print(addedHeight)
newImage = Image.new('RGBA', (map.mapImage.size[0],map.mapImage.size[1]+(addedHeight)),(255,255,255))
newImage.paste(map.mapImage, box=(0,0,map.mapImage.size[0],map.mapImage.size[1]))
newImage.resize((3840,2160))
d = ImageDraw.Draw(newImage)
basins = ['EP','SP','NA','SA','NI','SI','WP']
#left,up,right,low
for i in range(len(basins)):
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("arial.ttf", 300)
	# draw.text((x, y),"Sample Text",(r,g,b))
	cor = [newImage.size[0]*(i/len(basins)),newImage.size[1]-addedHeight,newImage.size[0]*((i+1)/len(basins)),newImage.size[1]]
	d.text((cor[0], cor[1]),basins[i],(0,0,0),font=font)
	width = 10
	for i in range(width):
		d.rectangle(cor,outline=(0,0,0))
		cor = [cor[0]+1,cor[1]-1,cor[2]-1,cor[3]-1]
for i in range(5):
	#working on lines
	d.line([(0,newImage.size[1]-addedHeight//(i+2)),(newImage.size[0],newImage.size[1]-addedHeight//(i+2))],width=10,fill=(0,0,0))
newImage.show()
newImage.save('images/vidEx.png')
