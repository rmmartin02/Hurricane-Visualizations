fullText = []
with open('hurdat.csv','r') as file:
	for text in file:
		text = text.split(',')
		if len(text)>6:
			text[4] = text[4][:-1]
			if text[5][-1] == 'W':
				text[5] = '-' + text[5][:-1]
			else:
				text[5] = text[5][:-1]
		fullText.append(','.join(text))
	
with open('hurdatFixed.csv','w') as file:
	for line in fullText:
		file.write(line.replace(' ','').replace('\t',''))