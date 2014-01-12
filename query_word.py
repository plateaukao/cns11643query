#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import httplib, urllib

def convertUtf8ToHex(char):
    u = unicode(char,'utf-8')
    return repr(u)[4:-1].upper()

def convertUtf8HexToCNS(char):
    
    command = "awk '$2 ~ /^%s/ {print $1}' *" % (char)
    output = os.popen(command).read()
    return output[:-1]

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
    print response.status, response.reason
    
    data = response.read()
    data = data.replace("<head>", "<head><base href='http://www.cns11643.gov.tw/AIDB/' />")
    conn.close()
    return data

if __name__ == '__main__':
    if len(sys.argv) < 1:
       exit(0) 

    hexcode = convertUtf8ToHex(sys.argv[1])
    #print hexcode
    cns = convertUtf8HexToCNS(hexcode)
    #print cns
    formatCode = formatCNS(cns)
    #print formatCode
    data = postQuery(formatCode)
    f = open('output.html', 'w+')
    f.write(data)
    f.close()
