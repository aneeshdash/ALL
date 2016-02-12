import sys

byte=0
filename = sys.argv[1]
offset = int(sys.argv[2])
f=open(filename,'r')
data=f.read()
f.close()

opcodes = {}
code=data.splitlines()
lines = {}
reg={'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'H':0, 'L':0}
mem=[0]*1024
sp=1023
flag=[0]*5
dispflag=0

f=open('oplength.txt','r')
data=f.read()
f.close()
lin=data.splitlines()
for line in lin:
	line=line.split(' ')
	opcodes[line[0]]=int(line[1])

j=offset
for line in code:
	lines[str(j)]=line
	if line.startswith('DB'):
		mem[j]=int(line.split(' ')[1])
	j += opcodes[line.split(' ')[0]]

i=j
byte=offset

def set_flag(acc):
	if acc == 0:
		flag[0]=1
		flag[1]=0
		flag[2]=0

	elif acc > 0:
		flag[1]=1
		flag[0]=0
		flag[2]=0

	else:
		flag[2]=1
		flag[1]=0
		flag[0]=0

dispflag=0
def display(prevs, nexts):
	global dispflag
	if dispflag is 0:
		for key in reg:
			print key+' : '+str(reg[key])
		print flag
		print 'Prev Statement:'+lines[str(prevs)]
		print 'Next Statement:'+lines[str(nexts)]
		print 'Contiue(c) or Next(n) :',
		res=raw_input()
		if res is 'c':
			dispflag=1
		
while byte < i:
	line=lines[str(byte)]
	line_split = line.split(' ')
	if len(line_split) > 1:
		line_split[1] = line_split[1].strip(',')
	if line.startswith('MOV'):
		reg[line_split[1]]=reg[line_split[2]]
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('MVI'):
		reg[line_split[1]]=int(line_split[2])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('LDA'):
		reg['A']=mem[int(line_split[1])]
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('ADI'):
		reg['A']=reg['A'] + int(line_split[1])
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('SUI'):
		reg['A']=reg['A'] - int(line_split[1])
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('SUB'):
		reg['A']=reg['A'] - reg[line_split[1]]
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('ADD'):
		reg['A']=reg['A'] + reg[line_split[1]]
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('STA'):
		mem[int(line_split[1])]=reg['A']
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('PUSH'):
		if line_split[1] is 'D':
			mem[sp]=reg['D']
			mem[sp-1]=reg['E']
		elif line_split[1] is 'B':
			mem[sp]=reg['B']
			mem[sp-1]=reg['C']
		else:
			mem[sp]=reg['H']
			mem[sp-1]=reg['L']
		sp=sp-2
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('POP'):
		if line_split[1] is 'D':
			reg['D']=mem[sp+1]
			reg['E']=mem[sp]
		elif line_split[1] is 'B':
			reg['B']=mem[sp+1]
			reg['C']=mem[sp]
		else:
			reg['H']=mem[sp+1]
			reg['L']=mem[sp]
		sp=sp+2
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('ORI'):
		reg['A']=reg['A'] | int(line_split[1])
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('ORA'):
		reg['A']=reg['A'] | reg[line_split[1]]
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)
	
	
	elif line.startswith('JNZ'):
		byte_old=byte
		if flag[0] == 0:
			byte=int(line_split[1])
		else:
			byte += opcodes[line_split[0]]
		display(byte_old, byte)

	elif line.startswith('JZ'):
		byte_old=byte
		if flag[0] == 1:
			byte=int(line_split[1])
		else:
			byte += opcodes[line_split[0]]
		display(byte_old, byte)			

	elif line.startswith('JP'):
		byte_old=byte
		if flag[1] == 1:
			byte=int(line_split[1])
		else:
			byte += opcodes[line_split[0]]
		display(byte_old, byte)	

	elif line.startswith('JMP'):
		byte_old=byte
		byte=int(line_split[1])
		display(byte_old, byte)

	# elif line.startswith('DB'):
	# 	mem[byte]=int(line_split[1])
	# 	byte += opcodes[line_split[0]]
	# 	display(byte-opcodes[line_split[0]], byte)
	
	elif line.startswith('JM'):
		byte_old=byte
		byte=int(line_split[1]) -1
		byte += opcodes[line_split[0]]
		display(byte_old, byte)
	
	elif line.startswith('ANI'):
		reg['A']=reg['A'] & int(line_split[1])
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)
	
	elif line.startswith('ANA'):
		reg['A']=reg['A'] & reg[line_split[1]]
		set_flag(reg['A'])
		byte += opcodes[line_split[0]]
		display(byte-opcodes[line_split[0]], byte)

	elif line.startswith('HLT'):
		byte += opcodes[line_split[0]]
		for key in reg:
			print key+' : '+str(reg[key])




