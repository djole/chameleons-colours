'''
Created on May 29, 2013

@author: djordje
'''
in_string = ''
with open ("./params.txt", "r") as params_file:
    in_string += params_file.read().replace('\n', '')
data = in_string.split(';')

parameters = {}

for d in data:
    if d.count(' ') == len(d): continue
    try:
        ass, ty = d.split(':')
    except:
        print "cannot unpack", d
        continue
    key, val_raw = ass.split('=')
    
    if ty == 'str': val = str(val_raw)
    elif ty == 'int': val = int(val_raw)
    elif ty == 'float': val = float(val_raw)
    else: raise TypeError
    parameters[key] = val

