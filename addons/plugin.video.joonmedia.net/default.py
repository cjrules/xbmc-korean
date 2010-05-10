# coding=utf-8
"""
  JoonMedia - Korea Drama/TV Shows Streaming Service
"""

import urllib,xbmcplugin,xbmcgui

# plugin constants
__plugin__  = "JoonMedia"
__author__  = "edge"
__url__     = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/JoonMedia"
__credits__ = "XBMC Korean User Group"
__version__ = "1.1.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
if not LIB_DIR in sys.path:
    sys.path.append (LIB_DIR)

from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
from getflv import GetFLV

#-----------------------------------------------------
def CATEGORIES():
    ## not parsing homepage for faster speed
    addDir(u"최근 업데이트","http://joonmedia.net",2,"")
    addDir(u"드라마","http://joonmedia.net/videos/dramas",1,"")
    addDir(u"오락","http://joonmedia.net/videos/shows",1,"")
    addDir(u"음악","http://joonmedia.net/videos/music",1,"")
    addDir(u"다시보기","http://joonmedia.net/videos/classics",1,"")
    addDir(u"영화","http://joonmedia.net/videos/movies",1,"")
    addDir(u"일본영화","http://joonmedia.net/videos/jpmovies",1,"")
    addDir(u"중국영화","http://joonmedia.net/videos/chmovies",1,"")
    addDir(u"서양영화","http://joonmedia.net/videos/enmovies",1,"")
    addDir(u"다큐","http://joonmedia.net/videos/docu",1,"")
    addDir(u"시사교양","http://joonmedia.net/videos/edu",1,"")

def VIDEO(main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    strain = SoupStrainer( "div", { "class" : "column" } )
    for item in soup.findAll(strain):
	ref = item.find('a')
	title = ref.string
	url = ref['href']
	thumb = item.find('img')['src']
	try:
	    xbmc.log( "TV program: %s" % title.encode("utf-8"), xbmc.LOGDEBUG )
	except:
	    pass    # skip unwanted encoding error (ex: Japanese character)
	addDir(title, url, 3, thumb)

def RECENT(main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    strain = SoupStrainer( "div", { "class" : "column" } )
    for item in soup.findAll(strain):
	category = item.find('h2').contents[0]
	addDir("---------------- %s ----------------" % category, '', 6, '')
	for ref in item.findAll('a'):
	    if str(ref.contents[0]).startswith('<strong>'):
		continue	# skip
	    title = ref.string
	    url = ref['href']
	    try:
		xbmc.log( "TV program: %s" % title.encode("utf-8"), xbmc.LOGDEBUG )
	    except:
		pass    # skip unwanted encoding error (ex: Japanese character)
	    addDir(title, url, 3, '')

def TVSHOW(main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    episodes = soup("div", {"class" : "column"})[3].findAll('li')
    for episode in episodes:
	title = ''.join(episode.find('b').findAll(text=lambda text:isinstance(text, NavigableString)))
	for ref in episode.findAll('a'):
	    url = ref['href']
	    suppl = ''.join(ref.findAll(text=lambda text:isinstance(text, NavigableString))).strip()
	    title2 = "%s (%s)" % (title,suppl)
	    try:
		xbmc.log( "Found page: %s" % title2.encode("utf-8"), xbmc.LOGDEBUG )
	    except:
		pass
	    if suppl.find(u"멀티로딩")==0:
		addDir( title2.replace(u"멀티로딩",u"유큐"), url, 5, '' )
	    elif suppl.find(u"토두")==0 or suppl.find(u"56com")==0:
		addDir( title2, url, 4, '' )
	    elif suppl.find(u"베오")==0:
		addDir( title2+u" [preview]", url, 4, '' )
	    elif suppl.find(u"하이스피드")==0:
		addDir( title2, url, 5, '' )
	    elif suppl.find(u"유튜브")==0 or suppl.lower()==u"youtube":
		addDir( title2, url, 6, '' )
	    elif suppl.find(u"데일리모션")==0:
		addDir( title2, url, 7, '' )
	    else:
		print "Unexpected: %s" % suppl.encode('euc-kr')

def EPISODE(main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    extr = GetFLV()
    i=0
    for item in soup.findAll('embed'):
	swf = item['src']
	thumb = extr.img(swf)
	xbmc.log( "Container[0]: %s" % swf, xbmc.LOGDEBUG )
	for flv in extr.flv(swf):
	    i=i+1;addLink("Part %d" % i, flv, thumb)

def EPISODE_DIRECT(main_url):
    # BeautifulSoup can not handle a statement not protected by quote
    import re
    tDoc = urllib.urlopen(main_url).read().decode('utf-8')
    i=0
    blks = re.compile('src=\S*vcastr_file=(\S*)').findall(tDoc)
    print "TEST: %d"%len(blks)
    for blk in blks:
	for vid in blk.split('|'):
	    i=i+1;addLink("Part %d" % i, vid, '')

def EPISODE_YOUTUBE(main_url):
    link = urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
    extr = GetFLV()
    i=0
    for item in soup.findAll('embed'):
	try:
	    swf = item['flashvars']
	except:
	    swf = None
	if swf:
	    ptn2 = 'file='
	    swf = swf[swf.find(ptn2)+len(ptn2):swf.find('&amp;')]
	    thumb = extr.img(swf)
	    xbmc.log( "Container[1]: %s" % swf, xbmc.LOGDEBUG )
	    for flv in extr.flv(swf):
		i=i+1;addLink("Part %d" % i, flv, thumb)
	else:
	    swf = item['src']
	    if '&' in swf:
		swf = swf[:swf.find('&')]
	    thumb = extr.img(swf)
	    xbmc.log( "Container[2]: %s" % swf, xbmc.LOGDEBUG )
	    for flv in extr.flv(swf):
		i=i+1;addLink("Part %d" % i, flv, thumb)

def EPISODE_PARAM(main_url):
    link = urllib.urlopen(main_url)
    strain = SoupStrainer( "param", { "name" : "movie" } )
    soup = BeautifulSoup( link.read(), strain, fromEncoding="utf-8" )
    extr = GetFLV()
    i=0
    for item in soup.findAll('param'):
	cntnr=item['value']
	xbmc.log( "Container[3]: %s" % cntnr, xbmc.LOGDEBUG )
	thumb = extr.img(cntnr)
	for flv in extr.flv(cntnr):
	    i=i+1;addLink("Part %d" % i, flv, thumb)

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
    xbmc.log( "addLink(%s,%s)" % (name, url), xbmc.LOGDEBUG )
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
    name=name.encode("utf-8")
    xbmc.log( "addDir(%s)" % name, xbmc.LOGDEBUG )
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
              
#-----------------------------------                
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
    VIDEO(url)
elif mode==2:
    RECENT(url)
elif mode==3:
    TVSHOW(url)
elif mode==4:
    EPISODE(url)
elif mode==5:
    EPISODE_DIRECT(url)
elif mode==6:
    EPISODE_YOUTUBE(url)
elif mode==7:
    EPISODE_PARAM(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
