import re

pp=0
code = []
symbols = {}
loopend = []
startif = []
opcodes = {}

def assemble(files):
	pp=0
	f=open('oplength.txt','r')
	data=f.read()
	f.close()
	lines=data.splitlines()
	for line in lines:
		line=line.split(' ')
		opcodes[line[0]]=int(line[1])
	assign=re.compile('var(.*?)=(.*)')
	ext=re.compile('extern (.*)')
	arith=re.compile('(.*?)=(.*?)[\+\-\&\|](.*?)')
	arith_add=re.compile('(.*?)=(.*?)\+(.*)')
	arith_sub=re.compile('(.*?)=(.*?)\-(.*)')
	arith_or=re.compile('(.*?)=(.*?)\|(.*)')
	arith_and=re.compile('(.*?)=(.*?)\&(.*)')

	for filen in files:
		filename=filen.split('.')[0]
		symbols[filename]= {}
		f=open(filen,'r')
		data=f.read()
		f.close()
		lines=data.splitlines()
		for line in lines:
			line=line.strip()
			if assign.match(line):
				asign=line[3:]
				a=re.search(r'(.*?)=(.*)',asign)
				vari = a.group(1).strip()
				val = a.group(2).strip()
				code.append('JMP '+str(pp+opcodes['JMP']+opcodes['DB'])+'\n')
				code.append('DB '+val+'\n')
				symbols[filename][vari] = str(pp+opcodes['JMP'])
				pp += opcodes['DB']+opcodes['JMP']

			elif ext.match(line):
				var=line[6:].strip()
				symbols[filename][var]='extern'+var

			elif arith.match(line):
				a=re.search(r'(.*?)=(.*?)[\+\-\&\|](.*)',line)
				if arith_add.match(line):
					op='ADD '
					opi='ADI '
				elif arith_sub.match(line):
					op='SUB '
					opi='SUI '
				elif arith_and.match(line):
					op='ANA '
					opi='ANI '
				elif arith_or.match(line):
					op='ORA '
					opi='ORI '
				vari = a.group(1).strip()
				var1 = a.group(2).strip()
				var2 = a.group(3).strip()
				if var1.isdigit() and var2.isdigit():
					code.append('MVI A, '+var1+'\n')
					code.append(opi+var2+'\n')
					code.append('STA '+symbols[filename][vari]+'\n')
					pp += opcodes['MVI']+opcodes['STA']+opcodes['ADI']
				elif var1.isdigit():
					code.append('LDA '+symbols[filename][var2]+'\n')
					code.append('MOV B, A\n')
					code.append('MVI A, '+var1+'\n')
					code.append(op+'B\n')
					code.append('STA '+symbols[filename][vari]+'\n')
					pp += opcodes['LDA']+opcodes['MOV']+opcodes['MVI']+opcodes['ADD']+opcodes['STA']
				elif var2.isdigit():
					code.append('LDA '+symbols[filename][var1]+'\n')
					code.append(opi+var2+'\n')
					code.append('STA '+symbols[filename][vari]+'\n')
					pp += opcodes['LDA']+opcodes['ADI']+opcodes['STA']
				else:
					code.append('LDA '+symbols[filename][var2]+'\n')
					code.append('MOV B, A\n')
					code.append('LDA '+symbols[filename][var1]+'\n')
					code.append(op+'B\n')
					code.append('STA '+symbols[filename][vari]+'\n')
					pp += opcodes['LDA']+opcodes['MOV']+opcodes['LDA']+opcodes['STA']

			elif line.startswith('loop'):
				a=re.search(r'loop(.*)',line)
				count=a.group(1).strip()
				code.append('PUSH D\n')
				code.append('MVI E, '+count+'\n')
				pp += opcodes['PUSH']+opcodes['MVI']
				loopend.append(str(pp))

			elif line.startswith('endloop'):
				code.append('MOV A, E\n')
				code.append('SUI 1\n')
				code.append('MOV E, A\n')
				code.append('JNZ '+loopend.pop()+'\n')
				code.append('POP D'+'\n')
				pp += opcodes['MOV']+opcodes['SUI']+opcodes['MOV']+opcodes['JNZ']+opcodes['POP']

			elif line.startswith('if'):
				a=re.search(r'if(.*?)\((.*?)\)',line)
				cond = a.group(2)
				if '>' in cond:
					a=re.search(r'(.*?)>(.*)',cond)
					var1 = a.group(1).strip()
					var2 = a.group(2).strip()
					code.append('LDA '+symbols[filename][var1]+'\n')
					code.append('MOV B, A\n')
					code.append('LDA '+symbols[filename][var2]+'\n')
					code.append('SUB B\n')
					startif.append(len(code))
					code.append('JP\n')
					code.append('JZ\n')
					pp += opcodes['LDA']+opcodes['MOV']+opcodes['LDA']+opcodes['SUB']+opcodes['JP']+opcodes['JZ']
				elif '=' in cond:
					a=re.search(r'(.*?)=(.*)',cond)
					var1 = a.group(1).strip()
					var2 = a.group(2).strip()
					code.append('LDA '+symbols[filename][var1]+'\n')
					code.append('MOV B, A\n')
					code.append('LDA '+symbols[filename][var2]+'\n')
					code.append('SUB B\n')
					startif.append(len(code))
					code.append('JNZ\n')
					pp += opcodes['LDA']+opcodes['MOV']+opcodes['LDA']+opcodes['SUB']+opcodes['JNZ']

			elif line.startswith('endif'):
				lineno=startif.pop()
				if code[lineno] is 'JNZ\n':
					code[lineno] = 'JNZ '+str(pp)+'\n'
				elif code[lineno] is 'JP\n':
					code[lineno] = 'JP '+str(pp)+'\n'
					code[lineno+1] = 'JZ '+str(pp)+'\n'

			else:
				a=re.search(r'(.*?)=(.*)',line)
				var=a.group(1).strip()
				val=a.group(2).strip()
				if val.isdigit():
					code.append('MVI A, '+val+'\n')
					code.append('STA '+symbols[filename][var]+'\n')
					pp += opcodes['MVI']+opcodes['STA']
				else:
					code.append('LDA '+symbols[filename][val]+'\n')
					code.append('STA '+symbols[filename][var]+'\n')
					pp += opcodes['LDA']+opcodes['STA']

		# code.append('HLT\n')
		# pp += 1
	code.append('HLT\n')
	filename=files[-1].split('.')[0]
	f=open(filename+'.asm','w')
	f.write(''.join(code))
	f.close()
	f=open(filename+'.assemble','w')
	f.write(''.join(code))
	f.close()
	print filename+'.assemble file generated.'
	return symbols