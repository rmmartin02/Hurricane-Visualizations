import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import matplotlib
import sys
from Map import Map
from Cyclone import Hurricane, TrackPoint
from PIL import Image
	

hurricaneList = []

print("Reading data")
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

#NEED TO FIX DATA (COASTLINE BIAS, TIME DIFFERENCES)
print("Cleaning data")
times = ['18:00:00','12:00:00','00:00:00','06:00:00']
removed = 0
h = 0
print(len(hurricaneList))
while h < len(hurricaneList):
	t = 0
	while t < len(hurricaneList[h].trackPoints):
		if hurricaneList[h].trackPoints[t].time[10:] in times or hurricaneList[h].trackPoints[t].wind<0.0:
			removed += 1
			del hurricaneList[h].trackPoints[t]
		else:
			t = t+1
	if len(hurricaneList[h].trackPoints) == 0:
		del hurricaneList[h]
	else:
		h = h + 1
print("Removed " + str(removed) + " points from data")
print(len(hurricaneList))
		
map = Map("images/worldMap.jpg", 90.0, -180.0, -90.0, 180.0)
maxlat = -180
maxlong = -90
minlat = 180
minlong = 90
latlongDict = {}
print("Constructing Map")
for hurricane in hurricaneList:
	for point in hurricane.trackPoints:
		lat = point.latitude
		lon = point.longitude
		if(lat>maxlat):
			maxlat = lat
		elif(lat<minlat):
			minlat = lat
		if(lon>maxlong):
			maxlong = lon
		elif(lon<minlong):
			minlong = lon
		map.drawPoint((255,0,0),lat,lon)
		
		key = str(lat) + ' ' + str(lon)
		if(key in latlongDict):
			latlongDict[key] = latlongDict[key] + 1
		else:
			latlongDict[key] = 1
print(len(latlongDict))
map = map.getSubMap(maxlat, minlong, minlat, maxlong)
#map.view()

#construct 2d array of all possible lat,long positions
#then go through points and count how many are at each position
longlat = [[0]*(int((maxlat-minlat) * 10)+1) for _ in range(int((maxlong-minlong)*10)+1)]
print("Calculating data points")
for key in latlongDict:
	c = key.split(' ')
	longlat[int((float(c[1])-minlong)*10)][int((float(c[0])-minlat)*10)] = latlongDict[key]
	
cfactor = int(sys.argv[2])
compressed = [[0]*(int(len(longlat)/cfactor)+1) for _ in range(int(len(longlat[0])/cfactor)+1)]
max = 0
print("Compressing data by " + str(cfactor) + "x")
for i in range(0,len(longlat[0]),cfactor):
	for j in range(0,len(longlat),cfactor):
		sum = 0
		for l in range(i,i+cfactor):
			if(l==len(longlat[0])):
				break
			for k in range(j,j+cfactor):
				if(k == len(longlat)):
					break
				sum += longlat[k][l]
		if(sum>max):
			max = sum
		compressed[int(i/cfactor)][int(j/cfactor)] = sum

for i in compressed:
	for j in i:
		j = float(j)/float(max)


#https://pythonspot.com/en/generate-heatmap-in-matplotlib/
#https://stackoverflow.com/questions/9295026/matplotlib-plots-removing-axis-legends-and-white-spaces
print("Plotting")

colormap = 'YlOrRd'

data = np.array(compressed)
plt.imsave("images/heatmap.png",data,format = "png", origin = 'lower',cmap = colormap)

print("Imposing heatmap over map")
#impose heatmap over map image
top = Image.open('images/heatmap.png')
bottom = map.mapImage
top = top.convert("RGBA")
top.putalpha(128)
datas = top.getdata()

newData = []
colormap = matplotlib.cm.get_cmap(colormap)
rgba = colormap(0.0)
rgba = (int(rgba[0]*255),int(rgba[1]*255),int(rgba[2]*255),int(rgba[3]*255))
for item in datas:
	if item[0] == rgba[0] and item[1] == rgba[1] and item[2] == rgba[2]:
		newData.append((255, 255, 255, 0))
	else:
		newData.append(item)

top.putdata(newData)
bottom = bottom.convert("RGBA")
bottom.putalpha(255)
top = top.resize(bottom.size)
final = Image.alpha_composite(bottom, top)
final.show()
 
