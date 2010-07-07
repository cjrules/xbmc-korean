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
__version__ = "0.0.1"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
if not LIB_DIR in sys.path:
  sys.path.append (LIB_DIR)

COOKIEFILE = xbmc.translatePath( 'special://masterprofile/_dabdate_cookie.lwp' )
TEMPDIR = xbmc.translatePath('special://temp')

__settings__ = xbmcaddon.Addon( __addonID__ )
__id__ = __settings__.getSetting( "id" )
__pass__ = __settings__.getSetting( "pass" )
__server__ = __settings__.getSetting( "ServerSel" )
MAX_TEMP = int( __settings__.getSetting( "MaxTemp" ) )

#-----------------------------------------------------
def CATEGORIES():
    BROWSE('http://www.dabdate.com')

def BROWSE(url):
    resp = urllib2.urlopen(url)
    items = resp.read().split('<td colspan=7 height=1>')
    for item in items[:-1]:
        vurl,img = re.compile('''<a href="([^"]*)"><img src='([^']*)' ''').search(item).group(1,2)
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
        print "LOGIN to %s" % newurl
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
        print "PAY to %s" % newurl
    #---
    if newurl.startswith(url):
        vurl = re.compile("FileName='([^']*)'").search( resp.read() ).group(1)
        #-- following code doesn't work lack of cookie support
        #addLink(u"시청", vurl, '')
        #-- store and run version
	import os.path
	tempname = "_dabdate_temp_%s.wmv" % re.compile('idx=(\d+)').search(url).group(1)
	TEMPFILE = os.path.join(TEMPDIR, tempname)
        # save video to local temp file
	if clear_temp_file(TEMPFILE) or save_wmv(vurl, TEMPFILE):
            addLink(u"시청", TEMPFILE, '')
    else:
        print "ERROR: %s is redirected to %s" % (url,newurl)

def clear_temp_file(tempfile):
    import os,glob
    temp_list = glob.glob(os.path.join(TEMPDIR, "_dabdate_temp_*.wmv"))
    for fx in temp_list[:-MAX_TEMP]:
	if tempfile != fx:
	    os.remove(fx)
    return tempfile in temp_list

def save_wmv(url,local):
    try: resp = urllib2.urlopen(url)
    except urllib2.URLError, e:
        print e.reason
        return False
    try:
        f = open(local,'wb')
    except IOError:
        print "File can not be written, %s" % local
        sys.exit(1)

    fileSz = int( resp.info()['Content-Length'] )
    stepSz = 1024*1024        # 1MB step size

    dialog = xbmcgui.DialogProgress()
    #ignored = dialog.create(__plugin__, u"저장")
    sz = 0
    dialog.update( 0 )
    while True:
	if dialog.iscanceled():
	    return False
	buf = resp.read(stepSz)
	if not buf: break
	sz += len(buf)
	f.write( buf )
	dialog.update( 100*sz/fileSz )
    f.close(); resp.close()
    dialog.close()

    if sz < fileSz:
	import os
	os.remove(local)
	return False
    return True

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
    print "Cookie is loaded"
print "Cookie is set, " + COOKIEFILE

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

xbmcplugin.endOfDirectory(int(sys.argv[1]))
