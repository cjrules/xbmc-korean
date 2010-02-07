# coding=utf-8
"""
  Daum tvpot / Best video clip
"""
import urllib,urllib2,re,xbmcplugin,xbmcgui

# plugin constants
__plugin__ = "Daum Best"
__author__ = "edge"
__url__ = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/Daum%20Best"
__credits__ = "XBMC Korean User Group"
__version__ = "0.1.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

# site
bestHome = "http://tvpot.daum.net/best/"

def CATEGORIES():
        addDir('1 - 일간 베스트', bestHome+'BestToday.do?svctab=best&range=0',3,'')
        addDir('2 - 주간 베스트', bestHome+'BestToday.do?svctab=best&range=1',3,'')
        addDir('3 - 월간 베스트', bestHome+'BestToday.do?svctab=best&range=2',3,'')
        addDir('4 - 10만 플레이', bestHome+'BestToday.do?svctab=10m',3,'')
        addDir('5 - (지난) 일간 베스트', bestHome+'BestToday.do?svctab=best&range=0',2,'')
        addDir('6 - (지난) 주간 베스트', bestHome+'BestToday.do?svctab=best&range=1',2,'')
        addDir('7 - (지난) 월간 베스트', bestHome+'BestToday.do?svctab=best&range=2',2,'')
        addDir('8 - (지난) 10만 플레이', bestHome+'BestToday.do?svctab=10m',1,'')
                       
def BEST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''<img src="([^"]+)" width="110" height="84" alt="[^"]+"\s+title="([^"]+)" /></a></dd>\s*<dt><a href="([^"]+)">''').findall(link)
        count=1
        for thumbnail,name,url in match:
                name = re.sub('\n',' ',name)
                name = re.sub('&lt;','<',name)
                name = re.sub('&gt;','>',name)
                name = re.sub('&quot;','"',name)
                name = re.sub('&#39;','\'',name)
                if url[0] == '/':
                        url = 'http://tvpot.daum.net' + url
                url = re.sub('&amp;','&',url)
                url = re.sub(' ','',url)
                VIDEOLINKS("%02d - "%(count) + name,url,thumbnail)
                count += 1
        xbmc.log( "matched item %d" % count, xbmc.LOGDEBUG )

def INDEX_BEST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''<li class="bar11c[^"]*">\s*<a href="([^"]*)"\s+title="([^"]*)">''').findall(link)
        count=0
        for url,date in match[:len(match)/2]:     # menu bar is shown twice in the page
                count += 1
                url = bestHome + "BestToday.do" + re.sub('&amp;','&',url)
                addDir(date, url, 3, '')
        xbmc.log( "page found %d" % count, xbmc.LOGDEBUG )

def INDEX(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()

        navhdr = re.search('''<table class="pageNav2"[^>]*>''', link)
        if (navhdr is None):
            xbmc.log( "No navigation table is found", xbmc.LOGWARNING )
            return
        import string
        navtend = string.find(link, "</table>", navhdr.end())
        navtbl = link[ navhdr.end() : navtend ]
        navpgs = re.split("<t[dh]", navtbl)
        for navpage in navpgs[1:]:
            match = re.search( '''<span class="sel">(\d+)</span>''', navpage )
            if (match is not None):
                addDir( "%s 페이지" % match.group(1), main_url, 3, '' )
            elif (navpage[:10] == ''' class="pg'''):
                match = re.match( ''' class="pg[LR]"><a href="([^"]*)"><em>(.*?)</em></a></th>''', navpage )
                url = bestHome + re.sub('&amp;','&',match.group(1))
                addDir( "%s 페이지" % match.group(2), url, 1, '' )
            elif (navpage[:8] == "><a href" or navpage[:13] == ''' class="last"'''):
                match = re.match( '''\s*[^>]*><a href="([^"]*)">(\d+)</a></td>''', navpage )
                if (match is None):
                    xbmc.log( "Unexpected parsing error in %s" % navpage, xbmc.LOGERROR )
                    continue
                url = bestHome + re.sub('&amp;','&',match.group(1))
                addDir( "%s 페이지" % match.group(2), url, 3, '' )

def VIDEOLINKS(name,url,thumbnail):
        xbmc.log( "daum videolink(%s)=%s" % (name, url), xbmc.LOGDEBUG )
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        # daumEmbed_jingle2 had 3 arguments, but daumEmbed_standard had 4
        match=re.compile('''daumEmbed_.+?\('.+?','(.+?)','.+?'[,\)]''').findall(link)
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
        xbmc.log( "get_params() "+paramstring, xbmc.LOGDEBUG )
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
        xbmc.log( "addLink() %s %s" % (name, url), xbmc.LOGDEBUG )
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

xbmc.log( "Mode: "+str(mode), xbmc.LOGINFO )
xbmc.log( "URL : "+str(url), xbmc.LOGINFO )
xbmc.log( "Name: "+str(name), xbmc.LOGINFO )

if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        INDEX(url)

elif mode==2:
        INDEX_BEST(url)

elif mode==3:
        BEST(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
