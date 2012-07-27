# -*- coding: utf-8 -*-
"""
    GomTV Mobile
"""

import urllib
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.m.gomtv.com"
__addon__   = xbmcaddon.Addon(__addonid__)
_L = __addon__.getLocalizedString

import os.path
LIB_DIR = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

plistDir = __addon__.getSetting('plistDir').lower() == 'true'

import gomm, gomtv

def categoryList():
    info = gomm.parseList("http://m.gomtv.com")
    for item in info['tab']:
        addDir(item['title'], item['url'], 1, "")
    endDir()

def sectionList(main_url):
    info = gomm.parseList(main_url)
    for item in info['subtab']:
        addDir(item['title'], item['url'], 2, "")
    endDir()

def _programList(main_url):
    info = gomm.parseList(main_url)
    for item in info['list']:
        addDir(item['title'], item['url'], 4, item['thumb'])
    return len(info['list'])

def programList(main_url):
    llen = _programList(main_url+"&limit=25")
    if llen == 25:
        # double number of items per page
        tMore = u"[COLOR FF0000FF]%s[/COLOR]" % _L(30100)
        addDir(tMore, main_url+"&limit=50", 3, "")
    endDir()

def programListMore(main_url):
    llen = _programList(main_url)
    pos = main_url.rfind('=')+1
    limit = int(main_url[pos:])
    if llen == limit:
        # double number of items per page
        tMore = u"[COLOR FF0000FF]%s[/COLOR]" % _L(30100)
        addDir(tMore, main_url[:pos]+str(limit*2), 3, "")
    endDir(True)

def videoList(main_url):
    info = gomm.parseProg(main_url)
    if info is None:
    	xbmcgui.Dialog().ok(_L(30010), _L(30011))
    	return
    if len(info['link']):
    	if len(info['link']) == 1:
            title = info['link'][0]['title']
            url = info['link'][0]['url'] + "|Referer="+main_url
            li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
            li.setInfo('video', {"Title": title})
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
    else:
    	url = "http://ch.gomtv.com/%s/%s/%s" % (info['chnum'],info['id1s'],info['id2s'])
    	info2 = gomtv.parseProg(url)
    	if info2 is None:
            xbmcgui.Dialog().ok(_L(30010), _L(30011))
    	    return
    	if len(info2['playlist']) == 1:
            title = info2['playlist'][0]['title']
            url = info['video_base'] + gomm.getRequestQuery(info['contentsid'],info['seriesid'],info2['playlist'][0]['nodeid'])
            url += "|Referer="+main_url
            li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
            li.setInfo('video', {"Title": title})
            xbmc.Player().play(url, li)
        elif plistDir:
            for item in info2['playlist']:
                url = info['video_base'] + gomm.getRequestQuery(info['contentsid'],info['seriesid'],item['nodeid'])
                url += "|Referer="+main_url
                addLink(item['title'], url, "")
            endDir()
        else:
            pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
            pl.clear()
            for item in info2['playlist']:
                li = xbmcgui.ListItem(item['title'], iconImage="DefaultVideo.png")
                li.setInfo( 'video', { "Title": item['title'] } )
                url = info['video_base'] + gomm.getRequestQuery(info['contentsid'],info['seriesid'],item['nodeid'])
                pl.add(url+"|Referer="+main_url, li)
            xbmc.Player().play(pl)

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
    programList(url)
elif mode==3:
    programListMore(url)
elif mode==4:
    videoList(url)

# vim:sts=4:et
