# -*- coding: utf-8 -*-
import urllib
import re
from BeautifulSoup import BeautifulSoup

root_url = "http://school.ohmynews.com"

def parseTop(main_url):
    result = []
    html = urllib.urlopen(main_url).read()
    soup = BeautifulSoup(html)
    result = []
    for sec in soup.findAll("div", {"id":"online_listout"}):
    	thumb = sec.find('img')['src']
    	aa = sec.find("div",{"class":"online_list_title"}).a
    	title = ''.join(aa.findAll(text=True)).strip()
    	url = main_url[ : main_url.rfind('/')] + '/' + aa['href']
    	result.append( (title, url, thumb) )
    return result

def parseLecture(main_url):
    html = urllib.urlopen(main_url).read()
    soup = BeautifulSoup(html)
    result = []
    for item in soup.find("div", {"class":"curriculum_list"}).findAll("li"):
    	title = u"[B]%s[/B] " % item.em.string
    	title += ''.join(item.a.findAll(text=True)).strip()
    	url = main_url[ : main_url.rfind('/') ] + "/" + item.a['href']
    	result.append( (title, url) )
    return result

def parseVideo(main_url):
    result = {}

    html = urllib.urlopen(main_url).read()
    pageUrl = root_url + re.compile('<div class="c_vod"><iframe.*src="(.*)"></iframe></div>').search(html).group(1)

    html = urllib.urlopen(pageUrl).read()
    swfUrl = root_url + re.compile("<object.*><embed.*src='(.*?)'.*/></object>").search(html).group(1)

    cdn = re.compile("cdn_path=(.*?)&").search(swfUrl).group(1)

    result['app'] = 'ohmyfree'
    result['tcUrl'] = "rtmp://cdnfs.ohmynews.com/"+result['app']
    result['pageUrl'] = pageUrl
    result['swfUrl'] = swfUrl
    result['playpath'] = "/TV/%s/%s.mp4" % (cdn[-2:], cdn)

    return result

# RTMP
# IP host: cdnfs.ohmynews.com
# TCP port 1935: macromedia-fcs
# (1) Handshake C0(0x03)+C1(1536 random byte)
# (2) Receive S0+S1+S2
# (3) Handshake C2(S1) + Connect('ohmyfree')
#   'app':'ohmyfree'
 #   'flashVer':'WIN 11,3,300,265'
 #   'swfUrl':swfurl
 #   'tcUrl':'rtmp://cdnfs.ohmynews.com/ohmyfree'
 #   'fpad':false
 #   'capabilities':239
 #   'audioCodecs':3575
 #   'videoCodecs':252
 #   'videoFunction':1
 #   'pageUrl':pageurl
 # (4) Play('/TV/%s/%s.mp4' % (cdn[-2:], cdn))
 # (5) onStatus('NetStream.Play.Reset') | ... | onStatus('NetStream.Play.Start')

if __name__ == "__main__":
    lccd = "SO000001444"
    url = root_url+"/NWS_Web/School/online_pg.aspx?lccd=%s&free=t" % lccd
    print parseLecture(url)
    exit(0)

    #
    pricecode = "PR000000481"
    url = root_url+"/NWS_Web/School/online_pg.aspx?lccd=%s&pricecode=%s&free=t" % (lccd, pricecode)
    print url

    info = parseVideo(url)
    print "%s app=%s swfUrl=%s pageUrl=%s playpath=%s" % (info['tcUrl'], info['app'], info['swfUrl'], info['pageUrl'], info['playpath'])

# vim:sw=4:sts=4:et
