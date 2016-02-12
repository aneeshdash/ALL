import re
import sys 


def search_ext(myDict, lookup):
    a=[]
    for key, value in myDict.items():
        if lookup in value:
            a.append(key)
    return a


def search_var(myDict, lookup):
    a=""
    for key, value in myDict.items():
        if lookup in key:
            return value
    return a
    
def linker(filename, symbols):
    ext_var = [] 
    var_adr = {}
    for key in symbols:
        ext_var = ext_var + search_ext(symbols[key], 'extern')

    for var in ext_var:
    	for key in symbols:
    		b=search_var(symbols[key], var)
    		if b is not "" :
    			var_adr[var]=b	

    f=open(filename,'r')
    data=f.read()
    f.close()
    for key in var_adr:
    	data=data.replace('extern'+key ,var_adr[key])
    f=open(filename,'w')
    f.truncate()
    f.write(data)
    f.close()
    f=open(filename.split('.')[0]+'.link','w')
    f.write(data)
    f.close()
    print filename.split('.')[0]+'.link file generated'