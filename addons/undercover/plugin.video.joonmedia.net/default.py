# -*- coding: utf-8 -*-
"""
    JoonMedia - Korea Drama/TV Shows Streaming Service
"""
import urllib,re
import xbmcaddon,xbmcplugin,xbmcgui
import os.path

# plugin constants
__addonid__ = "plugin.video.joonmedia.net"
__addon__ = xbmcaddon.Addon( __addonid__ )

__addon2__ = xbmcaddon.Addon( "script.module.getvideo" )
IMAGE_DIR = xbmc.translatePath( os.path.join( __addon2__.getAddonInfo('path'), 'images' ) )

from BeautifulSoup import BeautifulSoup

root_url = "http://www.mjoon.tv"
show_thumb = __addon__.getSetting('showThumb').lower() == 'true'

#-----------------------------------------------------
def rootList():
    ## not parsing homepage for faster speed
    addDir(u"최근 업데이트",root_url,2,"")
    addDir(u"드라마",root_url+"/vids/list/drama",1,"")
    addDir(u"종영드라마",root_url+"/vids/list/cdrama",1,"")
    addDir(u"예능",root_url+"/vids/list/show",1,"")
    addDir(u"시사교양",root_url+"/vids/list/edu",1,"")
    addDir(u"한국영화",root_url+"/vids/list/krmovie",1,"")
    addDir(u"일본영화",root_url+"/vids/list/jpmovie",1,"")
    addDir(u"중국영화",root_url+"/vids/list/chmovie",1,"")
    endDir()

def progList(main_url):
    html = urllib.urlopen(main_url).read()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    for item in soup.findAll("div", { "class" : "column" } ):
        ref = item.find('a')
        tlist = []
        for s in ref.contents:
            if s.string: tlist.append( s.string )
        title = " / ".join( tlist )
        url = ref['href']
        if not url.startswith('http://'):
            url = root_url + url
        xbmc.log( "TV program: %s" % title.encode('utf-8'), xbmc.LOGDEBUG )

        if show_thumb:
            thumb = item.find('img')['src']
            if thumb.endswith("/utils/icons/"):
                thumb = ""    # fix site bug
            else:
                if not thumb.startswith('http://'):
                    thumb = root_url + thumb
        else:
            thumb = ""
        addDir(title, url, 3, thumb)
    endDir()

def recentList(main_url):
    html = urllib.urlopen(main_url).read()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    for item in soup.findAll( "div", { "class" : "column" } ):
        category = item.find('h2').contents[0]
        addDir(u"[COLOR FFFF0000]%s[/COLOR]" % category, '', 6, '')
        for ref in item.findAll('a'):
            if str(ref.contents[0]).startswith('<strong>'):
                continue    # skip
            tlist = []
            for s in ref.contents:
                if s.string: tlist.append( s.string )
            title = " / ".join( tlist )
            url = ref['href']
            if not url.startswith('http://'):
                url = root_url + url
            xbmc.log( "TV program: %s" % title.encode('utf-8'), xbmc.LOGDEBUG )
            addDir(title, url, 3, '')
    endDir()

def episodeList(main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    colsel = int(__addon__.getSetting("VideoColumn"))
    episodes = soup("div", {"class" : "column"})[colsel-1].findAll('li')
    for episode in episodes:
        title = u""
        for node in episode.contents:
            if node.string:
            	title += node.string
            if getattr(node, 'name', None) == 'br':
            	break
        title = title.strip()

        for ref in episode.findAll('a'):
            url = ref['href']
            if not url.startswith('http://'):
            	url = root_url + url
            suppl = ''.join(ref.findAll(text=True)).strip()
            title2 = u"{0:s} ({1:s})".format(title,suppl)
            xbmc.log( "Found page: %s" % title2.encode('utf-8'), xbmc.LOGDEBUG )

            if url.find('tudou') > 0:
                addRedir(title2, url, 9, "", os.path.join(IMAGE_DIR,"tudou.png"))
            elif url.find('youku') > 0:
                addRedir(title2, url, 4, "", os.path.join(IMAGE_DIR,"youku.png"))
            elif url.find('sohu') > 0:
                addRedir(title2, url, 5, "", os.path.join(IMAGE_DIR,"sohu.png"))
            elif url.find('youtube') > 0:
                addRedir(title2, url, 6, title, os.path.join(IMAGE_DIR,"youtube.png"))
            elif url.find('dmotion') > 0:
                addRedir(title2, url, 7, title, os.path.join(IMAGE_DIR,"dailymotion.png"))
            elif url.find('source') > 0:
                addRedir(title2, url, 8, "")
            else:
                xbmc.Dialog().ok("Unsupported format", url)
    endDir()

#-----------------------------------                
def get_player_link(url):
    html = urllib.urlopen(url).read()
    return re.compile('<a class="player_link" href="([^"]*)" target="_blank">').findall(html)

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
        vid_url = vid['url'].replace("?1","?8") # trick to make streaming easier
        vid_url = vid_url+"|User-Agent="+vid['useragent']
        li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
        li.setInfo( 'video', { "Title": vid['title'] } )
        pl.add(vid_url, li)
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
        dialog.ok("Warning", "You'd be better try again with other Youtube quality")

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

#-----------------------------------                
def playFLVCD(url):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playFLVCD(match[0])

def playTudou(url):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playTudou(match[0])

def playSohu(url):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playSohu(match[0])

def playYoutube(url, title):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playYoutube(match[0], title)

def playDmotion(main_url, title):
    match = get_player_link(main_url)
    if len(match) == 0:
        return
    _playDmotion(match[0], title)

def playWrapper(main_url, title):
    match = get_player_link(main_url)
    if len(match) == 0:
        return
    url = match[0]

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
    recentList(url)
elif mode==3:
    episodeList(url)
elif mode==4:
    playFLVCD(url)
elif mode==5:
    playSohu(url)
elif mode==6:
    playYoutube(url, title)
elif mode==7:
    playDmotion(url, title)
elif mode==8:
    playWrapper(url, title)
elif mode==9:
    playTudou(url)

# vim:sts=4:sw=4:et
