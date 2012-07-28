# -*- coding: utf-8 -*-
import urllib
import re
from BeautifulSoup import BeautifulSoup

root_url = "http://tv.yb88.com"

def parseList(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = {}
    link = []
    for item in soup.find("div",{"class":"MAIN"}).findAll("dd"):
    	aa = item.find('a')
        title = aa['title']
        url = aa['href']
        thumb = aa.find('img')['src']
        link.append( {'title':title,'url':url,'thumb':thumb} )
    result['link'] = link
    sec = soup.find("div",{"class":"list-page pagepage"})
    prevpg = sec.find(text=lambda(x) : x == "Prev")
    if prevpg:
        result['prevpage'] = prevpg.parent['href']
    nextpg = sec.find(text=lambda(x) : x == "Next")
    if nextpg:
        result['nextpage'] = nextpg.parent['href']
    return result

def parseProg(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = {}
    # playlist
    link = []
    for aa in soup.find("dd",{"class":re.compile("^Content-view-mlink")}).findAll("a"):
    	if aa['href'].find('/play/') > 0:
            link.append({'title':aa.string,'url':aa['href'].replace('&amp;','&')})
    result['playlist'] = link
    # other episodes
    sec = soup.find("div",{"class":re.compile("^Content-list")}).find('ul')
    link = []
    for aa in sec.findAll('a'):
        link.append({'title':aa['title'],'url':aa['href'].replace('&amp;','&')})
    result['episodes'] = link
    return result

def parseVideoPlay(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    return re.compile("<script>show\('(.*)'\);</script>").search(html).group(1)

if __name__ == "__main__":
    result = parseList(root_url+"/tv/Entertainment/")
    print len(result['link'])
    print result['nextpage']
    result = parseProg(root_url+"/tv/Show.php?classid=10&id=31679")
    print len(result['playlist'])
    print parseVideoPlay(root_url+"/play/?classid=10&id=31376&pathid=2")

# vim:sw=4:sts=4:et
