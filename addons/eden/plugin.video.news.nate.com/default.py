# -*- coding: utf-8 -*-
"""
    Nate Sports News
"""
import urllib
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.sports.nate.com"
__addon__   = xbmcaddon.Addon(__addonid__)
_L = __addon__.getLocalizedString

import os.path
LIB_DIR = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

import nate_sports
selAltMovie = __addon__.getSetting("selAltMovie").lower() == "true"

tPrevPage = u"[B]<%s[/B]" % _L(30100)
tNextPage = u"[B]%s>[/B]" % _L(30101)

root_url = "http://sports.news.nate.com"

def categoryList():
    #addDir(u"eSports", root_url+"/esports/vod", 1, "")
    main_url = root_url+"/esports/vod"
    addDir(u"SK플래닛 SC프로리그", main_url+"?sec=esports", 2, "")
    addDir(u"4G LTE SF2프로리그", main_url+"?sec=esports_sf", 2, "")
    addDir(u"티빙 스타리그", main_url+"?sec=esports_tv", 2, "")
    endDir()

def sortedESportsList(main_url):
    for srt in nate_sports.parseSortList(main_url):
    	if srt['url'].find("vt=team") > 0:
            addDir(srt['name'], srt['url'], 3, "")
        else:
            addDir(srt['name'], srt['url'], 4, "")
    endDir()

def teamList(main_url):
    for team in nate_sports.parseTeamList(main_url):
        addDir(team['name'], team['url'], 4, "")
    endDir()

def _programList(main_url):
    info = nate_sports.parseESports(main_url)
    for sec in info['group']:
    	if 'title' in sec:
            title = u"[COLOR FF0000FF]"+sec['title']+"[/COLOR]"
            addDir(title, "-", 0, "")
        for item in sec['list']:
            url = root_url + "/view/" + item['aid']
            addDir(item['title'], url, 6, "")
    if "prevpage" in info:
        addDir(tPrevPage, info['prevpage'], 5, "")
    if "nextpage" in info:
        addDir(tNextPage, info['nextpage'], 5, "")

def programList(main_url):
    _programList(main_url)
    endDir()

def programListNext(main_url):
    _programList(main_url)
    endDir(True)

def videoList(main_url,main_title):
    try:
        vod_sq,vod_key = nate_sports.parseProg2(main_url)
    except:
        vod_sq,vod_key = nate_sports.parseProg(main_url)
    xbmc.log(vod_sq + " " + vod_key, xbmc.LOGDEBUG)
    vid_url,img_url = nate_sports.getVideoUrl(vod_sq,vod_key,selAltMovie)
    url = vid_url + "|Referer="+main_url
    li = xbmcgui.ListItem(main_title, iconImage=img_url)
    li.setInfo('video', {"Title": main_title})
    xbmc.Player().play(url, li)

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
    categoryList()
elif mode==1:
    sectionList(url)
elif mode==2:
    sortedESportsList(url)
elif mode==3:
    teamList(url)
elif mode==4:
    programList(url)
elif mode==5:
    programListNext(url)
elif mode==6:
    videoList(url,name)

# vim:sts=4:et
