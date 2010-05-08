# coding=utf-8
"""
  GomTV - Music Video
"""

import urllib,xbmcplugin,xbmcgui

# plugin constants
__plugin__  = "GomTV"
__author__  = "edge"
__url__     = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/GomTV"
__credits__ = "XBMC Korean User Group"
__version__ = "0.0.2"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
if not LIB_DIR in sys.path:
    sys.path.append (LIB_DIR)

from BeautifulSoup import BeautifulSoup, SoupStrainer

#-----------------------------------------------------
def CATEGORIES():
    addDir(u"뮤직비디오 차트","dummy",11,"")
    addDir(u"게임","dummy",12,"")

def CAT_MUSIC_CHART(main_url):
    addDir(u"실시간","http://www.gomtv.com/chart/index.gom?chart=1",1,"")
    addDir(u"주간","http://www.gomtv.com/chart/index.gom?chart=3",1,"")
    addDir(u"월간","http://www.gomtv.com/chart/index.gom?chart=4",1,"")
    addDir(u"주간1위모음","http://www.gomtv.com/chart/index.gom?chart=6",1,"")
    addDir(u"명예의전당","http://www.gomtv.com/chart/index.gom?chart=5",1,"")

def CAT_GAME(main_url):
    addDir(u"스타크래프트2 XP토너먼트","http://ch.gomtv.com/4002/27523",2,"")
    addDir(u"Star2gether","http://ch.gomtv.com/425/27635",2,"")
    addDir(u"[4R]프로리그 09-10","http://ch.gomtv.com/412/27633",2,"")
    addDir(u"[2R]프로리그 09-10","http://ch.gomtv.com/412/27713",2,"")
    addDir(u"[1R]프로리그 09-10","http://ch.gomtv.com/412/27607",2,"")

#-----------------------------------------------------
def MUSIC_CHART(main_url):
    link=urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="euc-kr" )
    #-- item list
    strain = SoupStrainer( "table", { "id" : "neo_wchart_list" } )
    list = soup.find(strain).findAll('a')
    while len(list) > 2:
	ref = list.pop(0)
	url = ref['href']
	thumb = ref.find('img')['src']
	ref = list.pop(0)
	while ref.find('img'):
	    ref = list.pop(0)
	title = ref.contents[0]
	list.pop(0)
	addDir(title,url,10,thumb)
    #-- next page
    strain = SoupStrainer( "div", { "class" : "neo_wchart_index" } )
    #print soup.find(strain).find(lambda tag: tag.name=='a' and len(tag.attrs)==2)
    list = soup.find(strain).findAll('a')
    while list:
	ref = list.pop(0)
	if ('class','cho_on') in ref.attrs and list:
	    ref = list.pop(0)
	    addDir(u'다음 페이지>', "http://www.gomtv.com"+ref['href'], 1, '')
	    break
    
def STAR2_CH(main_url):
    link=urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="euc-kr" )
    #-- item list
    strain1 = SoupStrainer( "table", { "id" : "program_text_list" } )
    strain2 = SoupStrainer( "dl", { "class" : "text_list" } )
    list1 = soup.find(strain1).findAll(strain2)
    for item in list1:
	refs = item.findAll('a')
	url = refs[0]['href']
	thumb = refs[0].find('img')['src']
	title = refs[1].contents[0]
	addDir(title,url,10,thumb)
    #-- next page
    strain = SoupStrainer( "table", { "class" : "page" } )
    import re
    curpg = soup.find(strain).find("td", {"class" : re.compile("^on")})
    if curpg and curpg['class'] != "on last":
	url = curpg.findNextSibling('td').find('a')['href']
	addDir(u'다음 페이지>', url, 2, '')

def SHOW_VIDEO(main_url):
    ids = GetGomId(main_url)
    if ids:
	st_url = "http://tv.gomtv.com/cgi-bin/gox/gox_channel.cgi?isweb=0&chid=%s&pid=%s&bid=%s&bjvid=%s" % ids
	vid_url = GetVideoUrl(st_url)
	if vid_url:
	    addLink(u"시청", vid_url, '')

def GetGomId(main_url):
    try:
	tDoc=urllib.urlopen(main_url).read()
    except:
	return None
    
    pos1 = tDoc.find('obj.useNoneImg')
    pos2 = tDoc.find('if(isFirst)',pos1)
    if pos1 < 0 or pos2 < 0:
	return None
    list = tDoc[pos1:pos2].split(';')
    ids = []
    # order is chid,pid,bjvid,bid
    for stmt in list[1:]:
	ids.append( stmt[stmt.rfind("'",0,-1)+1:-1] )
    return (ids[0],ids[1],ids[3],ids[2])

def GetVideoUrl(main_url):
    xbmc.log( "vidurl=%s"%main_url, xbmc.LOGDEBUG )
    try:
	link=urllib.urlopen(main_url)
    except:
	return None
    
    soup = BeautifulSoup( link.read(), fromEncoding="euc-kr" )
    list = soup.findAll('ref')
    for ref in list:
	url = ref['href']
	if url[7:url.find('.',7)].isdigit():
	    return url.replace('&amp;','&')
    return ''

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
    MUSIC_CHART(url)
elif mode==2:
    STAR2_CH(url)
elif mode==10:
    SHOW_VIDEO(url)
elif mode==11:
    CAT_MUSIC_CHART(url)
elif mode==12:
    CAT_GAME(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
