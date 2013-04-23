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

root_url = "http://"+__addon__.getSetting("SiteAddr")
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
    soup = BeautifulSoup( link.read() )
    cols = soup("div", {"class" : "column"})
    thumb = root_url + cols[0].find('img')['src']
    colsel = int(__addon__.getSetting("VideoColumn"))
    for episode in cols[colsel-1].findAll('li'):
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
                addRedir(title2, url, 9, "", os.path.join(IMAGE_DIR,"tudou.png"), thumb)
            elif url.find('youku') > 0:
                addRedir(title2, url, 4, "", os.path.join(IMAGE_DIR,"youku.png"), thumb)
            elif url.find('sohu') > 0:
                addRedir(title2, url, 5, "", os.path.join(IMAGE_DIR,"sohu.png"), thumb)
            elif url.find('youtube') > 0:
                addRedir(title2, url, 6, title, os.path.join(IMAGE_DIR,"youtube.png"), thumb)
            elif url.find('dmotion') > 0:
                addRedir(title2, url, 7, title, os.path.join(IMAGE_DIR,"dailymotion.png"), thumb)
            elif url.find('source') > 0:
                addRedir(title2, url, 8, thumbimage=thumb)
            else:
                xbmc.Dialog().ok("Unsupported format", url)
    endDir()

#-----------------------------------                
def get_player_link(url):
    html = urllib.urlopen(url).read()
    return re.compile('<a class="player_link" href="([^"]*)" target="_blank">').findall(html)

def _play_link(vid_list, thumb):
    pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    pl.clear()
    for vid in vid_list:
        li = xbmcgui.ListItem(vid['title'], thumbnailImage=thumb)
        li.setInfo( 'video', { "Title": vid['title'] } )
        pl.add(vid['url'], li)
    xbmc.Player().play(pl)

def _playFLVCD(url, thumb):
    from extract_withflvcd import extract_withFLVCD
    vid_list = extract_withFLVCD(urllib.quote_plus(url))
    if len(vid_list) == 0:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return
    _play_link(vid_list, thumb)

def _playTudou(url, thumb):
    import extract_tudou
    vid_list = extract_tudou.extract_video_from_url(url)
    if len(vid_list) == 0:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return
    # Tudou checks if User-Agent string remains same from start
    for i in range(len(vid_list)):
        vid_list[i]['url'] += "|User-Agent="+vid_list[i]['useragent']
    _play_link(vid_list, thumb)

def _playSohu(url, thumb):
    import extract_sohu
    vid_list = extract_sohu.extract_video_from_url(urllib.quote_plus(url))
    if len(vid_list) == 0:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return
    _play_link(vid_list, thumb)

def _playYoutube(url, title, thumb):
    fmttbl = {"270p":18, "360p":34, "480p":35, "720p":22, "1080p":37}
    import extract_youtube

    vid = url[ url.rfind('/')+1 : ]
    try:
        vid_urls = extract_youtube.extract_video(vid)
    except:
        xbmcgui.Dialog().ok("Fail to extract video", url)
        return
    qual = int(fmttbl[__addon__.getSetting('youtubeQuality')])
    if not vid_urls.has_key(qual):
        if len(vid_urls):
            dialog = xbmcgui.Dialog()
            dialog.ok("Warning", "You'd be better try again with other Youtube quality")
        return
    _play_link([{'title':title,'url':vid_urls[qual]}], thumb)

def _playDmotion(url, title, thumb):
    import extract_dailymotion
    vid = extract_dailymotion.extract_id(url)
    vid_urls = extract_dailymotion.extract_video(vid)

    qual = __addon__.getSetting('dailymotionQuality')
    if not vid_urls.has_key(qual):
        return
    _play_link([{'title':title,'url':url} for url in vid_urls[qual]], thumb)

#-----------------------------------                
def playFLVCD(url, thumb):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playFLVCD(match[0], thumb)

def playTudou(url, thumb):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playTudou(match[0], thumb)

def playSohu(url, thumb):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playSohu(match[0], thumb)

def playYoutube(url, title, thumb):
    match = get_player_link(url)
    if len(match) == 0:
        return
    _playYoutube(match[0], title, thumb)

def playDmotion(main_url, title, thumb):
    match = get_player_link(main_url)
    if len(match) == 0:
        return
    _playDmotion(match[0], title, thumb)

def playWrapper(main_url, title, thumb):
    match = get_player_link(main_url)
    if len(match) == 0:
        return
    url = match[0]

    if url.find('tudou.com') > 0:
        _playTudou(url, thumb)
    elif url.find('youku.com') > 0:
        _playFLVCD(url, thumb)
    elif url.find('56.com') > 0:
        _playFLVCD(url, thumb)
    elif url.find('letv.com') > 0:
        _playFLVCD(url, thumb)
    elif url.find('sohu.com') > 0:
        _playSohu(url, thumb)
    elif url.find('youtube.com') > 0:
        _playYoutube(url, title, thumb)
    elif url.find('dailymotion.com') > 0:
        _playDmotion(url, title, thumb)
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
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
    u+="&playtitle=&playthumb="
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addRedir(name,url,mode,title="",iconimage="DefaultVideo.png",thumbimage="DefaultVideo.png"):
    u=sys.argv[0]
    u+="?url="+urllib.quote_plus(url)
    u+="&mode="+str(mode)
    u+="&name="+urllib.quote_plus(name.encode('utf-8'))
    u+="&playtitle="+urllib.quote_plus(title.encode('utf-8'))
    u+="&playthumb="+urllib.quote_plus(thumbimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
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
playtitle=None
playthumb=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: playtitle=urllib.unquote_plus(params["playtitle"])
except: pass
try: playthumb=urllib.unquote_plus(params["playthumb"])
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
    playFLVCD(url, playthumb)
elif mode==5:
    playSohu(url, playthumb)
elif mode==6:
    playYoutube(url, playtitle, playthumb)
elif mode==7:
    playDmotion(url, playtitle, playthumb)
elif mode==8:
    playWrapper(url, playtitle, playthumb)
elif mode==9:
    playTudou(url, playthumb)

# vim:sts=4:sw=4:et
