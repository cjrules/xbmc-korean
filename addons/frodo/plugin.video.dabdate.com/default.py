# -*- coding: utf-8 -*-
"""
  Dabdate - Korea Drama/TV Shows Streaming Service
"""
import urllib, urllib2, re
import xbmcplugin, xbmcgui, xbmcaddon

# plugin constants
__plugin__ = "Dabdate"
__addonid__ = "plugin.video.dabdate.com"

CookieFile = xbmc.translatePath( 'special://temp/dabdate_cookie.lwp' )
BrowserAgent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)'
PlayerAgent  = 'Windows-Media-Player/12.0.7601.17514'

_A_ = xbmcaddon.Addon( __addonid__ )
_L_ = _A_.getLocalizedString
_S_ = _A_.getSetting

qualcode = {
    ''         :'1',    # default
    _L_(31000) :'1',
    _L_(31001) :'2',
    _L_(31002) :'3',
    _L_(31003) :'m',
}
localcode = {
    ''         :'la1',  # default
    _L_(31010) :'au1',
    _L_(31011) :'au2',
    _L_(31012) :'au3',
    _L_(31013) :'eu',
    _L_(31014) :'sa',
    _L_(31015) :'la1',
    _L_(31016) :'la2',
    _L_(31017) :'la3',
    _L_(31018) :'la4',
    _L_(31019) :'ny1',
    _L_(31020) :'ny2',
    _L_(31021) :'ny3',
}

__id__   = _S_( "id" )
__pass__ = _S_( "pass" )
__qual__ = qualcode[ _S_( "quality" ).decode('utf-8') ]
__local__ = localcode[ _S_( "local" ).decode('utf-8') ]

if __qual__=='m':
    root_url = "http://m.dabdate.com/"
    if __local__[:3]=="au":
        __qual__ = 'mAU'
else:
    root_url = "http://dabdate.com/"

tPrevPage = u"[B]<%s[/B]" % _L_(30200)
tNextPage = u"[B]%s>[/B]" % _L_(30201)

#-----------------------------------------------------
def CATEGORIES():
    _BROWSE(root_url)
    addDir(u"[COLOR FF0000FF]로보카 폴리[/COLOR]", root_url+"?lang=5", 12, '')
    addDir(u"[COLOR FF0000FF]그때를 아십니까[/COLOR]", root_url+"?lang=7", 12, '')
    addDir(u"[COLOR FF0000FF]특선 다큐멘터리[/COLOR]", root_url+"?lang=6", 12, '')
    endDir()

def BROWSE(url):
    _BROWSE(url)
    endDir(True)

def BROWSE2(url):
    _BROWSE(url)
    endDir()

def _BROWSE(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', BrowserAgent)
    psrc = urllib2.urlopen(req).read()
    items = re.split("<td colspan=\d+ height=\d+>", psrc)
    for item in items[:-1]:
    	try:
            title = re.compile('''<a href[^>]*pr=[1|m]"><font [^>]*>(.*?)</font></a>''').search(item).group(1)
            title = re.compile("</?b>").sub("",title)
            if re.compile('<b>Free').search(item):
                title = "[B]"+title+"[/B]"
        except:
            continue

        match = re.compile('''<img src='([^']*)' ''').search(item)
        if match:
            img = match.group(1)
        else:
            img = ""

        vurl = None
        if root_url.startswith("http://dabdate.com") and __qual__=='1':
            match = re.compile("<a href='([^']*&pr={0:s}&local={1:s})'>".format(__qual__, __local__)).search(item)
            if match:
                vurl = root_url + match.group(1)
        else:
            match = re.compile('<a href="([^"]*&pr={0:s})">'.format(__qual__)).search(item)
            if match:
                vurl = root_url + match.group(1)
        # fallback
        if vurl is None:
            #match = re.compile("<a href='([^']*&pr=1&local={0:s})'>".format(__local__)).search(item)
            match = re.compile('<a href="([^"]*&pr=1)">').search(item)
            if match:
                vurl = root_url + match.group(1)
        if vurl is None:
            xbmc.log("Video, {0:s}, doesn't exist on {1:s} server".format(title, __qual__), xbmc.LOGERROR)
            #dialog = xbmcgui.Dialog()
            #dialog.ok(u"Error", u"{1:s} 에서 {0:s}을 찾을 수 없습니다".format(title, __qual__))
        addDir(title.decode('euc-kr'),vurl,11,img)

    query = re.compile("<a href='([^']*)' class=navi>\[Prev\]</a>").search(psrc)
    if query:
        addDir(tPrevPage,root_url+query.group(1),10,'')
    query = re.compile("<a href='([^']*)' class=navi>\[Next\]</a>").search(psrc)
    if query:
        addDir(tNextPage,root_url+query.group(1),10,'')

def PLAY_VIDEO(url, title):
    req = urllib2.Request(url)
    req.add_header('User-Agent', BrowserAgent)
    resp = urllib2.urlopen(req)
    newurl = resp.geturl()
    #---
    if newurl.find('order.php') >= 0:
        resp.close()
        # POST
    	if __id__ == "" or __pass__ == "":
    	    dialog = xbmcgui.Dialog()
    	    dialog.ok(_L_(30202), _L(30203))
    	    return
        values = {
            'mode':'login',
            'url' :url,
            'id'  :__id__,
            'pass':__pass__
        }
        req = urllib2.Request( 'http://www.dabdate.com/login.php', urllib.urlencode(values) )
        req.add_header('User-Agent', BrowserAgent)
        req.add_header('Referer', newurl)
        resp = urllib2.urlopen( req )
        newurl = resp.geturl()
        cj.save(CookieFile)
        xbmc.log( "LOGIN to %s" % newurl, xbmc.LOGDEBUG )
    #---
    if newurl.find('msg.php') >= 0:
        resp.close()
        # POST
        values = {
            'mode':'auto',
            'mno' :'',
            'url' :url,
            'auto':'0'
        }
        req = urllib2.Request( 'http://www.dabdate.com/msg.php', urllib.urlencode(values) )
        req.add_header('User-Agent', BrowserAgent)
        req.add_header('Referer', newurl)
        resp = urllib2.urlopen(req)
        newurl = resp.geturl()
        cj.save(CookieFile)
        xbmc.log( "PAY to %s" % newurl, xbmc.LOGDEBUG )
    #---
    newurl = resp.geturl()
    doc = resp.read()
    resp.close()
    if newurl.startswith(url):
    	if newurl.startswith("http://m.dabdate.com"):
            vurl = re.compile(r"location\.href\s*=\s*'([^']*)'").search( doc ).group(1)
        else:
            vurl = re.compile("FileName='([^']*)'").search( doc ).group(1)
            if not vurl.startswith("http://"):
                vurl = "http://dabdate.com/"+vurl
        cookies = []
        for cookie in cj:
            cookies.append( "%s=%s" % (cookie.name, cookie.value) )
        ckStr = ';'.join(cookies)
        playUrl = '{0:s}|User-Agent={1:s}&Cookie="{2:s}"'.format(vurl, PlayerAgent, ckStr)
        li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
        li.setInfo( 'video', { "Title": title } )
        xbmc.Player().play( playUrl, li )
    else:
        xbmc.log( "ERROR: %s is redirected to %s" % (url,newurl), xbmc.LOGERROR )

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
    try:
        xbmc.log( "addLink(%s,%s)" % (name, url), xbmc.LOGDEBUG )
    except:
        pass
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

# set cookie
import os
import cookielib
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
if os.path.isfile(CookieFile):
    cj.load(CookieFile)
    xbmc.log( "Cookie is loaded", xbmc.LOGINFO )
xbmc.log( "Cookie is set, " + CookieFile, xbmc.LOGINFO )

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

if mode==None or mode==1:
    CATEGORIES()
elif mode==10:
    BROWSE(url)
elif mode==11:
    PLAY_VIDEO(url, name)
elif mode==12:
    BROWSE2(url)

# vim:ts=8:sts=4:sw=4:et
