basinList = []

with open('data/unedited.csv','r') as f:
	f.readline()
	for text in f:
		text = text.replace(" ","").split(",")
		if(text[3] not in basinList):
			basinList.append(text[3])
print(basinList);

fullText = []
windChange = 0
pressChange = 0
typeChange = 0
dropped = 0
with open('data/unedited.csv','r') as file:
	headings = file.readline().split(',')
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
		text = ','.join(text)
		text = text.replace(' ','').split(',')
		#wind
		if float(text[10])<=0:
			if text[12] != 'N/A':
				for i in range(18,143,5):
					if text[12] in headings[i] and float(text[i])>0:
						text[10] = text[i]
						windChange += 1
			if float(text[10])<=0:
				for i in range(18,143,5):
					if float(text[i])>0:
						text[10] = text[i]
						windChange += 1
		#pressure
		if float(text[11])<=0:
			if text[12] != 'N/A':
				for i in range(19,144,5):
					if text[12] in headings[i] and float(text[i])>0:
						text[11] = text[i]
						pressChange += 1
			if float(text[11])<=0:
				for i in range(19,144,5):
					if float(text[i])>0:
						text[11] = text[i]
						pressChange += 1
		#type/grade
		if text[7] == 'NR':
			natures = ['TS', 'ET', 'SS', 'DS', 'MX']
			if text[12] != 'N/A':
				for i in range(17,142,5):
					if text[12] in headings[i] and text[i] in natures:
						text[7] = text[i]
						typeChange += 1
			if text[7] == 'NR':
				for i in range(17,142, 5):
					if text[i] in natures:
						text[7] = text[i]
						typeChange += 1
					elif float(text[10])>=34.0:
						text[7] = 'TS'
						typeChange += 1
		if len(text)>14 and text[13] != 'split':
			fullText.append(','.join(text[:15]))
		else:
			dropped += 1

print(len(fullText), windChange, pressChange, typeChange, dropped)		
with open('data/all.csv','w') as file:
	for line in fullText:
		file.write(line + '\n')
	
for basin in basinList:
	with open('data/' + basin.lower() + '.csv','w') as file:
		with open('data/all.csv','r') as f:
			for text in f:
				row = text.replace(" ","").split(",")
				if(row[3] in basin):
					file.write(text)
		