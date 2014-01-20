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

    #remove useless link and script
    links = soup.findAll('link')
    [link.extract() for link in links]
    scripts = soup.findAll('script')
    [script.extract() for script in scripts]

    #soup.h3.clear()
    #soup.p.clear()

    totals = soup.findAll(attrs={"class":"con"})
    total_chr = totals[0].contents[0]
    total_page = totals[1].contents[0]
    cnsvalue = soup.findAll(attrs={"name":"cns"})[0]['value']

    tds_link = soup.findAll("td", width='100')
    tds_desc = soup.findAll("td", bgcolor="#F2EAC4")

    div = soup.find("div", class_="maincolumn_content")

    conn.close()
    return soup.head, tds_link, tds_desc, total_chr, total_page, cnsvalue.encode('ascii')

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
        header, tds_link, tds_desc,total_chr, total_page,cnsvalue = postQuery(formatCode)
        print total_chr, total_page
        # add header part
        if count == 0:
            html += "<html>"
            html += repr(header)
            html += """<body>
            <form name="queryForm" id="queryForm" method="post" action="fm_results.do" target="_blank">
            <input name="cns" type="hidden" value="0"><input name="font" type="hidden" value=""><input name="author" type="hidden" value=""><input name="pageNo" type="hidden" value="0">
            </form>
           <script language="javascript" type="text/JavaScript">
             function query(page, cv) {
                 document.queryForm.pageNo.value = page+"";
                 document.queryForm.cns.value=cv+"";
                 document.queryForm.submit();
             }
            </script>"""
        # character official page links
        html += "<table ><tr><td bgcolor='#DBDBDB' colspan='42'>%s 共有%d個字; %d頁  " % (character.encode('utf8'), int(total_chr), int(total_page))
        for i in range(int(total_page)):
            html += "<a href='javascript:query(%d,%s);'>第%d頁</a> | " % (i, cnsvalue, i+1)
        # images and description
        image_line = ""
        desc_line = ""
        for i in range(len(tds_link)):
            if i % 10 == 0:
                if i > 0:
                    html += image_line + desc_line
                    image_line = ""
                    desc_line = ""
                image_line += "<tr>"
                desc_line += "<tr>"
            if -1 != repr(tds_desc[i]).find("&nbsp;"):
                continue
            image_line += repr(tds_link[i])
            desc_line += repr(tds_desc[i])
        if image_line != "":
            html += image_line + desc_line

        html += "<br>"
        count += 1
    html += "</body></html>"
    return html

if __name__ == '__main__':
    if len(sys.argv) < 1:
       exit(0) 

    arg = unicode(sys.argv[1],'utf-8')
    if len(arg) > 0:
        html = generateHTML(arg)
        open("output.html","w+").write(html).close()
        os.system("open output.html")
