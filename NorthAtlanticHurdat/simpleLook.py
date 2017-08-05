import sys
from Cyclone import Hurricane, TrackPoint
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
hurricaneList = Hurricane.readData('hurdatFixed.csv')
times = {}
for h in hurricaneList:
	for p in h.trackPoints:
		if p.time not in times:
			times[p.time] = 1
		else:
			times[p.time] = times[p.time] + 1
print(sorted(times.items(), key=lambda x:x[1]))