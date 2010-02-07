# coding=utf-8
"""
  Daum tvpot / Starcraft gamecast
"""

import urllib,urllib2,re,xbmcplugin,xbmcgui

# plugin constants
__plugin__ = "Daum Starcraft"
__author__ = "edge"
__url__ = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/Daum%20Starcraft"
__credits__ = "XBMC Korean User Group"
__version__ = "0.1.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

# site
slHome  = "http://tvpot.daum.net/game/sl/"
clipUrl = "http://tvpot.daum.net/clip/ClipView.do?clipid="

def CATEGORIES():
        addDir("01 - 프로리그", slHome+"LeagueList.do?league=pro&type=list",2,'')
        addDir("02 - 온게임넷 스타리그", slHome+"LeagueList.do?league=osl&type=list",2,'')
        addDir("03 - (지난게임) 프로리그", slHome+"LeagueList.do?league=pro&type=list",1,'')
        addDir("04 - (지난게임) 온게임넷 스타리그", slHome+"LeagueList.do?league=osl&type=list",1,'')

def STAR_LEAGUE(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        minfc=re.compile('''\s*<h5><strong>(\d{4}.\d{2}.\d{2})</strong>.*?</h5>\s*<p>\s*(.*)</p>''')
        setc1=re.compile('''([^<]+)</strong>\s*<dl>\s*<dt[^/]+</dt>\s*<dd class="player">\s*<a class=[^>]+>([^<]+)</a>\s*<em[^/]+</em>\s*</dd>\s*</dl>\s*<span>VS</span>\s*<dl class="right">\s*<dt[^/]+</dt>\s*<dd class="player">\s*<a class=[^>]+>([^<]+)</a>\s*<em[^/]+</em>\s*</dd>\s*</dl>\s*<a href="/clip/ClipView.do\?clipid=(\d+)" class="playBtn on">''')
        setc2=re.compile('''([^<]+)</strong>\s*<dl>\s*<dt[^/]+</dt>\s*<dd class="description">([^<]+)</dd>\s*</dl>\s*<a href="/clip/ClipView.do\?clipid=(\d+)" class="playBtn on"''')

        mgrp=re.split('''<div class="matchGroup">''',link)
        xbmc.log( "#match groups=%d"%(len(mgrp)-1), xbmc.LOGDEBUG )
        match_cnt=0
        for mgdata in mgrp[1:]:                #skip first chunk
                match_cnt = match_cnt+1

                mset=re.split('''<strong class="set">''',mgdata)
                xbmc.log( "#set in match%d=%d"%(match_cnt, len(mset)-1), xbmc.LOGDEBUG )

                # match date & title
                mhdr = re.sub('\s+',' ',mset[0])
                mginfo = minfc.match(mhdr)
                if (mginfo is None):
                        match_date = ""
                        match_title = ""
                else:
                        match_date  = mginfo.group(1)
                        match_title = re.sub('<br\s*/?>',' ',mginfo.group(2))
                        match_title = re.sub('<[^>]*>','',match_title)
                        match_title = re.sub('\s*$','',match_title)

                # players in each set
                for setdata in mset[1:]:
                        match = setc1.findall(setdata)
                        for setname,player1,player2,clipid in match:
                                url = clipUrl + clipid
                                VIDEOLINKS("%s %s - %s[%s vs %s]" % (match_date,match_title,setname,player1,player2),url,'')
                        match=setc2.findall(setdata)
                        for setname,descr,clipid in match:
                                if clipid == 0:
                                        continue
                                url = clipUrl + clipid
                                VIDEOLINKS("%s %s - %s[%s]" % (match_date,match_title,setname,descr),url,'')


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
                addDir( "%s 페이지" % match.group(1), main_url, 2, '' )
            elif (navpage[:10] == ''' class="pg'''):
                match = re.match( ''' class="pg[LR]"><a href="([^"]*)"><em>(.*?)</em></a></th>''', navpage )
                url = slHome + re.sub('&amp;','&',match.group(1))
                addDir( "%s 페이지" % match.group(2), url, 1, '' )
            elif (navpage[:8] == "><a href" or navpage[:13] == ''' class="last"'''):
                match = re.match( '''\s*[^>]*><a href="([^"]*)">(\d+)</a></td>''', navpage )
                if (match is None):
                    xbmc.log( "Unexpected parsing error in %s" % navpage, xbmc.LOGERROR )
                    continue
                url = slHome + re.sub('&amp;','&',match.group(1))
                addDir( "%s 페이지" % match.group(2), url, 2, '' )

def VIDEOLINKS(name,url,thumbnail):
        xbmc.log( "videolink(%s,%s)" % (name,url), xbmc.LOGDEBUG )
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
        
elif mode==2:
        STAR_LEAGUE(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
