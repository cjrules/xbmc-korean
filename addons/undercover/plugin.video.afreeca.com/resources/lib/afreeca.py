# -*- coding: utf-8 -*-
#
# [관련변수]
#   szBjId        : BJ ID
#   nStationNo    : 방송국 ID (방송국에 여러 BJ 소속가능)
#   nBbsNo        : 게시판 ID (방송국 홈피에 여러 게시판 존재)
#   nTItleNo      : 게시글(또는 동영상) ID
#   nBroadNo      : 생방송 ID

import urllib
import time
import simplejson
import re
from BeautifulSoup import BeautifulSoup

root_url = "http://www.afreeca.com"
UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.9"

# http://www.afreeca.com/script/main/afreeca.front.main.js
def getTopBroadcast():
    ts_now = time.time() * 1000
    result = []
    result.append({'title':u"실시간 인기방송", 'data':getVideoList(root_url+"/data/main/main_top_broad_list.json?%d" %ts_now)})
    result.append({'title':u"보라 인기방송",   'data':getVideoList(root_url+"/data/main/main_top_bora_broad_list.json?%d" %ts_now, dataitem_name='M_DATA')})
    #result += getEsportsVideo('broadcast')
    return result

def getTopClips():
    result = []
    result.append({'title':u"추천 영상클립", 'data':getVideoList(root_url+"/m.afreeca.com/json/app_main_hot_vod.js")})
    result.append({'title':u"인기 영상클립", 'data':getVideoList(root_url+"/data/main/main_top_vod_list.json")})
    #result += getEsportsVideo('vod')
    return result

def getEsportsVideo(select='all'):
    ts_now = time.time() * 1000
    result = []
    for sect in getVideoList(root_url+"/data/main/main_sports_esports.json?%d" %ts_now):
    	if select=='all' or select=='broadcast':
            result.append({'title':u"e스포츠 인기방송", 'data':sect['BROAD_INFO']})
    	if select=='all' or select=='vod':
            result.append({'title':u"e스포츠 영상클립", 'data':sect['VOD_INFO']})
    return result

def getVideoList(url, dataitem_name='DATA'):
    print url
    jstr = urllib.urlopen(url).read().decode('euc-kr')
    json = simplejson.loads(jstr)
    return json[dataitem_name]
    #return [{'title':item['broad_title'], 'user_id':item['user_id'], } for item in json[dataitem_name]]

# 실시간 시청인원 급상승 방송
def getRapidGrowingBroadcast():
    url = "http://live.afreeca.com:8057/pg_gen/broad_list_rank_js.php"
    html = urllib.urlopen(url).read().decode('euc-kr')
    jstr = re.search('var oBroadListViewRank = ({.*?});', html).group(1)
    ptn_item = re.compile('"([^"]*)"\s*:\s*"([^"]*)"')
    items = []
    for sect in re.compile('({[^{}]*})').findall(jstr):
        info = dict()
        for key, val in ptn_item.findall(sect):
            if key == 'bj_id':
                info['user_id'] = val
            if key == 'bj_nick':
                info['user_nick'] = val
            if key == 'broad_title':
                info['broad_title'] = val.replace('\[','[').replace('\]',']')
            if key == 'broad_no':
                info['broad_no'] = val
            if key == 'thumb':
                info['thumb'] = val
        items.append(info)
    return items

# 이슈 생방송
def getIssueBroadcast(showmore=False):
    ts_now = time.time() * 1000
    url = root_url+"/data/main/main_live_banner_list.json?%d" %ts_now
    jstr = urllib.urlopen(url).read().decode('euc-kr')
    json = simplejson.loads(jstr)
    items = []
    for item in json['DATA']['aBannerInfo']:
        items += json['DATA']['aBannerInfo'][item]
    if showmore:
        for item in json['DATA']['aBroadInfo']:
            items += json['DATA']['aBroadInfo'][item]
    return items

def getBestBj():
    url = root_url+"/data/main/main_best_bj.json"
    jstr = urllib.urlopen(url).read().decode('euc-kr')
    json = simplejson.loads(jstr)
    return json['DATA']

def getBjRanking():
    ts_now = time.time() * 1000
    url = root_url+"/data/main/bj_ranking.json"
    jstr = urllib.urlopen(url).read().decode('euc-kr')
    json = simplejson.loads(jstr)
    return json['DATA']

# parse BJ랭킹
# parse 스타BJ

# 결국 '게임 인기방송'을 game_no 로 필터링
def getGameRanking():
    ts_now = time.time() * 1000
    return getVideoList(root_url+"/data/main/game_ranking.json?%d" %ts_now)

def getGameBroadcast(cateNo=''):
    ts_now = time.time() * 1000
    url = root_url+"/data/main/main_top_game_broad_list.json?%d" %ts_now
    for sec in getVideoList(url):
        if not cateNo or sec['cate_no'] == cateNo:
            return sec['list']
    return None

def extractBroadUrl(uid, bid):
    url = "http://live.afreeca.com:8057/afreeca/newafreeca/index.php?szBjId="+uid+"&nBroadNo="+bid
    html = urllib.urlopen(url).read()
    xap_url = re.search('var xapUrl = "(http.*?)";',html).group(1)
    # Current XBMC does not support Silverlight(XAP)
    return None

# http://www.afreeca.com/script/search/afreeca.front.search.js
def searchBroadById(uId):
    ts_now = time.time() * 1000
    keywd = ','.join(uId.split(' '))
    url = "http://affind.afreeca.com:8057/afreeca/search_api.php?szCallback=?&szType=json&szPageType=new&szOrder=rank&szKeyword=%s&nPageNo=1&nListCnt=10&%d" %(uId, ts_now)
    import urllib2
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    req.add_header('Referer', "http://www.afreeca.com/total_search.html")
    req.add_header('Accept', 'text/html')
    jstr = urllib2.urlopen(req).read()[2:-1]
    btbl = dict()
    for broad_no, user_id in re.compile("'broad_no':'(\d+)',[^}]*'user_id':'([^']*)'").findall(jstr):
        if user_id in btbl:
            btbl[user_id].append(broad_no)
        else:
            btbl[user_id] = [broad_no]
    return btbl
    json = simplejson.loads(jstr)
    for item in json['REAL_BROAD']:
        user_id = item['user_id']
        if user_id in btbl:
            btbl[user_id].append( item['broad_no'] )
        else:
            btbl[user_id] = [ item['broad_no'] ]
    return btbl

def searchBjById(uId):
    url = "http://bjsearch.afreeca.com:8102/api/bj_search_api.php?szCallback=?&szType=json&szOrder=ranking&szKeyword=%s&nPageNo=1&nListCnt=10" %uId
    jstr = urllib.urlopen(url).read()
    json = simplejson.loads(jstr[2:-1])
    return None

if __name__ == "__main__":
    #print getTopBroadcast()
    #print getTopClips()
    print getEsportsVideo()
    #print getIssueBroadcast()
    #print getRapidGrowingBroadcast()
    #print getBestBj()
    #print getBjRanking()
    #print getGameRanking()
    #print getGameBroadcast()
    #print searchBroadById('sehee3235')

# vim:sw=4:sts=4:et
