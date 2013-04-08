# -*- coding: utf-8 -*-
# [Site]
#   한국야구: http://sportstv.afreeca.com/kbo/
#   일본야구: http://sportstv.afreeca.com/npb/
#   e스포츠:  http://sportstv.afreeca.com/esports/
#
#   동영상:
#       <c_id>:     [esports_highlight|esports_replay]
#       <b_no>:
#       <btype>:    'esports':[GSL|GSTL|LOL]
#       <szPos>:    [kbo|mlb|npb|kfa|afc|ufa|chams|kbl|kov|etc|esports]
#   Script: http://www.afreeca.com/script/new_main/sportstv_neo.js
#
#   Highlight:
#   Replay: SPORTS_TV+'/<szPos>/replay.php?&szSubBtype=<type>'
#
#   View1: http://sportstv.afreeca.com/?board=vod&c_id=<c_id>&b_no=<b_no>&control=view&szSubBtype=<type>
#       -> View2
#   View2: http://sportstv.afreeca.com/bbs/index.php?board=vod&c_id=<c_id>&b_no=<b_no>&control=view&c_sub_btype=<type>
#       -> Proxy needed
#
# [Data]
#   http://www.afreeca.com/data/sportstv/neo_sports_best.js
#   http://www.afreeca.com/data/sportstv/neo_esports_best.js
#   http://www.afreeca.com/data/sportstv/neo_esports_today_broad.js
#   Script: http://www.afreeca.com/script/new_main/sportstv_main.js

import urllib, urllib2
from urlparse import parse_qs
import re
from BeautifulSoup import BeautifulSoup
import simplejson
import xml.etree.ElementTree as etree

UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.9"

root_url = "http://sportstv.afreeca.com"

def getSportsBest():
    url = "http://www.afreeca.com/data/sportstv/neo_sports_best.js"
    jstr = urllib.urlopen(url).read().decode('euc-kr')
    json = simplejson.loads( jstr[jstr.find('{') : jstr.rfind(';')] )
    return json['BEST_INFO']

def getEsportsBest():
    url = "http://www.afreeca.com/data/sportstv/neo_esports_best.js"
    jstr = urllib.urlopen(url).read().decode('euc-kr')
    json = simplejson.loads( jstr[jstr.find('{') : jstr.rfind(';')] )
    return json['BEST_INFO']

def parseBoard(c_id, sub_btype, pageNo=''):
    page_url = root_url+'/bbs/index.php?board=vod&c_id=%s&c_sub_btype=%s' %(c_id, sub_btype)
    if pageNo:
    	page_url += '&pageNo='+pageNo
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    result = {'video':[]}
    # video list
    ptn_bno = re.compile('goView\((\d+)\)')
    for item in soup.find('div', {'class':'vod_list'}).findAll('li'):
    	thumb = item.findAll('img')[1]['src']
    	a_node = item.findAll('a')[1]
    	title = a_node.string
    	b_no = ptn_bno.search(a_node['href']).group(1)
    	result['video'].append({'title':title, 'b_no':b_no, 'thumbnail':thumb})
    # navigation
    curpg = soup.find('div', {'class':re.compile("^paginate")}).find('strong')
    prevpg = curpg.findPreviousSibling('a')
    if prevpg:
    	result['prev_pgno'] = prevpg.string
    nextpg = curpg.findNextSibling('a')
    if nextpg:
    	result['next_pgno'] = nextpg.string
    return result

def parseReplayAll(szPos, subBtype):
    page_url = root_url+'/'+szPos+'/replay.php?&szSubBtype='+subBtype
    print page_url
    html = urllib.urlopen(page_url).read()
    new_url = root_url + re.search('<iframe[^>]*src="([^"]*)"', html).group(1)
    print new_url
    html = urllib.urlopen(new_url).read()
    print html
    return None

def getInfoById(c_id, b_no, btype, proxy=None):
    url = root_url+"/bbs/index.php?board=vod&c_id=%s&b_no=%s&control=view&c_sub_btype=%s" %(c_id, b_no, btype)
    return parseVideoPage(url, proxy)

def parseVideoPage(page_url, proxy=None):
    if 'szSubBtype' in page_url:
    	html = urllib.urlopen(page_url).read()
    	page_url = re.search('<iframe[^>]*src="([^"]*)"', html).group(1).replace('&amp;','&')
    	print page_url
    qq = parse_qs(page_url.split('?', 1)[1])
    c_id = qq['c_id'][0]
    b_no = qq['b_no'][0]
    if 'c_sub_btype' in qq:
        btype = qq['c_sub_btype'][0]
    else:
        btype = ''

    if proxy:
        handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(handler)
    else:
        opener = urllib2.build_opener()
    #urllib2.install_opener(opener)

    opener.addheaders = [ ("User-Agent", UserAgent), ("Accept", "text/html") ]
    html = opener.open(page_url).read()

    # META property="og:title" content=""
    # META property="og:description" content=""
    # META property="og:image" content=""
    # META property="og:video" content=""
    idx = re.search("FlashVars='[^']*idx=(\d+)[^']*'", html).group(1)
    return {'c_id':c_id, 'b_no':b_no, 'sub_btype':btype, 'idx':idx}
    
def extractStreamUrl(c_id, b_no, sub_btype, idx):
    url2 = "http://afbbs.afreeca.com:8080/api/video/get_sports_info.php?c_sub_btype=%s&c_id=%s&idx=%s&control=view&board=vod&b_no=%s&autoPlay=true" %(sub_btype, c_id, idx, b_no)
    xml = urllib2.urlopen(url2).read()
    #print xml
    root = etree.fromstring(xml)
    title = root.find('.//title').text
    #rtmp_url = root.find('.//track/video[@duration]').text
    for video in root.findall('.//video'):
    	if video.text.startswith('rtmp'):
            rtmp_url = video.text
    thumb = root.find('.//titleImage').text
    return {'title':title, 'url':rtmp_url, 'thumbnail':thumb}

if __name__ == "__main__":
    proxy = "http://175.209.211.180:8888/"

    #print getSportsBest()
    #print getEsportsBest()

    #info = parseVideoPage( root_url+"/?board=vod&c_id=npb_highlight2&control=view&b_no=29692&szSubBtype=", proxy=proxy )
    #info = parseVideoPage( root_url+"/bbs/index.php?board=vod&c_id=esports_replay&b_no=29674&control=view&c_sub_btype=GSL", proxy=proxy )
    #print extractStreamUrl(info['c_id'], info['b_no'], info['sub_btype'], info['idx'])

    print parseBoard('esports_highlight', 'GSL')
    #print parseReplayAll('esports', 'GSL')

# vim:sw=4:sts=4:et
