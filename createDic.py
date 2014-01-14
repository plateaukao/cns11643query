
import sqlite3 as lite

lines = open('unicode.txt','r').readlines()
dicc = {}
for l in lines:
    if not l[0] == '#':
        words = l[:-1].split()
        key = words[1]
        value = words[0]
        dicc[key] = value

print dicc


