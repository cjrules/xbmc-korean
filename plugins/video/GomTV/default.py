# coding=utf-8
"""
  GomTV - Music Video
"""

import urllib,xbmcplugin,xbmcgui
import re

# plugin constants
__plugin__  = "GomTV"
__author__  = "anonymous"
__url__     = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/GomTV"
__credits__ = "XBMC Korean User Group"
__version__ = "0.3.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)

__settings__ = xbmc.Settings( path=os.getcwd() ) 
hq_first = __settings__.getSetting( "HQVideo" )=="true"
menu_div = u"------------------------------------------------"

from BeautifulSoup import BeautifulSoup, SoupStrainer

#-----------------------------------------------------
def CATEGORIES():
    addDir(u"시청순위","-",13,"")
    addDir(u"뮤직비디오 차트","-",11,"")
    addDir(u"뮤직","-",15,"")
    addDir(u"게임","-",12,"")
    addDir(u"연예/오락","-",16,"")
    addDir(u"교육","-",17,"")
    addDir(u"[설정]","-",100,"")

def CAT_MUSIC_CHART(main_url):
    mchart_url = "http://www.gomtv.com/chart/index.gom?chart=%d"
    addDir(u"실시간",mchart_url % 1,3,"")
    addDir(u"주간",mchart_url % 3,3,"")
    addDir(u"월간",mchart_url % 4,3,"")
    addDir(u"주간1위모음",mchart_url % 6,3,"")
    addDir(u"명예의전당",mchart_url % 5,3,"")

def CAT_GAME(main_url):
    addDir(u"스타크래프트2 XP토너먼트","http://ch.gomtv.com/4002/27523",2,"")
    addDir(u"Star2gether","http://ch.gomtv.com/425/27635",2,"")
    addDir(u"[4R]프로리그 09-10","http://ch.gomtv.com/412/27633",2,"")
    addDir(u"특별기획-스타2G","http://ch.gomtv.com/439/27503",2,"")
    addDir(u"곰게임넷","http://ch.gomtv.com/439/24776",2,"")
    addDir(menu_div,"",2,"")
    addDir(u"곰게임넷","http://ch.gomtv.com/439",1,"")
    addDir(u"겜플렉스","http://ch.gomtv.com/4002",1,"")
    addDir(u"신한은행 프로리그 09-10","http://ch.gomtv.com/412",1,"")

def CAT_MUSIC(main_url):
    addDir(u"YG TV","http://ch.gomtv.com/707",1,"")
    addDir(u"DSP Zone","http://ch.gomtv.com/2201",1,"")
    addDir(u"엠넷미디어","http://ch.gomtv.com/278",1,"")
    addDir(u"JYP 엔터테인먼트","http://ch.gomtv.com/206",1,"")
    addDir(u"FLUXUS Music","http://ch.gomtv.com/2002",1,"")

def CAT_ETMNT(main_url):
    addDir(u"ETN","http://ch.gomtv.com/7071",1,"")
    addDir(u"Q채널","http://ch.gomtv.com/710",1,"")

def CAT_EDU(main_url):
    addDir(u"동양문고 어학강좌","http://ch.gomtv.com/9110",1,"")

def CAT_HOT(main_url):
    link=urllib.urlopen( "http://www.gomtv.com/navigation/navigation.gom?navitype=3" )
    strain = SoupStrainer('ul', {"class" : "lnb_list"})
    soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
    for item in soup.findAll('li', {"class" : "mbin_list_1"}):
	ref = item.find('a')
	addDir(ref.contents[0], "http://www.gomtv.com"+ref['href'], 14, "")

def CAT_HOT_SUB(main_url):
    link=urllib.urlopen( main_url )
    strain = SoupStrainer('ul', {"id" : "tab_menu"})
    soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
    for item in soup.findAll('li'):
	ref = item.find('a')
	addDir(ref.contents[0], "http://www.gomtv.com"+ref['href'], 4, "")

#-----------------------------------------------------
def GOM_CH(main_url):
    link=urllib.urlopen(main_url)
    strain = SoupStrainer( "div", { "id" : "ch_menu" } )
    soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
    #-- channel menu
    for item in soup.findAll('p'):
	if item['class'] == 'mbin_tit':
	    if item.span and item.span.string:
		addDir("----- %s -----" % item.span.string, '', 1, '')
	elif item['class'] == 'mbin_list_s':
	    url = ''
	    for key,value in item.a.attrs:
		if key == 'href':
		    url = value
		    break
	    if re.compile('http://ch.gomtv.com/\d+/\d+').match(url):
		addDir(item.a.span.string, url, 2, '')

def GOM_CH_SUB(main_url):
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
	title = refs[1].contents[0].replace('&amp;','&')
	addDir(title,url,10,thumb)
    #-- next page
    strain = SoupStrainer( "table", { "class" : "page" } )
    import re
    curpg = soup.find(strain).find("td", {"class" : re.compile("^on")})
    if curpg and curpg['class'] != "on last":
	url = curpg.findNextSibling('td').find('a')['href']
	addDir(u'다음 페이지>', url, 2, '')

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
	title = ref.contents[0].replace('&amp;','&')
	list.pop(0)
	addDir(title,url,10,thumb)
    #-- next page
    strain = SoupStrainer( "div", { "class" : "neo_wchart_index" } )
    thispage = soup.find(strain).find('a', {"class" : "cho_on"})
    if thispage:
	nextpage = thispage.findNextSibling('a')
	if nextpage:
	    addDir(u'다음 페이지>', "http://www.gomtv.com"+nextpage['href'], 1, '')
    
def MOST_WATCHED(main_url):
    link=urllib.urlopen(main_url)
    soup = BeautifulSoup( link.read(), fromEncoding="euc-kr" )
    #-- item list
    for item in soup.findAll('dl', {"id" : "ranking_set"}):
	#title/url
	titblk = item.find('h6').find('a')
	title = titblk.string.replace('&amp;','&')
	url = titblk['href']
	#thumb
	thumb = ''
	img = item.find('a',{"href" : url}).find('img')
	if img: thumb = img['src']
	addDir(title,url,10,thumb)
    #-- next page
    strain1 = SoupStrainer( "table", { "class" : "down_page" } )
    strain2 = SoupStrainer( "td", { "class" : "on" } )
    nextpage = soup.find(strain1).find(strain2).findNextSibling('td')
    if nextpage is None: return
    for attr,value in nextpage.attrs:
	if attr == 'class' and value.endswith("nv"):
	    return
    addDir(u'다음 페이지>', "http://www.gomtv.com"+nextpage.find('a')['href'], 3, '')

#-----------------------------------                
def GOM_VIDEO(main_url):
    ids = GetGomId(main_url)
    if ids:
	(chid,pid,bid),sub_ids = ids
	for bjvid,title in sub_ids:
	    st_url = "http://tv.gomtv.com/cgi-bin/gox/gox_channel.cgi?isweb=0&chid=%s&pid=%s&bid=%s&bjvid=%s" % (chid,pid,bid,bjvid)
	    vid_url = GetVideoUrl(st_url)
	    if vid_url:
		addLink(title, vid_url, '')

def GetGomId(main_url):
    try:
	tDoc=urllib.urlopen(main_url).read()
    except:
	return None

    #-- chid/pid/bid
    query = re.compile('@brief add(.*?)\*/',re.S).search(tDoc)
    if query is None:
	print "%s is not allowed" % main_url
	return None
    tSec1 = query.group(1)
    chid,pid,bjvid,bid = re.compile("'(\d+)'").findall(tSec1)[:4]
    common_ids = (chid,pid,bid)

    #-- check playlist table
    sub_ids = []
    soup = BeautifulSoup( tDoc, fromEncoding="euc-kr" )
    if hq_first:
	plist = soup.find("ul", {"id" : "widgetTabs1"})	# HQ first
	if plist is None:
	    plist = soup.find("ul", {"id" : "widgetTabs2"})
    else:
	plist = soup.find("ul", {"id" : "widgetTabs2"})	# Std first
	if plist is None:
	    plist = soup.find("ul", {"id" : "widgetTabs1"})
    if plist:
	#-- bjvid from table
	for item in plist.findAll('a'):
	    ref = item['href']
	    id = ref[ref.rfind('(')+1:ref.rfind(',')]
	    title = item['title']
	    title = title[:title.find('\n')]
	    sub_ids.append( (id, title) )
    else:
	#-- bjvid for single
	match = re.compile('this\.arr(?:High|Low)Bjoinv\s*=\s*\[(\d+)\];').findall(tDoc)
	if len(match) != 2:
	    print "%s has unsupported format" % main_url
	    return None
	if hq_first: bjvid = match[0]
	else:        bjvid = match[1]
	sub_ids.append( (bjvid,u"시청") )	# single video
    return (common_ids, sub_ids)

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
    GOM_CH(url)
elif mode==2:
    GOM_CH_SUB(url)
elif mode==3:
    MOST_WATCHED(url)
elif mode==4:
    MUSIC_CHART(url)
elif mode==10:
    GOM_VIDEO(url)
elif mode==11:
    CAT_MUSIC_CHART(url)
elif mode==12:
    CAT_GAME(url)
elif mode==13:
    CAT_HOT(url)
elif mode==14:
    CAT_HOT_SUB(url)
elif mode==15:
    CAT_MUSIC(url)
elif mode==16:
    CAT_ETMNT(url)
elif mode==17:
    CAT_EDU(url)
elif mode==100:
    __settings__.openSettings()
    hq_first = __settings__.getSetting( "HQVideo" )=="true"

xbmcplugin.endOfDirectory(int(sys.argv[1]))
