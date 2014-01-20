#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import httplib, urllib

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag

from Utf8ToCNSMap import code_map

def convertUtf8ToHex(char):
    return repr(char)[4:-1].upper()

def convertUtf8HexToCNS(char):
    if code_map.has_key(char):
        return code_map[char]
    else:
        return None

def formatCNS(char):
    if char[0] == '0':
        return char[1] + char[3:]
    else:
        return char[0:2] + char[3:]

def postQuery(char,page_num='0'):
    params = urllib.urlencode({'cns': char, 'font': '', 'author': '', 'cnscode':'1455f', 'pageNo':page_num})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.cns11643.gov.tw")
    conn.request("POST", "/AIDB/fm_results.do", params, headers)
    response = conn.getresponse()
    #print response.status, response.reason
    
    data = response.read()
    data = data.replace("530","100%")
    soup = BeautifulSoup(data)

    baseTag = Tag(soup, "base")
    baseTag['href'] = "http://www.cns11643.gov.tw/AIDB/"
    soup.head.insert(0,baseTag)

    soup.head.title.contents[0].replaceWith(unicode("CalliPlus 搜尋結果","utf-8"))

    #soup.h3.clear()
    #soup.p.clear()

    tds_link = soup.findAll("td", width='100')
    tds_desc = soup.findAll("td", bgcolor="#F2EAC4")

    div = soup.find("div", class_="maincolumn_content")

    conn.close()
    return soup.head, tds_link, tds_desc

def generateHTML(arg):
    count = 0 
    html = ""
    for character in arg:
        hexcode = convertUtf8ToHex(character)
        #print hexcode
        cns = convertUtf8HexToCNS(hexcode)
        if cns == None:
            continue
        #print cns
        formatCode = formatCNS(cns)
        #print formatCode
        header, tds_link, tds_desc = postQuery(formatCode)
        if count == 0:
            html += repr(header)
            html += "<body><table>"
        html += "<tr>"
        for i in tds_link:
            html += repr(i)
        html += "<tr>"
        for i in tds_desc:
            html += repr(i)
    html += "</body>"
    return html

if __name__ == '__main__':
    if len(sys.argv) < 1:
       exit(0) 

    arg = unicode(sys.argv[1],'utf-8')
    if len(arg) > 0:
        html = generateHTML(arg)
        open("output.html","w+").write(html).close()
        os.system("open output.html")
