basinList = []

with open('data/unedited.csv','r') as f:
	for text in f:
		text = text.replace(" ","").split(",")
		if(text[3] not in basinList):
			basinList.append(text[3])

fullText = []
with open('data/unedited.csv','r') as file:
	for text in file:
		text = text.split(',')
		#YYYY-MM-DD HH:MM:SS
		#D/M/YYYY H:MM or D/M/YYYY H:MM
		if '/' in text[6]:
			s = text[6].split(' ')
			date = s[0].split('/')
			if len(date[0])==1:
				date[0] = '0' + date[0]
			if len(date[1])==1:
				date[1] = '0' + date[1]
			temp = date[0]
			date[0] = date[2]
			date[2] = temp
				
			time = s[1].split(':')
			if len(time[0]) == 1:
				time[0] = '0' + time[0]
			if len(time) == 2:
				time.append('00')
				
			text[6] = '-'.join(date) + ' ' + ':'.join(time)
		fullText.append(','.join(text))
			
with open('data/all.csv','w') as file:
	file.writelines(fullText)
	
print(basinList);
			
for basin in basinList:
	with open('data/' + basin.lower() + '.csv','w') as file:
		with open('data/all.csv','r') as f:
			for text in f:
				row = text.replace(" ","").split(",")
				if(row[3] in basin):
					file.write(text)
		