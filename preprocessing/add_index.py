a = open('temp', 'r')
b = open('temp2', 'w')

line = ''
i = 0
while(True):
	line = a.readline()
	if not line:
		break

	mod_line = line[:-1] + ' : ' + str(i) + '\n'
	i+=1
	b.write(mod_line)