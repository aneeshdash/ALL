import re,assemble,link,loader,machine
files=[]
print 'Enter file names(in descending order of execution):'
while True:
	print 'File Name:',
	fname=raw_input()
	if fname is '':
		break;
	files.append(fname)
print 'Enter Offset:',
offset=int(raw_input())
main=files[-1].split('.')[0]+'.asm'
symbols=assemble.assemble(files)
link.linker(main, symbols)
loader.loader(main, offset)
machine.machine(main)
print 'Symbol Table:'
for key in symbols:
	print 'File: '+key
	print symbols[key]
