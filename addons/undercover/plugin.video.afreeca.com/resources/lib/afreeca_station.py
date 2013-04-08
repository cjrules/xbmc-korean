# -*- coding: utf-8 -*-
#
# [관련변수]
#   szBjId        : BJ ID
#   nStationNo    : 방송국 ID (방송국에 여러 BJ 소속가능)
#   nBbsNo        : 게시판 ID (방송국 홈피에 여러 게시판 존재)
#   nTitleNo      : 게시글(또는 동영상) ID
#   nBroadNo      : 생방송 ID
#
# [사이트]
#   BJ Home: http://afreeca.com/<szBjId>
#       (http://live.afreeca.com:8079/app/index.cgi?szBjId=<szBjId>)
#   방송국: http://live.afreeca.com:8079/app/index.cgi?szBjId=<szBjId>&nStationNo=<nStationNo>
#   게시판: http://afbbs.afreeca.com:8080/app/list_ucc_bbs.cgi?szBjId=<szBjId>&nStationNo=<nStationNo>&nBbsNo=<nBbsNo>
#   게시글: http://afbbs.afreeca.com:8080/app/read_ucc_bbs.cgi?szBjId=<szBjId>&nStationNo=<nStationNo>&nBbsNo=<nBbsNo>&nTitleNo=<nTitleNo>
#   생방송: http://player.afreeca.com/<szBjId>

import urllib, urllib2
import re
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

root_url = "http://live.afreeca.com:8079/app/"
UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.9"
PTN_UCC = re.compile('nTitleNo=(\d*)')

nRowNum = 50

def is_broadcasting(uId):
    url = root_url + "index.cgi?szBjId=%s" %uId
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    req.add_header('Accept', "text/html")
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html).find('div', {'class':'app_t'})
    tsec = soup.find('div', {'class':'thum_img'})
    if tsec.find(lambda tag: tag.name=='img' and 'ic_live' in tag['src']):
    	title = soup.find('div', {'class':'title'}).marquee.string
    	thumb = tsec.find('img', {'id':'broadImg'})['src']
    	if 'liveimg' in thumb:
            bNo = re.search('/(\d+)\.', thumb).group(1)
            return {'title':title, 'broad_no':bNo, 'thumbnail':thumb}
        else:
            return {'title':title, 'thumbnail':thumb}
    return None

def parse_ucc(uId, sNo=''):
    if not sNo:
        url1 = root_url + "index.cgi?szBjId=%s&nStationNo=%s" %(uId, sNo)
        print url1
        req = urllib2.Request(url1)
        req.add_header('User-Agent', UserAgent)
        req.add_header('Accept', "text/html")
        html = urllib2.urlopen(req).read()
        sNo = re.search('<meta property="og:url" content="[^"]*nStationNo=(\d+)', html).group(1)
    url = "http://afbbs.afreeca.com:8080/app/list_ucc_bbs.cgi?szBjId=%s&nStationNo=%s&nRowNum=%d&nPageNo=%d" %(uId, sNo, nRowNum, 1)
    print url
    return parse_bbs_by_url(url)

def parse_bbs(uId, sNo, bbsNo):
    url = "http://live.afreeca.com:8079/app/list_ucc_bbs.cgi?szBjId=%s&nStationNo=%s&nBbsNo=%s&nRowNum=%d&nPageNo=%d" %(uId, sNo, bbsNo, nRowNum, 1)
    print url
    return parse_bbs_by_url(url)

def parse_bbs_by_url(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    result = {'video':[]}
    for item in soup.find('div', {'class':'vod_list'}).findAll('li'):
    	url = item.a['href']
    	uccno = PTN_UCC.search(url).group(1)
    	title = item.a.string
    	thumb = item.find('dd', {'class':'thum'}).img['src']
    	result['video'].append({'title':title, 'ucc_id':uccno, 'thumbnail':thumb})
    # TODO: Ugly page navigation structure
    #     goListPage(nPageNo)
    return result

def extractUccUrl(uid, vid):
    url = "http://afbbs.afreeca.com:8080/api/flv_player_env.php?uid=%s&nTitleNo=%s" % (uid, vid)
    xml = urllib.urlopen(url).read()
    soup = BeautifulStoneSoup(xml, fromEncoding='euc-kr')

    try:
        pageUrl = soup.find("movieurl").string
        swfUrl = soup.find('fulllink').string
    except:
        return None

    xml = urllib.urlopen(pageUrl).read()
    soup = BeautifulStoneSoup(xml, fromEncoding='euc-kr')
    #soup.find('title').string
    #soup.find('thumb').string
    result = extractRtmpUrl( soup.find('flv_name').string )
    result['pageUrl'] = pageUrl
    result['swfUrl'] = swfUrl
    return result

def extractRtmpUrl(url):
    vidtype = url[ url.rfind('.')+1 : ]
    pos = url.find('flv')
    vidhost = url[ pos : url.find('.',pos) ]
    vidurl = url[ url.find('/',7)+1 : ]

    app_name = 'af'+vidhost+'/_definst_'
    return {'app'     :  app_name,
            'tcUrl'   :  "rtmp://"+vidhost+".afreeca.com/"+app_name,
            'playpath': vidtype+":"+vidurl}

# RTMP
# IP host: 180.68.204.196
# TCP port 1935: macromedia-fcs
# (1) Handshake C0(0x03)+C1(1536 random byte)
# (2) Handshake C2(S1) + Connect('afflv1/_definst_')
#   'app':'afflv1/_definst_'
#   'flashVer':'WIN 11,3,300,265'
#   'swfUrl':'http://afbbs.afreeca.com:8080/playerorg.swf?uid=trtv&nTitleNo=103071'
#   'tcUrl':'rtmp://flv1.afreeca.com/afflv1/_definst_'
#   'fpad':false
#   'capabilities':239
#   'audioCodecs':3575
#   'videoCodecs':252
#   'videoFunction':1
#   'pageUrl':'http://afbbs.afreeca.com:8080/app/read_ucc_bbs.cgi?nStationNo=1752122&nTitleNo=103071&szBjId=trtv&szSkin=gmpremium'
# (3) Receive S0+S1+S2
# (4) Play('flv:AFFLV/03/2/20/1_03_192622_080717195020.flv'
# (5) onStatus('NetStream.Play.Reset') | ... | onStatus('NetStream.Play.Start')

if __name__ == "__main__":
    print is_broadcasting('house2222')
    #print parse_ucc('house2222', '')
    #print parse_ucc('house2222', '5180346')
    #print parse_bbs('house2222', '5180346', '11159637')
    #print extractUccUrl('house2222', '3428584')

# vim:sw=4:sts=4:et
