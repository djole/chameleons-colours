'''
Created on May 29, 2013

@author: djordje
'''
import sys

in_args = sys.argv
parameters_file = "./params.txt" if len(in_args) == 1 else in_args[1]
print parameters_file
in_string = ''
with open (parameters_file, "r") as params_file:
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
    elif ty == 'bool': val = bool(int(val_raw))
    else: raise TypeError
    parameters[key] = val

