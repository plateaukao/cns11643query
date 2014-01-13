
import sqlite3 as lite

lines = open('unicode.txt','r').readlines()
con = lite.connect('map.db')

with con:
    cur = con.cursor()    
    cur.execute("CREATE TABLE Mapping(UTF8 PRIMARY KEY, CNS TEXT)")

    for l in lines:
        if not l[0] == '#':
            words = l[:-1].split()
            key = words[1]
            value = words[0]
            cur.execute("INSERT INTO Mapping VALUES('%s', '%s')" % (key, value))



