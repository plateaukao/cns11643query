#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import httplib, urllib
import sqlite3 as lite

from bs4 import BeautifulSoup

con = lite.connect('map.db')

def convertUtf8ToHex(char):
    return repr(char)[4:-1].upper()

def convertUtf8HexToCNS(char):
    
    #command = "awk '$2 ~ /^%s/ {print $1}' *" % (char)
    #output = os.popen(command).read()
    with con:
        cur = con.cursor() 
        cur.execute("SELECT CNS FROM Mapping WHERE UTF8='%s'" % (char))
        con.commit()

        row = cur.fetchone()
        if len(row) > 0:
            return row[0]

def formatCNS(char):
    if char[0] == '0':
        return char[1] + char[3:]
    else:
        return char[0:2] + char[3:]

def postQuery(char):
    params = urllib.urlencode({'cns': char, 'font': '', 'author': '', 'cnscode':'1455f'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.cns11643.gov.tw")
    conn.request("POST", "/AIDB/fm_results.do", params, headers)
    response = conn.getresponse()
    #print response.status, response.reason
    
    data = response.read()
    data = data.replace("<head>", "<head><base href='http://www.cns11643.gov.tw/AIDB/' />")
    data = data.replace("530","100%")
    soup = BeautifulSoup(data)
    #soup.head.append("<base href='http://www.cns11643.gov.tw/AIDB/' />")
    soup.h3.clear()
    soup.p.clear()
    div = soup.find("div", class_="maincolumn_content")
    div.table.td['colspan'] = 10

    conn.close()
    return soup.head, div 

if __name__ == '__main__':
    if len(sys.argv) < 1:
       exit(0) 

    arg = unicode(sys.argv[1],'utf-8')
    if len(arg) > 0:
        f = open('output.html', 'w+')
        count = 0 
        for character in arg:
            hexcode = convertUtf8ToHex(character)
            #print hexcode
            cns = convertUtf8HexToCNS(hexcode)
            #print cns
            formatCode = formatCNS(cns)
            #print formatCode
            header, data = postQuery(formatCode)
            if count == 0:
                f.write(repr(header))
                f.write("<body><table><tr><td>")
                f.write(repr(data))
                f.write("</td>")
                count += 1 
            elif count % 2 != 0:
                f.write("<td>")
                f.write(repr(data))
                f.write("</td></tr>")
                count += 1
            else:
                f.write("<td>")
                f.write(repr(data))
                f.write("</td>")
                count += 1
        f.write("</table></body>")
        f.close()
        os.system('open output.html')
