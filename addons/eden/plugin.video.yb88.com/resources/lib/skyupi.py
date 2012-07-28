# -*- coding: utf-8 -*-
import urllib
import re
from BeautifulSoup import BeautifulSoup

def parseList(main_url):
    html = urllib.urlopen(main_url).read()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = []
    items = soup.find("div",{"class":re.compile("^VIEWS-content")}).findAll("b")
    for item in items[:-2]:
    	aa = item.find('a')
        title = aa['title']
        url = aa['href']
        #date = item.findNextSibling().string
        result.append( {'title':title,'url':url} )
    return result

def parseProg(main_url):
    html = urllib.urlopen(main_url).read()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = []
    sec = soup.findAll("div",{"class":re.compile("^VIEWS-160")})[1]
    # unstructured format...
    return result

if __name__ == "__main__":
    print parseList("http://www.skyupi.com/List.php?classid=10")
    print parseProg("http://www.skyupi.com/Show.php?classid=10&id=31679")

# vim:sw=4:sts=4:et
