# -*- coding: utf-8 -*-
"""
  Dabdate
"""

import urllib,urllib2,re
import xbmcplugin,xbmcgui,xbmcaddon

# plugin constants
__plugin__ = "Dabdate"
__addonID__ = "plugin.video.dabdate.com"
__url__     = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/addons/plugin.video.dabdate.com"
__credits__ = "XBMC Korean User Group"
__version__ = "0.2.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
if not LIB_DIR in sys.path:
  sys.path.append (LIB_DIR)

COOKIEFILE = xbmc.translatePath( 'special://temp/dabdate_cookie.lwp' )

__settings__ = xbmcaddon.Addon( __addonID__ )
__id__ = __settings__.getSetting( "id" )
__pass__ = __settings__.getSetting( "pass" )
__server1__ = int(__settings__.getSetting( "server1" )) + 1
__server2__ = int(__settings__.getSetting( "server2" )) + 1

#-----------------------------------------------------
def CATEGORIES():
    BROWSE('http://www.dabdate.com')

def BROWSE(url):
    resp = urllib2.urlopen(url)
    items = resp.read().split('<td colspan=7 height=1>')
    for item in items[:-1]:
        match = re.compile('<a href="([^"]*&pr=%s)">' % __server1__).search(item)
        if match:
            vurl = match.group(1)
        else:
            match = re.compile('<a href="([^"]*&pr=%s)">' % __server2__).search(item)
            if match is None:
                continue
            vurl = match.group(1)
        img = re.compile('''<img src='([^']*)' ''').search(item).group(1)
        title = re.compile('''<a href[^>]*><font class=big[^>]*>([^<]*)</font></a>''').search(item).group(1)
        if re.compile('<b>Free').search(item):
	    title = "*"+title
        addDir(title.decode('euc-kr'),"http://www.dabdate.com/"+vurl,11,img)
    query = re.compile("<a href='([^']*)' class=navi>\[Next\]</a>").search(items[-1])
    if query:
        addDir(u"다음 페이지>","http://www.dabdate.com/"+query.group(1),10,'')

def SHOW_WMV(url):
    agent_hdr = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)'

    req = urllib2.Request(url)
    req.add_header('User-Agent', agent_hdr)
    resp = urllib2.urlopen(req)
    newurl = resp.geturl()
    #---
    if newurl.find('login.php') >= 0:
        # form
        from ClientForm import ParseResponse
        forms = ParseResponse(resp)
        resp.close()

        form = forms[0]
        form['id'] = __id__
        form['pass'] = __pass__
  
        resp = urllib2.urlopen( form.click() )
        newurl = resp.geturl()
        cj.save(COOKIEFILE)
        xbmc.log( "LOGIN to %s" % newurl, xbmc.LOGDEBUG )
    #---
    if newurl.find('msg.php') >= 0:
        from ClientForm import ParseResponse
        forms = ParseResponse(resp)
        resp.close()
        form = forms[0]
        req = form.click()  # click default
        req.add_header('User-Agent', agent_hdr)
        req.add_header('Referer', newurl)
        resp = urllib2.urlopen(req)
        newurl = resp.geturl()
        cj.save(COOKIEFILE)
        xbmc.log( "PAY to %s" % newurl, xbmc.LOGDEBUG )
    #---
    if newurl.startswith(url):
        vurl = re.compile("FileName='([^']*)'").search( resp.read() ).group(1)
        cookies = []
        for cookie in cj:
            cookies.append( "%s=%s" % (cookie.name, cookie.value) )
        ckStr = ';'.join(cookies)
        xbmc.Player().play( '%s|Cookie="%s"' % (vurl,ckStr) )
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
              
#-----------------------------------                
params=get_params()
url=None
name=None
mode=None

# set cookie
import cookielib
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
if os.path.isfile(COOKIEFILE):
    cj.load(COOKIEFILE)
    xbmc.log( "Cookie is loaded", xbmc.LOGINFO )
xbmc.log( "Cookie is set, " + COOKIEFILE, xbmc.LOGINFO )

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
elif mode==10:
    BROWSE(url)
elif mode==11:
    SHOW_WMV(url)

if mode != 11:
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
