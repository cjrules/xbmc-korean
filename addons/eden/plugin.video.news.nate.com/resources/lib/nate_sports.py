# -*- coding: utf-8 -*-
"""
  sports.news.nate.com/esports
"""
import urllib, urllib2, re
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

BrowserAgent = "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/ 20120405 Firefox/14.0.1"

root_url = "http://sports.news.nate.com"

def parseVod(main_url):
    return []   # not yet implemented

def parseSortList(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', BrowserAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, fromEncoding='euc-kr')
    sort_info = []
    for aa in soup.find("ul", {"id":"selectDesign"}).findAll("a"):
        sort_info.append( {"name":aa.string, "url":aa['href'].replace('&amp;','&')} )
    return sort_info

def parseTeamList(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', BrowserAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, fromEncoding='euc-kr')
    team_info = []
    for aa in soup.find("ul", {"class":re.compile("^esp_teamTab_sc")}).findAll("a"):
        team_info.append( {"name":aa.string, "url":aa['href'].replace('&amp;','&')} )
    return team_info

def parseESports(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', BrowserAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, fromEncoding='euc-kr')
    vod_info = []
    for sec in soup.findAll("div", {"class":re.compile("^vodPlayList")}):
    	vodgrp = {"list":[]}
    	if sec.h5:
            vodgrp['title'] = " ".join(sec.h5.findAll(text=True))
        for item in sec.findAll("li"):
            aa = item.findAll('a')[1]
            title = aa['title']
            aid = re.compile("aid=(\w*)").search(aa['href']).group(1).encode('ascii')
            thumb = item.find('img')['src']
            vodgrp['list'].append({"title":title,"aid":aid,"thumb":thumb})
    	vod_info.append(vodgrp)
    return vod_info

def parseProg(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', BrowserAgent)
    html = urllib2.urlopen(req).read()
    vod_sq,vod_key = re.compile(r"vod_sq\s*:\s*'(\d+)',\n\s*vod_key\s*:\s*'(\w+)',").search(html).group(1,2)
    return (vod_sq, vod_key)

def parseProg2(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', BrowserAgent)
    html = urllib2.urlopen(req).read()
    vod_sq,vod_key = re.compile(r"video_player\('(\d+)','(\w+)',").search(html).group(1,2)
    return (vod_sq, vod_key)

def getVideoUrl(vod_sq, vod_key):
    url = "http://v.nate.com/movie_url.php?mov_id=%s&v_key=%s&type=xml" % (vod_sq, vod_key)
    xml = urllib2.urlopen(url).read()
    #dom = xml.dom.minidom.parseString(xml)   # encoding error?
    soup = BeautifulStoneSoup(xml, fromEncoding='euc-kr')
    vid_url = urllib.unquote(soup.movie.mov_url.string)
    img_url = soup.movie.master_thumbnail.url.string
    return (vid_url, img_url)

if __name__ == "__main__":
    #url = root_url+"/abrsoccer/vod?sec=abrsoccer_bd"     # 분데스리가
    #url = root_url+"/abrsoccer/vod?sec=abrsoccer_la"     # 라리가
    #url = root_url+"/abrbaseball/vod?sec=abrbaseball_m"  # MLB
    #url = root_url+"/general/vod?sec=esports"
    #url = root_url+"/general/vod?sec=esports_sf"
    #info = parseVod(url)

    #url = root_url+"/esports/vod?sec=esports"    # SK플래닛 SC프로리그
    #url = root_url+"/esports/vod?sec=esports_s"  # 4G LTE SF2프로리그
    #url = root_url+"/esports/vod?sec=esports_tv" # 티빙 스타리그
    #url = root_url+"/esports/vod?sec=esports&vt=time"    # 시간별
    url = root_url+"/esports/vod?sec=esports&vt=clst"    # 경기별
    #url = root_url+"/esports/vod?sec=esports&vt=team"    # 팀별

    info = parseESports(url)
    for vodlst in info:
        print vodlst['title'].encode('utf-8')
        for item in vodlst['list']:
            print "%s : %s" % (item['title'].encode('utf-8'), item['aid'])

    #html = urllib2.urlopen(url).read()
    #open("b.html", "w").write(html)

    aid = info[0]['list']['aid']
    vod_sq,vod_key = parseProg(root_url+"/view/"+aid)
    #vod_sq,vod_key = parseProg(root_url+"/spo/vodPopup?aid=20120724n21082&epo=1&clst_id=368440")
    print getVideoUrl(vod_sq,vod_key)

# vim:sts=4:et
