# -*- coding: utf-8 -*-
#
# [사이트]
#   Hot: 
#   OnAir: 생방송 리스트

import urllib2
import re
from BeautifulSoup import BeautifulSoup

root_url = "http://m.afreeca.com"

IPadAgent = "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) Mobile"

AFPLAY_PTN = re.compile("afPlay\((\d+)\)")

# http://m.afreeca.com/index.php
def parseMobileHot( main_url ):
    req = urllib2.Request( main_url )
    req.add_header('User-Agent',IPadAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup( html )
    pl = []
    for item in soup.findAll("dl", {"class":"onair"}):
    	thumb = item.find('img')['src']
    	aa = item.dt.a
    	title = aa.string
    	jstr = aa['href']
    	try:
            bnum = int(AFPLAY_PTN.search( jstr ).group(1))
            pl.append( {'title':title, 'broad_no':bnum, 'thumbnail':thumb} )
        except:
            pass
    return {'video':pl}

# http://m.afreeca.com/onair.php
def parseMobileOnAir( main_url ):
    req = urllib2.Request( main_url )
    req.add_header('User-Agent',IPadAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup( html )
    result = {'video':[]}
    for item in soup.find("ul", {"class":"on_list1"}).findAll("li"):
    	thumb = item.find('img')['src']
    	aa = item.dl.dt.a
    	title = aa.string
    	jstr = aa['href']
    	try:
            bnum = int(AFPLAY_PTN.search( jstr ).group(1))
            result['video'].append( {'title':title, 'broad_no':bnum, 'thumbnail':thumb} )
        except:
            pass
    # paging
    base_url = main_url
    pos = main_url.rfind('?')
    if pos > 0:
        base_url = main_url[:pos]
    sec = soup.find("div", {"class":"paging"})
    curpg = sec.strong
    prevpg = curpg.findPreviousSibling('a')
    PGNUM_PTN = re.compile("goPage\((\d+)\);")
    if prevpg:
    	result['prevpage'] = base_url+"?page_no="+PGNUM_PTN.search(prevpg['href']).group(1)
    nextpg = curpg.findNextSibling('a')
    if nextpg:
    	result['nextpage'] = base_url+"?page_no="+PGNUM_PTN.search(nextpg['href']).group(1)
    return result

def getStreamUrlByBroadNum( bnum ):
    url = "http://istream.m.afreeca.com/stream/route/%d.m3u8?fr=w" %bnum
    #return url
    html = urllib2.urlopen(url).read()
    murls = re.compile('(http://.*)', re.M).findall(html)
    return murls[-1] if murls else None     # the best quality

if __name__ == "__main__":
    print parseMobileHot( "http://m.afreeca.com/index.php" )
    print parseMobileOnAir( "http://m.afreeca.com/onair.php" )
    print parseMobileOnAir("http://m.afreeca.com/onair.php?page_no=5")
    print getStreamUrlByBroadNum(31476971)

# vim:sw=4:sts=4:et
