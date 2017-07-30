import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import matplotlib
import sys
from Map import Map
from Cyclone import Hurricane, TrackPoint
from PIL import Image
	

hurricaneList = []
cfactor = int(sys.argv[2])

print("Reading data")
hurricaneList = Hurricane.readData(sys.argv[1])

print("Cleaning data")
#remove landfall bias and adjust data
times = ['18:00:00','12:00:00','00:00:00','06:00:00']
removed = 0
h = 0
print(len(hurricaneList))
while h < len(hurricaneList):
	t = 0
	#delHur = hurricaneList[h].season<1966
	delHur = False
	while t < len(hurricaneList[h].trackPoints):
	#t!=0
		if hurricaneList[h].trackPoints[t].time[10:] not in times:
			removed += 1
			del hurricaneList[h].trackPoints[t]
		else:
			t = t+1
	#or hurricaneList[h].trackPoints[0].time[5:7]!='07'
	if len(hurricaneList[h].trackPoints) == 0 or delHur:
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
countsDict = {}
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
		if(key in countsDict):
			countsDict[key] = countsDict[key] + 1
		else:
			countsDict[key] = 1
print(len(countsDict))

#trying to fix slight mismatch between heatmap and map by making sure map coords divisible by cfactor
maxlat += .1
maxlong += .1
print(maxlat, minlat, maxlong, minlong)
print(((maxlat-minlat)*10)%cfactor, ((maxlong-minlong)*10)%cfactor)
if not ((maxlat-minlat)*10)%cfactor == 0:
	if (maxlat + (cfactor - (((maxlat-minlat)*10)%cfactor))*.1)!=90.0:
		print('increase max lat')
		maxlat = maxlat + (cfactor - (((maxlat-minlat)*10)%cfactor))*.1
	elif (minlat - (((maxlat-minlat)*10)%cfactor)*.1)!=-90.0:
		print('decrease min lat')
		minlat = minlat - (((maxlat-minlat)*10)%cfactor)*.1
	else:
		print('decrease max lat')
		maxlat = maxlat - (((maxlat-minlat)*10)%cfactor)*.1
if not ((maxlong-minlong)*10)%cfactor == 0:
	if (maxlong + (cfactor - (((maxlong-minlong)*10)%cfactor))*.1)!=90.0:
		print('increase max long')
		maxlong = maxlong + (cfactor - (((maxlong-minlong)*10)%cfactor))*.1
	elif (minlong - (((maxlong-minlong)*10)%cfactor)*.1)!=-90.0:
		print("decrease min long")
		minlong = minlong - (((maxlong-minlong)*10)%cfactor)*.1
	else:
		print("decrease max long")
		maxlong = maxlong - (((maxlong-minlong)*10)%cfactor)*.1
map = map.getSubMap(maxlat, minlong, minlat, maxlong)	
print(((maxlat-minlat)*10)%cfactor, ((maxlong-minlong)*10)%cfactor)
print(maxlat,minlat,maxlong,minlong)

#construct 2d array of all possible lat,long positions
#then go through points and count how many are at each position
print(int(round((maxlong-minlong)*10)),int(round((maxlat-minlat)*10)))
counts = [[0]*(int(round((maxlong-minlong)*10))) for _ in range(int(round((maxlat-minlat)*10)))]
print("Calculating data points")
for key in countsDict:
	c = key.split(' ')
	lat = float(c[0])
	long = float(c[1])
	if (lat<=maxlat and lat>=minlat) and (long<=maxlong and long>=minlong):
		counts[int((lat-minlat)*10)][int((long-minlong)*10)] = countsDict[key]
	
#compress data so that it looks better on heatmap
compressed = [[0]*(int(len(counts[0])/cfactor)) for _ in range(int(len(counts)/cfactor))]
print(len(counts),len(counts[0]))
print(len(compressed),len(compressed[0]))
max = 0
print("Compressing data by " + str(cfactor) + "x")
for i in range(0,len(counts),cfactor):
	for j in range(0,len(counts[0]),cfactor):
		sum = 0
		for l in range(i,i+cfactor):
			for k in range(j,j+cfactor):
				sum += counts[l][k]
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
if len(sys.argv)>3:
	final.save("visuals/"+sys.argv[3])
else:
	final.show()
 
