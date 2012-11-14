# -*- coding: utf-8 -*-
"""
    OhMyNews School 
"""
import urllib
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.school.ohmynews.com"
__addon__   = xbmcaddon.Addon(__addonid__)

import os.path
LIB_DIR = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

import ohmynews

root_url = "http://school.ohmynews.com"

def programList():
    for title, url, thumb in ohmynews.parseTop(root_url+"/NWS_Web/School/online_search.aspx"):
        addDir(title, url, 1, thumb)
    endDir()

def lectureList(main_url):
    for title, url in ohmynews.parseLecture(main_url):
        addDir(title, url, 2, "")
    endDir()

def videoPlay(main_url,main_title):
    info = ohmynews.parseVideo(main_url)
    url = "%s app=%s swfUrl=%s pageUrl=%s playpath=%s" % (info['tcUrl'], info['app'], info['swfUrl'], info['pageUrl'], info['playpath'])
    li = xbmcgui.ListItem(main_title, iconImage="DefaultVideo.png")
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
    programList()
elif mode==1:
    lectureList(url)
elif mode==2:
    videoPlay(url,name)

# vim:sts=4:et
