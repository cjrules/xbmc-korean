# -*- coding: utf-8 -*-
import urllib, urllib2
import re
from BeautifulSoup import BeautifulSoup

root_url = "http://www.koreayh.com"

def parseList(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = {}
    link = []
    for item in soup.find("ul",{"class":"filmListShow"}).findAll("li"):
        thumb = root_url + item.find('img')['data-original']
    	aa = item.dl.dt.a
        title = aa.font.string
        url = root_url + aa['href']
        link.append( {'title':title,'url':url,'thumb':thumb} )
    result['link'] = link
    sec = soup.find("div",{"id":"page_nav"})
    prevpg = sec.find(text=re.compile(u"이전"))
    if prevpg:
        url = root_url + prevpg.parent['href']
        if url != main_url:
            result['prevpage'] = url
    nextpg = sec.find(text=re.compile(u"다음"))
    if nextpg:
        url = root_url + nextpg.parent['href']
        if url != main_url:
            result['nextpage'] = url
    return result

# hotplay
def parseHotList(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = {}
    link = []
    for item in soup.find("div",{"class":re.compile("play_best_list")}).findAll("li"):
    	aa = item.find('a')
        title = aa.string.strip()
        url = root_url + aa['href']
        link.append( {'title':title,'url':url,'thumb':''} )
    result['link'] = link
    return result

def parseProg(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    # playlist
    link = []
    sec = soup.find("ul",{"id":"sort_video_list"})
    for item in sec.findAll("li"):
    	title = item.span.string
    	for aa in item.findAll("a"):
    	    if aa['class'] == 'youku':
    	    	url = aa['data-id']
    	    elif aa['class'] == 'tudou':
    	    	url = aa['data-id']
    	    elif aa['class'] == 'sohu':
    	    	url = aa['data-id']
    	    elif aa['class'] == 'leshi':
    	    	url = aa['data-id']
    	    elif aa['class'] == 'pptv':
    	    	url = aa['data-id']
    	    else:
    	    	url = None
            if url:
                link.append( {'title':title,'url':url} )
    return link

# /player/playurl?film=<id>&film_=<$(data-index)-1>&type=<youku|tudou|...>&film_code=<>&
def parseVideoPlay(main_url):
    url = root_url + "/player/playurl"
    values = {
    	'film':'1318',
    	'film_':'0',
    	'type':'youku',
    	'film_code':'92B45C7804994CE4FF7651604109BBBD', # generated from 25502?
    }
    #data = urllib.urlencode(values)
    data = "film=1318&film_=0&type=youku&film_code=92B45C7804994CE4FF7651604109BBBD"
    req = urllib2.Request(url, data)
    req.add_header('Referer', "http://www.koreayh.com/play/1318/%EB%93%9C%EB%A6%BC%ED%95%98%EC%9D%B4%202")
    resp = urllib2.urlopen(req)
    html = resp.read()
    resp.close()
    return html

if __name__ == "__main__":
    #result = parseList(root_url+"/vlist/24/1/24")
    #print len(result['link'])
    #print result['nextpage']
    #result = parseHotList(root_url+"/vlist/24/1/24")
    #print len(result['link'])
    #result = parseProg(root_url+"/tv/Show.php?classid=10&id=31679")
    #print len(result['playlist'])
    print parseVideoPlay('25502')

# vim:sw=4:sts=4:et
