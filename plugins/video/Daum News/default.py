# coding=utf-8
"""
  Daum Media TV News service
"""

import urllib,urllib2,re,xbmcplugin,xbmcgui

# plugin constants
__plugin__ = "Daum TV News"
__author__ = "anonymous"
__url__ = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/Daum%20News"
__credits__ = "XBMC Korean User Group"
__version__ = "0.1.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

#TV DASH - by You 2008.

def CATEGORIES():
        req = urllib2.Request('http://tvnews.media.daum.net/')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class="M"><a href="(.+?)" id=".+?">(.+?)</a></li>').findall(link)
        count=1
        for url,name in match:
                url = re.sub('&amp;','&',url)
                addDir("%02d - "%(count) + name,url,3,'')
                count += 1

def NEWS_PROGRAM(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_div=re.compile('<div class="TvBro3">(.+?)</div>', re.DOTALL).findall(link)

        if len( match_div) > 0:
                match=re.compile('<a href="(.+?)">(.+?)</a>').findall(match_div[0])
                count=1
                for url,name in match:
                        url = re.sub('&amp;','&',url)
                        addDir("%02d - "%(count) + name,url,1,'')
                        count += 1
        else:
                INDEX(main_url)

def INDEX(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<dl class="TV_RL">\s+<dd class="fl"><a href=".+?"><img src="(.+?)" width="100" height="76" alt="" /></a><br /></dd>\s+<dt class="fl"><a href="(.+?)">(.+?)</a><br /></dt>').findall(link)
        count=1
        for thumbnail,url,name in match:
                name = re.sub('&lt;','<',name)
                name = re.sub('&gt;','>',name)
                name = re.sub('&#39;','\'',name)
                url = re.sub('&amp;','&',url)
                VIDEOLINKS("%02d - "%(count) + name,main_url+url,thumbnail)
                count += 1
        if count == 1:
                match=re.compile('''<a href="(.+?)"><img src="(.+?)" width="120" height="90" alt="" class="img" /></a>\s+ <div class="R">\s+<h4><a href=".+?" class="tit">(.+?)</a></h4>''').findall(link)
                for url,thumbnail,name in match:
                    name = re.sub('&lt;','<',name)
                    name = re.sub('&gt;','>',name)
                    name = re.sub('&#39;','\'',name)
                    url = re.sub('&amp;','&',url)
                    VIDEOLINKS("%02d - "%(count) + name,main_url+url,thumbnail)
                    count += 1


def VIDEOLINKS(name,url,thumbnail):
        xbmc.log( "videolink(%s,%s)" % (name,url), xbmc.LOGDEBUG )
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''UI.tvpotSWF\("http://flvs.daum.net/flvPlayer.swf\?vid=(.+?)"\)''').findall(link)
        for vid in match:
                flv = DaumGetFlvByVid(url,vid)
                if flv is not None:
                    addLink(name,flv,thumbnail)

#Python Video Decryption and resolving routines.
#Courtesy of Voinage, Coolblaze.        

def DaumGetFLV(referer, url):
    xbmc.log( "daum loc=%s" % url, xbmc.LOGINFO )
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.search('''<MovieLocation movieURL="(.+?)"\s*/>''', response)
    if query_match:
        return query_match.group(1)
    xbmc.log( "Fail to find FLV location from %s" % url, xbmc.LOGERROR )
    return None

def DaumGetFlvByVid(referer, vid):
    xbmc.log( "daum vid=%s" % vid, xbmc.LOGDEBUG )
    req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.search('''<MovieLocation regdate="\d+" url="([^"]*)" storage="[^"]*"\s*/>''', response)
    if query_match:
        url = re.sub('&amp;','&',query_match.group(1))
        return DaumGetFLV(referer, url)
    xbmc.log( "Fail to find FLV reference with %s" % vid, xbmc.LOGERROR )
    return None


                
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
        xbmc.log( "addLink(%s,%s)" % (name, url), xbmc.LOGDEBUG )
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        xbmc.log( "addDir(%s)" % u, xbmc.LOGDEBUG )
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

xbmc.log( "Mode: "+str(mode), xbmc.LOGINFO)
xbmc.log( "URL : "+str(url), xbmc.LOGINFO)
xbmc.log( "Name: "+str(name), xbmc.LOGINFO)

if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        INDEX(url)
        
elif mode==3:
        NEWS_PROGRAM(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
