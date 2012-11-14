# -*- coding: utf-8 -*-
"""
    tving Air
"""

import urllib, urllib2
import simplejson
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.tving.com"
__addon__   = xbmcaddon.Addon(__addonid__)
_L = __addon__.getLocalizedString

tPrevPage = u"[B]<%s[/B]" % _L(30100)
tNextPage = u"[B]%s>[/B]" % _L(30101)
itemPerPage = 15
MobileAgent = "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) Mobile"

root_url = "http://www.tving.com"
api_root = "http://air.tving.com"
img_root = "http://image.tving.com"

def doTopList():
    addDir(u"무료", "free", 1, "")
    addDir(u"무료영화", "10", 11, "")
    #addDir(u"무료성인영화", "3", 13, "")
    endDir()

def doChList(cate_cd):
    url = root_url + "/vod/categoryAllChListA.do"
    values = {
    	"key"    :"CATE_CH00",
    	"deploy" :"0",
    	"cache"  :"N",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/vod/genre.do?cate_cd="+cate_cd)
    resp = urllib2.urlopen(req, urllib.urlencode(values))
    jstr = resp.read()
    resp.close()
    json = simplejson.loads(jstr)

    cate_tpl = u"[COLOR FFFF0000]%s[/COLOR]"
    addDir(u"[B]전체[/B]", cate_cd+"|", 3, "")
    for item in json['RESULT_DATA']:
    	#url = '|'.join([item['CATE_CD'], item['CH_CD']])
    	url = '|'.join([cate_cd, item['CH_CD']])
    	if len(item['CH_CD']) == 2:
            name = cate_tpl% item['CH_NM']
    	else:
            name = item['CH_NM']
        addDir(name, url, 3, "")
    endDir()

def _doProgList(main_url, skip_num):
    cate_cd, ch_cd = main_url.split('|')
    start_num = skip_num+1
    end_num = skip_num+itemPerPage

    url = root_url + "/vod/vodListA.do"
    values = {
    	"key"    :"vodList",
    	"cate_cd":cate_cd,
    	"ch_cd"  :ch_cd,
    	"sort_type":"NEW",
    	"start_num":start_num,
    	"end_num":end_num,
    	"payfree_yn":"",
    	"initial_keyword":"",
    	"adult_yn":"Y",
    	"deploy" :"0",
    	"cache"  :"N",
    	"package_id":"",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/vod/genre.do?cate_cd=free")
    resp = urllib2.urlopen(req, urllib.urlencode(values))
    jstr = resp.read()
    resp.close()
    json = simplejson.loads(jstr)

    for item in json['RESULT_DATA']['RESULT_DATA']:
        #addDir(item['PGM_NM'], item['DRM_VOD_FILE_CD'], 100, img_root+item['IMG_URL'])
        addDir(item['PGM_NM'], str(item['PGM_CD']), 5, img_root+item['IMG_URL'])
    if skip_num >= itemPerPage:
        new_skip_num = skip_num-itemPerPage;
        addDir(tPrevPage, main_url, 4, "", skip_num=new_skip_num)
    #print json['RESULT_DATA']['RESULT_COUNT']
    if len(json['RESULT_DATA']['RESULT_DATA']) == itemPerPage:
        new_skip_num = skip_num+itemPerPage
        addDir(tNextPage, main_url, 4, "", skip_num=new_skip_num)

def doProgList(url):
    _doProgList(url, 0)
    endDir()

def doProgListMore(url, skip_num):
    _doProgList(url, skip_num)
    endDir(True)

def _doEpisodeListAir(main_url, skip_num):
    pgm_cd = main_url
    url = api_root+"/TvingAir/api/facebook/episodeList/"+pgm_cd+"/%d/%d?out=jsonp" % (skip_num, itemPerPage)
    jstr = urllib.urlopen(url).read()
    json = simplejson.loads(jstr)

    for item in json['list']:
        title = u"%s [%s]" % (item['title'], str(item['broadDt']))
        if item['price'] != 0:
            title = "[I]"+title+"[/I]"
        addDir(title, item['drmCode'], 100, item['thumbnail'])
    if skip_num >= itemPerPage:
        new_skip_num = skip_num-itemPerPage;
        addDir(tPrevPage, main_url, 6, "", skip_num=new_skip_num)
    if len(json['list']) >= itemPerPage:
        new_skip_num = skip_num+itemPerPage;
        addDir(tNextPage, main_url, 6, "", skip_num=new_skip_num)

def doEpisodeList(url):
    _doEpisodeListAir(url, 0)
    endDir()

def doEpisodeListMore(url, skip_num):
    _doEpisodeListAir(url, skip_num)
    endDir(True)

def playVideo(file_cd):
    # vodInfo/[TYPE]/[DRM_VOD_FILE_CD]/[PROTOCOL]?out=jsonp
    #   TYPE: clip / vod
    #   PROTOCOL: HLS / RTSP / HTTP
    url = api_root+"/TvingAir/api/facebook/vodInfo/clip/"+file_cd+"/HLS?out=jsonp"
    req = urllib2.Request(url)
    req.add_header('User-Agent', MobileAgent)
    jstr = urllib2.urlopen(req).read()
    json = simplejson.loads(jstr)
    info = json['info']

    if info['broadURL'] is None:
        xbmcgui.Dialog().ok(_L(30010), _L(30011))
        return
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo('video', {"Title": info['title']})
    xbmc.Player().play(info['broadURL'], li)

#-----------------------------------                
def _doFreeMovieListAir(main_url, skip_num):
    vodtype = '0233'    # PC
    url = api_root+"/TvingAir/api/movie/freeList/"+vodtype+"/new/%d/%d?out=jsonp" % (skip_num, itemPerPage)
    jstr = urllib.urlopen(url).read()
    json = simplejson.loads(jstr)

    for item in json['movie']:
        addDir(item['title'], item['clipCode'], 100, item['thumbnail'])
    if skip_num >= itemPerPage:
        new_skip_num = skip_num-itemPerPage;
        addDir(tPrevPage, main_url, 12, "", skip_num=new_skip_num)
    if len(json['movie']) >= itemPerPage:
        new_skip_num = skip_num+itemPerPage;
        addDir(tNextPage, main_url, 12, "", skip_num=new_skip_num)

def _doFreeMovieList(main_url, pg_num):
    cate_cd = main_url
    url = root_url + "/sm/ms/SMMS401A.do"
    values = {
    	"CATE_CD":cate_cd,
    	"sortType":"NEW",
    	"pageNo":pg_num,
    	"grade":"ALL",
    	"runtime":"ALL",
    	"year":"ALL",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/sm/ms/SMMS401Q.do?CATE_CD="+str(cate_cd))
    resp = urllib2.urlopen(req, urllib.urlencode(values))
    jstr = resp.read()
    resp.close()
    json = simplejson.loads(jstr)

    for item in json['data']:
        #print item['DRM_VOD_FILE_CD'] + " / " + item['VOD_FILE_CD']
        addDir(item['MAST_NM'], item['DRM_VOD_FILE_CD'], 100, img_root+item['POSTER_IMG_URL'])
    if pg_num > 1:
        new_skip_num = pg_num-1
        addDir(tPrevPage, main_url, 12, "", skip_num=new_skip_num)
    new_skip_num = pg_num+1
    addDir(tNextPage, main_url, 12, "", skip_num=new_skip_num)

def doFreeMovieList(url):
    #_doFreeMovieList(url, 1)
    _doFreeMovieListAir(url, 0)
    endDir()

def doFreeMovieListMore(url, skip_num):
    #_doFreeMovieList(url, skip_num)
    _doFreeMovieListAir(url, skip_num)
    endDir(True)

#-----------------------------------                
def _doAdultMovieList(main_url, pg_num):
    scptype = main_url
    url = root_url + "/sm/ms/SMMS800A.do"
    values = {
    	"scptype":scptype,
    	"PAYFREE_YN":"Y",
    	"CATE_CD":"ALL",
    	"sortType":"NEW",
    	"pageNo":pg_num,
    	"grade":"ALL",
    	"runtime":"ALL",
    	"year":"ALL",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/sm/ms/SMMS800Q.do?scptype="+str(scptype))
    resp = urllib2.urlopen(req, urllib.urlencode(values))
    jstr = resp.read()
    resp.close()
    json = simplejson.loads(jstr)

    for item in json['data']:
        addDir(item['MAST_NM'], item['DRM_VOD_FILE_CD'], 100, img_root+item['POSTER_IMG_URL'])
    if pg_num > 1:
        new_skip_num = pg_num-1
        addDir(tPrevPage, main_url, 14, "", skip_num=new_skip_num)
    new_skip_num = pg_num+1
    addDir(tNextPage, main_url, 14, "", skip_num=new_skip_num)

def doAdultMovieList(url):
    _doAdultMovieList(url, 1)
    endDir()

def doAdultMovieListMore(url, pg_num):
    _doAdultMovieList(url, pg_num)
    endDir(True)

#-----------------------------------                
def get_params():
    param=[]
    paramstring=sys.argv[2]
    xbmc.log( "get_params() %s" % paramstring, xbmc.LOGDEBUG )
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                        
    return param

def addLink(name,url,iconimage):
    ok=True
    name=name.encode("utf-8")
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage,skip_num=0):
    name=name.encode("utf-8")
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    u+="&skip_num="+str(skip_num)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    xbmc.log( "addDir(%s)" % u, xbmc.LOGDEBUG )
    return ok

def endDir(update=False):
    xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=update)
                
#-----------------------------------                
params=get_params()
url=None
name=None
mode=None
skip_num=0

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: skip_num=int(params["skip_num"])
except: pass

if mode==None or url==None or len(url)<1:
    doTopList()
elif mode==1:
    doChList("free")
elif mode==3:
    doProgList(url)
elif mode==4:
    doProgListMore(url, skip_num)
elif mode==5:
    doEpisodeList(url)
elif mode==6:
    doEpisodeListMore(url, skip_num)
elif mode==11:
    doFreeMovieList(url)
elif mode==12:
    doFreeMovieListMore(url, skip_num)
elif mode==13:
    doAdultMovieList(url)
elif mode==14:
    doAdultMovieListMore(url)
elif mode==100:
    playVideo(url)

# vim:sts=4:et
