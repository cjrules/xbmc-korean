# -*- coding: utf-8 -*-
"""
    GomTV
"""
import urllib, re
import xbmcaddon,xbmcplugin,xbmcgui

__addonid__ = "plugin.video.gomtv.com"
__addon__   = xbmcaddon.Addon(__addonid__)
_L = __addon__.getLocalizedString

import os.path
LIB_DIR = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

plistDir = __addon__.getSetting('plistDir').lower() == 'true'
tNextPage = u"[B]%s>[/B]" % _L(30100)
tPrevPage = u"[B]<%s[/B]" % _L(30101)

root_url   = "http://www.gomtv.com"
chroot_url = "http://ch.gomtv.com"

def CATEGORIES():
    addDir(u"영화","http://movie.gomtv.com",20,"")
    addDir(u"뮤직",root_url+"/chart/index.gom",10,"")
    addDir(u"채널",root_url+"/allchannel.gom",1,"")
    endDir()

def GOM_CH(main_url):
    from gomtv_site import gomtv_site
    site = gomtv_site()
    for item in site.parseChList(main_url):
    	if item['url']:
            addDir(item['name'], item['url'], 2, item['thumb'])
        else:
            addDir(u"[COLOR FFFF0000]%s[/COLOR]"% item['name'],"-",0,"")
    endDir()

def GOM_CH_SUB(main_url):
    from gomtv_site import gomtv_site
    site = gomtv_site()
    for item in site.parseChPage(main_url):
    	if item['url']:
            addDir(item['name'], item['url'], 3, item['thumb'])
        else:
            addDir(u"[COLOR FF0000FF]%s[/COLOR]"% item['name'],"-",0,"")
    endDir()

def listProg(main_url):
    from gomtv_site import gomtv_site
    site = gomtv_site()
    for item in site.parseSubChPage(main_url):
        addDir(item['name'], item['url'], 5, item['thumb'])
    if site.prevpage:
        addDir(tPrevPage, site.prevpage, 4, '')
    if site.nextpage:
        addDir(tNextPage, site.nextpage, 4, '')

def GOM_CONTENTS(main_url):
    listProg(main_url)
    endDir()

def GOM_CONTENTS_MORE(main_url):
    listProg(main_url)
    endDir(True)

def playVideo(main_url, main_title):
    html = urllib.urlopen(main_url).read()
    contentsid, seriesid = re.compile("contentsid:'(\d*)',seriesid:'(\d*)'").search(html).group(1,2)
    referer = "http://m.gomtv.com/view.gom?contentsid=" + contentsid

    import gomm
    info = gomm.parseProg(referer)
    if info is None:
        xbmcgui.Dialog().ok(_L(30010), _L(30011))
        return
    if len(info['link']) == 0:
        import gomtv
        nidlist = gomtv.getNodeIds( int(info['contentsid']), int(info['seriesid']) )
        setnum = 0
        for nid in nidlist:
            info['link'].append( {
                'title':info['titles'][setnum],
                'url':info['video_base']+gomm.getRequestQuery(info['contentsid'],info['seriesid'],nid)
                } )
            setnum += 1

    if len(info['link']) == 1:
        url = info['link'][0]['url'] + "|Referer="+main_url
        li = xbmcgui.ListItem(main_title, iconImage="DefaultVideo.png")
        li.setInfo('video', {"Title": main_title})
        xbmc.Player().play(url, li)
    elif plistDir:
        for item in info['link']:
            url = item['url'] + "|Referer="+main_url
            addLink(item['title'], url, "")
        endDir()
    else:
        pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        pl.clear()
        for item in info['link']:
            li = xbmcgui.ListItem(item['title'], iconImage="DefaultVideo.png")
            li.setInfo( 'video', { "Title": item['title'] } )
            pl.add(item['url']+"|Referer="+main_url, li)
        xbmc.Player().play(pl)

#-----------------------------------                
# Music & Most Watched Chart
def CAT_MUSIC_CHART(main_url):
    addDir(u"실시간", main_url+"?chart=1", 11,"")
    addDir(u"주간", main_url+"?chart=3", 11,"")
    addDir(u"월간", main_url+"?chart=4", 11,"")
    addDir(u"주간1위모음", main_url+"?chart=6", 11,"")
    addDir(u"명예의전당", main_url+"?chart=5", 11,"")
    endDir()

def listMusic(main_url):
    from gomtv_site import gomtv_site
    site = gomtv_site()
    for item in site.parseMusicChartPage(main_url):
        addDir(item['name'], item['url'], 5, item['thumb'])
    if site.prevpage:
        addDir(tPrevPage, site.prevpage, 12, '')
    if site.nextpage:
        addDir(tNextPage, site.nextpage, 12, '')

def MUSIC_CHART(main_url):
    listMusic(main_url)
    endDir()
    
def MUSIC_CHART_MORE(main_url):
    listMusic(main_url)
    endDir(True)

def CAT_MOVIE(main_url):
    addDir(u"무료영화",main_url+"/list.gom?cateid=4",21,'')
    endDir()

def listMovie(main_url):
    from gomtv_movie_site import gommovie_site 
    site = gommovie_site()
    for item in site.parseMovieChartPage(url):
        addDir(item['name'], item['url'], 5, item['thumb'])
    if site.prevpage:
        addDir(tPrevPage, site.prevpage, 22, '')
    if site.nextpage:
        addDir(tNextPage, site.nextpage, 22, '')

def MOVIE_CHART(main_url):
    listMovie(main_url)
    endDir()
    
def MOVIE_CHART_MORE(main_url):
    listMovie(main_url)
    endDir(True)
    
"""
def CAT_HOT(url):
    for item in gomtv_site().parseHotListPage( "http://www.gomtv.com/navigation/navigation.gom?navitype=3" ):
        addDir(item['name'], item['url'], 14, item['thumb'])

def CAT_HOT_SUB(main_url):
    for item in gomtv_site().parseHotSubListPage(url):
        addDir(item['name'], item['url'], 3, item['thumb'])

def MOST_WATCHED(main_url):
    site = gomtv_site()
    for item in site.parseMostWatchedPage(url):
        addDir(item['name'], item['url'], 10, item['thumb'])
    if site.nextpage:
        addDir(title_nextpage, site.nextpage, 2, '')

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

    from gomtv_movie_site import gommovie_site 
    site = gommovie_site()
    for item in site.parseMovieChartPage(url):
        addDir(item['name'], item['url'], child_fid, item['thumb'])
    if site.nextpage:
        addDir(title_nextpage, site.nextpage, 102, '')
  
def PREMIER_LIST(url):
    from gomtv_movie_site import gommovie_site 
    site = gommovie_site()
    for item in site.parsePremierPage(url):
        addDir(item['name'], item['url'], 110, item['thumb'])
    if site.nextpage:
        addDir(title_nextpage, site.nextpage, 107, '')
  
def MOVIE_HOTCLIP(main_url):
    from gomtv_movie_site import gommovie_site 
    site = gommovie_site()
    for item in site.parseHotClipPage(url):
        addDir(item['name'], item['url'], 110, item['thumb'])
    if site.nextpage:
        addDir(title_nextpage, site.nextpage, 101, '')

def MOVIE_BOXOFFICE(main_url):
    from gomtv_movie_site import gommovie_site 
    site = gommovie_site()
    for item in site.parseBoxOfficePage(url):
        addDir(item['name'], item['url'], 110, item['thumb'])
    if site.nextpage:
        addDir(title_nextpage, site.nextpage, 103, '')

def GOM_MOVIE(main_url):
    print "MOVIE %s" % main_url
    # free movie
    if __settings__.getSetting('MovieBackdoor')=='true':
        import re
        match = re.compile('http://movie.gomtv.com/(\d+)/(\d+)').match(main_url)
        vinfo = {'dispid':match.group(1), 'vodid':match.group(2)}
    else:
        from gomtv_movie_site import gommovie_site
        site = gommovie_site()
        vinfo = site.parseMoviePage(main_url)
    from gommovie_downloader import gommovie_downloader
    downloader = gommovie_downloader()
    mov_list = downloader.getMovieUrls(vinfo)
    for title,url in mov_list:
        addLink(title, url, '')
    # hotclip
    if vinfo.has_key('misid'):
        hotclip_url = "http://movie.gomtv.com/sub/detailAjax.gom?misid=%s&dispid=%s&vodid=%s&mtype=5" % \
                                (vinfo['misid'], vinfo['dispid'], vinfo['vodid'])
        hc_ids = site.parseMovieHotClipPage( hotclip_url )
        if mov_list and hc_ids:
            addDir(menu_div, '', 110, '')  # divider
        for info in hc_ids:
            url = "http://tv.gomtv.com/cgi-bin/gox/gox_clip.cgi?dispid=%s&clipid=%s" % (vinfo['dispid'],info['clipid'])
            addLink(info['name'], url, info['thumb'])
"""

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
                
def endDir(update=False):
    xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=update)
                
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
elif mode==1:
    GOM_CH(url)
elif mode==2:
    GOM_CH_SUB(url)
elif mode==3:
    GOM_CONTENTS(url)
elif mode==4:
    GOM_CONTENTS_MORE(url)
elif mode==5:
    playVideo(url, name)
elif mode==10:
    CAT_MUSIC_CHART(url)
elif mode==11:
    MUSIC_CHART(url)
elif mode==12:
    MUSIC_CHART_MORE(url)
elif mode==20:
    CAT_MOVIE(url)
elif mode==21:
    MOVIE_CHART(url)
elif mode==22:
    MOVIE_CHART_MORE(url)

# vim: softtabstop=4 shiftwidth=4 expandtab
