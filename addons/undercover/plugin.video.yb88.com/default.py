# -*- coding: utf-8 -*-
"""
    yb88 - 영변88 TV
"""
import urllib,re
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.yb88.com"
__addon__ = xbmcaddon.Addon( __addonid__ )
_L = __addon__.getLocalizedString

import os.path
LIB_DIR = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

root_url = "http://tv.yb88.com"
import yb88tv

tPrevPage = u"[B]<%s[/B]" % _L(30100)
tNextPage = u"[B]%s>[/B]" % _L(30101)

#-----------------------------------------------------
def rootList():
    ## not parsing homepage for faster speed
    #addDir(u"텔레비젼",root_url+"/tv",1,"")
    addDir(u"드라마",root_url+"/tv/Drama",1,"")
    addDir(u"시사교양",root_url+"/tv/Preview-Hobbies",1,"")
    addDir(u"연예오락",root_url+"/tv/Entertainment",1,"")
    addDir(u"스포츠",root_url+"/tv/Sports",1,"")
    addDir(u"다큐멘터리",root_url+"/tv/documentary",1,"")
    addDir(u"영화",root_url+"/movie",1,"")
    addDir(u"뮤직비디오",root_url+"/music-video",1,"")
    endDir()

def _progList(main_url):
    info = yb88tv.parseList(main_url)
    for item in info['link']:
        addDir(item['title'], item['url'], 3, item['thumb'])
    if 'prevpage' in info:
        addDir(tPrevPage, info['prevpage'], 2, "")
    if 'nextpage' in info:
        addDir(tNextPage, info['nextpage'], 2, "")

def progList(main_url):
    _progList(main_url)
    endDir()

def progListNext(main_url):
    _progList(main_url)
    endDir(True)

def _episodeList(main_url):
    info = yb88tv.parseEpisodePage(main_url)
    for item in info['link']:
        addDir(item['title'], item['url'], 5, "")
    if 'prevpage' in info:
        addDir(tPrevPage, info['prevpage'], 4, "")
    if 'nextpage' in info:
        addDir(tNextPage, info['nextpage'], 4, "")

def episodeList(main_url):
    _episodeList(main_url)
    endDir()

def episodeListNext(main_url):
    _episodeList(main_url)
    endDir(True)

def videoList(main_url):
    info = yb88tv.parseProg(main_url)
    for item in info['list']:
        addDir(item['title'], item['url'], 6, "")
    endDir()

#-----------------------------------                
def _playFLVCD(url):
    from extract_withflvcd import extract_withFLVCD
    vid_list = extract_withFLVCD(urllib.quote_plus(url))
    if len(vid_list) == 0:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return

    pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    pl.clear()
    for vid in vid_list:
        li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
        li.setInfo( 'video', { "Title": vid['title'] } )
        pl.add(vid['url'], li)
    xbmc.Player().play(pl)

def _playTudou(url):
    import extract_tudou
    vid_list = extract_tudou.extract_video_from_url(url)
    if len(vid_list) == 0:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return

    pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    pl.clear()
    for vid in vid_list:
        li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
        li.setInfo( 'video', { "Title": vid['title'] } )
        pl.add(vid['url']+"|User-Agent="+vid['useragent'], li)
    xbmc.Player().play(pl)

def _playSohu(url):
    import extract_sohu
    vid_list = extract_sohu.extract_video_from_url(urllib.quote_plus(url))
    if len(vid_list) == 0:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return

    pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    pl.clear()
    for vid in vid_list:
        li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
        li.setInfo( 'video', { "Title": vid['title'] } )
        pl.add(vid['url'], li)
    xbmc.Player().play(pl)

def _playYoutube(url, title):
    fmttbl = {"270p":18, "360p":34, "480p":35, "720p":22, "1080p":37}
    import extract_youtube

    vid = url[ url.rfind('/')+1 : ]
    try:
        vid_urls = extract_youtube.extract_video(vid)
    except:
        vid_urls = None
    if vid_urls is None:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return
    qual = int(fmttbl[__addon__.getSetting('youtubeQuality')])
    if vid_urls.has_key(qual):
        url = vid_urls[qual]
        xbmc.log("Youtube: "+url, xbmc.LOGDEBUG)
        li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
        li.setInfo('video', {"Title": title})
        xbmc.Player().play(url, li)
    elif len(vid_urls):
        dialog = xbmcgui.Dialog()
        dialog.ok("Warning", _L(30102))

def _playDmotion(url, title):
    import extract_dailymotion
    vid = extract_dailymotion.extract_id(url)
    vid_urls = extract_dailymotion.extract_video(vid)

    qual = __addon__.getSetting('dailymotionQuality')
    if not vid_urls.has_key(qual):
        return

    pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    pl.clear()
    for url in vid_urls[qual]:
        li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
        li.setInfo('video', {"Title": title})
        pl.add(url, li)
        xbmc.log("Video: "+url, xbmc.LOGDEBUG)
    xbmc.Player().play(pl)

def playWrapper(main_url, title):
    if main_url.find('http://www.dailymotion.com') == 0:
        url = main_url
    else:
        url = yb88tv.parseVideoPlay(main_url)

    if url.find('tudou.com') > 0:
        _playTudou(url)
    elif url.find('youku.com') > 0:
        _playFLVCD(url)
    elif url.find('56.com') > 0:
        _playFLVCD(url)
    elif url.find('letv.com') > 0:
        _playFLVCD(url)
    elif url.find('sohu.com') > 0:
        _playSohu(url)
    elif url.find('youtube.com') > 0:
        _playYoutube(url, title)
    elif url.find('dailymotion.com') > 0:
        _playDmotion(url, title)
    else:
        xbmc.Dialog().ok("Unsupported format", url)

#-----------------------------------                
def get_params():
    param=[]
    paramstring=sys.argv[2]
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
    name=name.encode('utf-8')
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
    name=name.encode('utf-8')
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    u+="&mode="+str(mode)
    u+="&name="+urllib.quote_plus(name)
    u+="&title="
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addRedir(name,url,mode,title="",iconimage="DefaultVideo.png",thumbimage=""):
    name=name.encode('utf-8')
    title=title.encode('utf-8')
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    u+="&mode="+str(mode)
    u+="&name="+urllib.quote_plus(name)
    u+="&title="+urllib.quote_plus(title)
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=thumbimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def endDir(update=False):
    xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=update)

#-----------------------------------                
params=get_params()
url=None
name=None
mode=None
title=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
xbmc.log( "Mode: "+str(mode), xbmc.LOGINFO)
xbmc.log( "URL : "+str(url), xbmc.LOGINFO)
xbmc.log( "Name: "+str(name), xbmc.LOGINFO)

if mode==None:
    rootList()
elif mode==1:
    progList(url)
elif mode==2:
    progListNext(url)
elif mode==3:
    episodeList(url)
elif mode==4:
    episodeListNext(url)
elif mode==5:
    videoList(url)
elif mode==6:
    playWrapper(url, name)

# vim:sts=4:sw=4:et
