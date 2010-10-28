# -*- coding: utf-8 -*-
"""
    GomTV - Music Video
"""

import urllib
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__plugin__ = "GomTV Mobile"
__addonID__ = "plugin.video.gomtv.com"
__url__ = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/addons/plugin.video.m.gomtv.com"
__credits__ = "XBMC Korean User Group"
__version__ = "0.7.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)

__settings__ = xbmcaddon.Addon(id=__addonID__)
getLS = __settings__.getLocalizedString

menu_div = u"----------------------------------------------------"
title_nextpage = u"%s>" % getLS(30100)
title_prevpage = u"<%s" % getLS(30101)

import xml.dom.minidom as xml
user_chcfg = xbmc.translatePath( 'special://masterprofile/gomtv.xml' )
if os.path.isfile(user_chcfg):
    chset = xml.parse( user_chcfg )
else:
    chset = xml.parse( os.path.join( os.getcwd(), 'resources', 'gomtv.xml' ) )

from gomtv_scraper import gomtv_scraper

#-----------------------------------------------------
# Channel
def CATEGORIES():
    addDir(u"시청순위","-",13,"")
    addDir(u"영화/드라마","-",106,"")
    addDir(u"뮤직","-",15,"")
    addDir(u"게임","-",12,"")
    addDir(u"연예/오락","-",16,"")
    addDir(u"뉴스/정보","-",17,"")
    #addDir(u"생중계","http://live.gomtv.com",200,"")

def CAT_MUSIC_CHART(main_url):
    mchart_url = "http://www.gomtv.com/chart/index.gom?chart=%d"
    addDir(u"실시간",mchart_url % 1,4,"")
    addDir(u"주간",mchart_url % 3,4,"")
    addDir(u"월간",mchart_url % 4,4,"")
    addDir(u"주간1위모음",mchart_url % 6,4,"")
    addDir(u"명예의전당",mchart_url % 5,4,"")

def CAT_GAME(main_url):
    thisch = chset.getElementsByTagName('game')[0]
    shortcuts = thisch.getElementsByTagName('shortcut')
    for subch in shortcuts:
        name = subch.getElementsByTagName('name')[0].childNodes[0].data
        number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    if shortcuts:
        addDir(menu_div,"",12,"")
    for ch in thisch.getElementsByTagName('channel'):
        name = ch.getElementsByTagName('name')[0].childNodes[0].data
        number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

def CAT_MUSIC(main_url):
    addDir(u"뮤직비디오 차트","-",11,"")
    thisch = chset.getElementsByTagName('music')[0]
    for subch in thisch.getElementsByTagName('shortcut'):
        name = subch.getElementsByTagName('name')[0].childNodes[0].data
        number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    addDir(menu_div,"",15,"")
    for ch in thisch.getElementsByTagName('channel'):
        name = ch.getElementsByTagName('name')[0].childNodes[0].data
        number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

def CAT_ETMNT(main_url):
    thisch = chset.getElementsByTagName('entertainment')[0]
    shortcuts = thisch.getElementsByTagName('shortcut')
    for subch in shortcuts:
        name = subch.getElementsByTagName('name')[0].childNodes[0].data
        number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    if shortcuts:
        addDir(menu_div,"",16,"")
    for ch in thisch.getElementsByTagName('channel'):
        name = ch.getElementsByTagName('name')[0].childNodes[0].data
        number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

def CAT_INFO(main_url):
    thisch = chset.getElementsByTagName('information')[0]
    shortcuts = thisch.getElementsByTagName('shortcut')
    for subch in shortcuts:
        name = subch.getElementsByTagName('name')[0].childNodes[0].data
        number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    if shortcuts:
        addDir(menu_div,"",17,"")
    for ch in thisch.getElementsByTagName('channel'):
        name = ch.getElementsByTagName('name')[0].childNodes[0].data
        number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

def GOM_CH(url):
    for item in gomtv_scraper().parseChPage(url):
        addDir(item['name'], item['url'], 2, item['thumb'])

def GOM_CH_SUB(url):
    scraper = gomtv_scraper()
    for item in scraper.parseSubChPage(url):
        addDir(item['name'], item['url'], 10, item['thumb'])
    if scraper.nextpage:
        addDir(title_nextpage, scraper.nextpage, 2, '')

def GOM_PROGRAM(url):
    print "PROGRAM %s" % url
    if __settings__.getSetting('fromMobile') == 'false':
        hq = __settings__.getSetting('HQVideo') == 'true'
        scraper = gomtv_scraper(hq)
        from gomtv_downloader import gomtv_downloader
        downloader = gomtv_downloader()
    else:
        from gomm_scraper import gomm_scraper
        scraper = gomm_scraper()
        from gomm_downloader import gomm_downloader
        downloader = gomm_downloader()
    for vidinfo in scraper.parseProgramPage(url):
        vidurl = downloader.getPlayUrl( vidinfo )
        addLink(vidinfo['title'], vidurl+"|Referer="+downloader.referer, '')

#-----------------------------------                
# Music & Most Watched Chart
def MUSIC_CHART(url):
    scraper = gomtv_scraper()
    for item in scraper.parseMusicChartPage(url):
        addDir(item['name'], item['url'], 10, item['thumb'])
    if scraper.nextpage:
        addDir(title_nextpage, scraper.nextpage, 2, '')
    
def CAT_HOT(url):
    for item in gomtv_scraper().parseHotListPage( "http://www.gomtv.com/navigation/navigation.gom?navitype=3" ):
        addDir(item['name'], item['url'], 14, item['thumb'])

def CAT_HOT_SUB(main_url):
    for item in gomtv_scraper().parseHotSubListPage(url):
        addDir(item['name'], item['url'], 3, item['thumb'])

def MOST_WATCHED(main_url):
    scraper = gomtv_scraper()
    for item in scraper.parseMostWatchedPage(url):
        addDir(item['name'], item['url'], 10, item['thumb'])
    if scraper.nextpage:
        addDir(title_nextpage, scraper.nextpage, 2, '')

#-----------------------------------                
# Movie Chart
def CAT_PREMIER_LIST(main_url):
    mvlist_url = "http://movie.gomtv.com/list.gom?cateid=%d"
    addDir(u"현재 상영작",mvlist_url % 65,107,'')
    addDir(u"개봉 예정작",mvlist_url % 66,107,'')
    addDir(u"개봉 미정작",mvlist_url % 67,107,'')

def CAT_MOVIE_HOTCLIP(main_url):
    hot_url = "http://movie.gomtv.com/release/hotclip.gom"
    addDir(u"전체보기",hot_url,101,'')
    addDir(u"본예고",hot_url+"?flag=3000",101,'')
    addDir(u"티저예고",hot_url+"?flag=3500",101,'')
    addDir(u"메이킹",hot_url+"?flag=3100",101,'')
    addDir(u"M/V",hot_url+"?flag=3200",101,'')
    addDir(u"인터뷰",hot_url+"?flag=3600",101,'')

def CAT_MOVIE(main_url):
    addDir(u"무료영화","http://movie.gomtv.com/list.gom?cateid=4",102,'')
    #addDir(u"무료드라마","http://movie.gomtv.com/list.gom?cateid=189",102,'')
    addDir(u"에니메이션","http://movie.gomtv.com/list.gom?cateid=44",102,'')
    addDir(u"극장개봉정보","-",104,'')
    addDir(u"박스오피스","http://movie.gomtv.com/release/boxoffice.gom",103,'')
    addDir(u"핫클립","-",105,'')

    thisch = chset and chset.getElementsByTagName('movie')[0]
    for subch in thisch.getElementsByTagName('shortcut'):
        name = subch.getElementsByTagName('name')[0].childNodes[0].data
        number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://movie.gomtv.com/"+number,2,"")
    channels = thisch.getElementsByTagName('id')
    if channels:
        addDir(menu_div,'',18,'')
    for ch in channels:
        name = ch.getElementsByTagName('name')[0].childNodes[0].data
        number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name, "http://movie.gomtv.com/"+number, 110, '')

def MOVIE_LIST(url):
    if url.endswith("cateid=44") or url.endswith("cateid=189"):
        child_fid = 102  # sub table
    else:
        child_fid = 110  # movie page

    from gomtv_movie_scraper import gommovie_scraper 
    scraper = gommovie_scraper()
    for item in scraper.parseMovieChartPage(url):
        addDir(item['name'], item['url'], child_fid, item['thumb'])
    if scraper.nextpage:
        addDir(title_nextpage, scraper.nextpage, 102, '')
  
def PREMIER_LIST(url):
    from gomtv_movie_scraper import gommovie_scraper 
    scraper = gommovie_scraper()
    for item in scraper.parsePremierPage(url):
        addDir(item['name'], item['url'], 110, item['thumb'])
    if scraper.nextpage:
        addDir(title_nextpage, scraper.nextpage, 107, '')
  
def MOVIE_HOTCLIP(main_url):
    from gomtv_movie_scraper import gommovie_scraper 
    scraper = gommovie_scraper()
    for item in scraper.parseHotClipPage(url):
        addDir(item['name'], item['url'], 110, item['thumb'])
    if scraper.nextpage:
        addDir(title_nextpage, scraper.nextpage, 101, '')

def MOVIE_BOXOFFICE(main_url):
    from gomtv_movie_scraper import gommovie_scraper 
    scraper = gommovie_scraper()
    for item in scraper.parseBoxOfficePage(url):
        addDir(item['name'], item['url'], 110, item['thumb'])
    if scraper.nextpage:
        addDir(title_nextpage, scraper.nextpage, 103, '')

def GOM_MOVIE(main_url):
    print "MOVIE %s" % main_url
    # free movie
    if __settings__.getSetting('MovieBackdoor')=='true':
        import re
        match = re.compile('http://movie.gomtv.com/(\d+)/(\d+)').match(main_url)
        vinfo = {'dispid':match.group(1), 'vodid':match.group(2)}
    else:
        from gomtv_movie_scraper import gommovie_scraper
        scraper = gommovie_scraper()
        vinfo = scraper.parseMoviePage(main_url)
    from gommovie_downloader import gommovie_downloader
    downloader = gommovie_downloader()
    mov_list = downloader.getMovieUrls(vinfo)
    for title,url in mov_list:
        addLink(title, url, '')
    # hotclip
    if vinfo.has_key('misid'):
        hotclip_url = "http://movie.gomtv.com/sub/detailAjax.gom?misid=%s&dispid=%s&vodid=%s&mtype=5" % \
                                (vinfo['misid'], vinfo['dispid'], vinfo['vodid'])
        hc_ids = scraper.parseMovieHotClipPage( hotclip_url )
        if mov_list and hc_ids:
            addDir(menu_div, '', 110, '')  # divider
        for info in hc_ids:
            url = "http://tv.gomtv.com/cgi-bin/gox/gox_clip.cgi?dispid=%s&clipid=%s" % (vinfo['dispid'],info['clipid'])
            addLink(info['name'], url, info['thumb'])

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
    try: xbmc.log( "addLink(%s,%s)" % (name, url), xbmc.LOGDEBUG )
    except: pass
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
    name=name.encode("utf-8")
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    xbmc.log( "addDir(%s)" % u, xbmc.LOGDEBUG )
    return ok
                
#-----------------------------------                
params=get_params()
url=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

xbmc.log( "Mode: "+str(mode), xbmc.LOGINFO)
xbmc.log( "URL : "+str(url), xbmc.LOGINFO)
xbmc.log( "Name: "+str(name), xbmc.LOGINFO)

if mode==None or url==None or len(url)<1:
    CATEGORIES()
# Channel
elif mode==1:
    GOM_CH(url)
elif mode==2:
    GOM_CH_SUB(url)
elif mode==3:
    MOST_WATCHED(url)
elif mode==4:
    MUSIC_CHART(url)
elif mode==10:
    GOM_PROGRAM(url)
elif mode==11:
    CAT_MUSIC_CHART(url)
elif mode==12:
    CAT_GAME(url)
elif mode==13:
    CAT_HOT(url)
elif mode==14:
    CAT_HOT_SUB(url)
elif mode==15:
    CAT_MUSIC(url)
elif mode==16:
    CAT_ETMNT(url)
elif mode==17:
    CAT_INFO(url)
# Movie
elif mode==101:
    MOVIE_HOTCLIP(url)
elif mode==102:
    MOVIE_LIST(url)
elif mode==103:
    MOVIE_BOXOFFICE(url)
elif mode==104:
    CAT_PREMIER_LIST(url)
elif mode==105:
    CAT_MOVIE_HOTCLIP(url)
elif mode==106:
    CAT_MOVIE(url)
elif mode==107:
    PREMIER_LIST(url)
elif mode==110:
    GOM_MOVIE(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
# vim: softtabstop=4 shiftwidth=4 expandtab
