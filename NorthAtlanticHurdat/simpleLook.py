import sys
from Tools.Cyclone import Hurricane, TrackPoint
hurricaneList = Hurricane.readHurdat()
"""	
hurricaneList = []
list = []
f = open('hurdat.csv', 'r' )
line = f.readline()
hurrNum = -1
while line :
	line = line.replace(' ','').replace('\t','').replace('\n','')
	text = line.split(',')
	if len(text) == 4:
		hurrNum += 1
		hurricaneList.append(Hurricane(text[0][:2],int(text[0][2:4]),int(text[0][4:]),text[1],int(text[2])))
	else:
		if text[4][-1] not in list:
			list.append(text[4][-1])
		if text[5][-1] not in list:
			list.append(text[5][-1])
		#hurricaneList[hurrNum].addTrackPoint(int(text[0][:4]),int(text[0][4:6]),int(text[0][6:8]),int(text[1][:2]),int(text[1][2:]),text[2],text[3],)
	line = f.readline()
f.close()
print(list)
"""
"""
hurricaneList = Hurricane.readData('hurdat.csv')
times = {}
for h in hurricaneList:
	for p in h.trackPoints:
		if p.time not in times:
			times[p.time] = 1
		else:
			times[p.time] = times[p.time] + 1
print(sorted(times.items(), key=lambda x:x[1]))
"""
"""
hurricaneList = Hurricane.readHurdat()
land = {}
for h in hurricaneList:
	for p in h.trackPoints:
		if p.recordID == 'L':
			ser = str(h.basin) + str(h.num) + str(h.season)
			if ser in land:
				land[ser] = land[ser]+1
			else:
				land[ser] = 1
print(sorted(land.items(), key=lambda x:x[1]))
"""
"""
year = {}
for h in hurricaneList:
	if h.season not in year:
		year[h.season] = 0
	year[h.season] = year[h.season] + h.getACE()
	year[h.season] = round(year[h.season],3)
print(sorted(year.items(), key=lambda x:x[1]))
"""
tropCount = {}
hurCount = {}
majCount = {}
for h in hurricaneList:
	if h.season not in tropCount:
		tropCount[h.season] = 0
	if h.season not in hurCount:
		hurCount[h.season] = 0
	if h.season not in majCount:
		majCount[h.season] = 0
	ts = False
	hur = False
	maj = False
	for p in h.trackPoints:
		if p.nature=='TS':
			ts = True
		if p.nature=='HU':
			hur = True
		if p.wind>=96.0:
			maj = True
	if ts:
		tropCount[h.season] = tropCount[h.season] + 1
	if hur:
		hurCount[h.season] = hurCount[h.season] + 1
	if maj:
		majCount[h.season] = majCount[h.season] + 1
print(sorted(tropCount.items(), key=lambda x:x[1]))
print(sorted(hurCount.items(), key=lambda x:x[1]))
print(sorted(majCount.items(), key=lambda x:x[1]))
tropArr = []
hurArr = []
majArr = []
for key in tropCount:
	tropArr.append(tropCount[key])
for key in hurCount:
	hurArr.append(hurCount[key])
for key in majCount:
	majArr.append(majCount[key])
print(sum(tropArr)//len(tropArr),tropArr[len(tropArr)//2])
print(sum(hurArr)//len(hurArr),hurArr[len(hurArr)//2])
print(sum(majArr)//len(majArr),majArr[len(majArr)//2])