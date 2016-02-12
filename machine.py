import sys

def machine(filename):
	code=[]
	f=open(filename,'r')
	data=f.read()
	f.close()

	lines=data.splitlines()
	reg={}
	mem=[0]*1024


	for line in lines:
		line_split = line.split(' ')

		if line.startswith('ADI'):
			code.append('11000110\n')	
			val=int(line.split(' ')[1])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('ANI'):
			code.append('11100110\n')	
			val=int(line.split(' ')[1])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('JMP'):
			code.append('11000011\n')
			val=int(line.split(' ')[1])
			val1=str('{0:016b}'.format(val))
			code.append(val1[0:8] + '\n')
			code.append(val1[8:16] + '\n')


		if line.startswith('JNZ'):
			code.append('11000010\n')
			val=int(line.split(' ')[1])
			val1=str('{0:016b}'.format(val))
			code.append(val1[0:8] + '\n')
			code.append(val1[8:16] + '\n')

		if line.startswith('JZ'):
			code.append('11001010\n')
			val=int(line.split(' ')[1])
			val1=str('{0:016b}'.format(val))
			code.append(val1[0:8] + '\n')
			code.append(val1[8:16] + '\n')

		if line.startswith('JP'):
			code.append('11111010\n')
			val=int(line.split(' ')[1])
			val1=str('{0:016b}'.format(val))
			code.append(val1[0:8] + '\n')
			code.append(val1[8:16] + '\n')

		if line.startswith('HLT'):
			code.append('01110110\n')		

		if line.startswith('ORI'):
			code.append('11110110\n')
			val=int(line.split(' ')[1])
			code.append(str('{0:08b}'.format(val))+'\n')


		if line.startswith('SUI'):
			code.append('11010110\n')
			val=int(line.split(' ')[1])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('ADD A'):
			code.append('11010110\n')

		if line.startswith('ADD B'):
			code.append('11010110\n')

		if line.startswith('ADD C'):
			code.append('11010110\n')

		if line.startswith('ADD D'):
			code.append('11010110\n')

		if line.startswith('ADD E'):
			code.append('11010110\n')

		if line.startswith('ADD H'):
			code.append('11010110\n')

		if line.startswith('ADD L'):
			code.append('11010110\n')

		if line.startswith('ANA A'):
			code.append('10100111\n')

		if line.startswith('ANA B'):
			code.append('10100000\n')

		if line.startswith('ANA C'):
			code.append('10100001\n')

		if line.startswith('ANA D'):
			code.append('10100010\n')

		if line.startswith('ANA E'):
			code.append('10100011\n')

		if line.startswith('ANA H'):
			code.append('10100100\n')

		if line.startswith('ANA L'):
			code.append('10100101\n')


		if line.startswith('SUB A'):
			code.append('10010111\n')

		if line.startswith('SUB B'):
			code.append('10010000\n')

		if line.startswith('SUB C'):
			code.append('10010001\n')

		if line.startswith('SUB D'):
			code.append('10010010\n')

		if line.startswith('SUB E'):
			code.append('10010011\n')

		if line.startswith('SUB H'):
			code.append('10010100\n')

		if line.startswith('SUB L'):
			code.append('10010101\n')

		if line.startswith('DB'):
			val=int(line.split(' ')[1])
			code.append(str('{0:08b}'.format(val))+'\n')	

		if line.startswith('POP B'):
			code.append('11000001\n')

		if line.startswith('POP D'):
			code.append('11010001\n')
		
		if line.startswith('POP H'):
			code.append('11100001\n')

		if line.startswith('PUSH B'):
			code.append('11000101\n')

		if line.startswith('PUSH D'):
			code.append('11010101\n')
		
		if line.startswith('PUSH H'):
			code.append('11100101\n')

		if line.startswith('MVI A'):
			code.append('00111110\n')
			val=int(line.split(' ')[2])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('MVI B'):
			code.append('00000110\n')
			val=int(line.split(' ')[2])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('MVI C'):
			code.append('00001110\n')
			val=int(line.split(' ')[2])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('MVI D'):
			code.append('00010110\n')
			val=int(line.split(' ')[2])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('MVI E'):
			code.append('00011110\n')
			val=int(line.split(' ')[2])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('MVI H'):
			code.append('00100110\n')
			val=int(line.split(' ')[2])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('MVI L'):
			code.append('00101110\n')
			val=int(line.split(' ')[2])
			code.append(str('{0:08b}'.format(val))+'\n')

		if line.startswith('MOV A, A'):
			code.append('01111111\n')

		if line.startswith('MOV A, B'):
			code.append('01111000\n')

		if line.startswith('MOV B, A'):
			code.append('01000111\n')

		if line.startswith('ORA A'):
			code.append('10110111\n')

		if line.startswith('ORA B'):
			code.append('10110000\n')

		if line.startswith('ORA C'):
			code.append('10110001\n')

		if line.startswith('ORA D'):
			code.append('10110010\n')

		if line.startswith('ORA E'):
			code.append('10110011\n')

		if line.startswith('ORA H'):
			code.append('10110100\n')

		if line.startswith('ORA L'):
			code.append('10110101\n')

		if line.startswith('LDA'):
			code.append('00111010\n')
			val=int(line.split(' ')[1])
			val1=str('{0:016b}'.format(val))
			code.append(val1[0:8] + '\n')
			code.append(val1[8:16] + '\n')

		if line.startswith('STA'):
			code.append('00110010\n')
			val=int(line.split(' ')[1])
			val1=str('{0:016b}'.format(val))
			code.append(val1[0:8] + '\n')
			code.append(val1[8:16] + '\n')
	
	code=''.join(code)
	filename=filename.split('.')[0]+'.machine'
	f=open(filename,'w')
	f.write(code)
	f.close()
