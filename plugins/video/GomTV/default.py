# coding=utf-8
"""
  GomTV - Music Video
"""

import urllib,xbmcplugin,xbmcgui
import re

# plugin constants
__plugin__ = "GomTV"
__pluginid__ = "plugin.video.gomtv.com"
__url__ = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/GomTV"
__credits__ = "XBMC Korean User Group"
__version__ = "0.4.3"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)

#__settings__ = xbmc.Settings( id=__pluginid__ ) 
__settings__ = xbmc.Settings( path=os.getcwd() ) 
__hq_first__ = __settings__.getSetting( "HQVideo" )=="true"
__movie_backdoor__ = __settings__.getSetting( "MovieBackdoor" )=="true"

menu_div = u"----------------------------------------------------"

CHSET_FILE = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'gomtv.xml' ) )
import xml.dom.minidom as xml
chset = xml.parse( CHSET_FILE )

from BeautifulSoup import BeautifulSoup, SoupStrainer
from GomTvLib import GomTvLib

#-----------------------------------------------------
def CATEGORIES():
    addDir(u"시청순위","-",13,"")
    addDir(u"영화/드라마","-",18,"")
    addDir(u"뮤직","-",15,"")
    addDir(u"게임","-",12,"")
    addDir(u"연예/오락","-",16,"")
    addDir(u"뉴스/정보","-",17,"")
    addDir(u"[설정]","-",100,"")

def CAT_MUSIC_CHART(main_url):
    mchart_url = "http://www.gomtv.com/chart/index.gom?chart=%d"
    addDir(u"실시간",mchart_url % 1,4,"")
    addDir(u"주간",mchart_url % 3,4,"")
    addDir(u"월간",mchart_url % 4,4,"")
    addDir(u"주간1위모음",mchart_url % 6,4,"")
    addDir(u"명예의전당",mchart_url % 5,4,"")

def CAT_GAME(main_url):
    thisch = chset and chset.getElementsByTagName('game')[0]
    favorites = thisch.getElementsByTagName('favorite')
    for subch in favorites:
    	name = subch.getElementsByTagName('name')[0].childNodes[0].data
    	number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    if favorites:
        addDir(menu_div,"",12,"")
    for ch in thisch.getElementsByTagName('channel'):
    	name = ch.getElementsByTagName('name')[0].childNodes[0].data
    	number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

def CAT_MUSIC(main_url):
    addDir(u"뮤직비디오 차트","-",11,"")
    thisch = chset and chset.getElementsByTagName('music')[0]
    for subch in thisch.getElementsByTagName('favorite'):
    	name = subch.getElementsByTagName('name')[0].childNodes[0].data
    	number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    addDir(menu_div,"",15,"")
    for ch in thisch.getElementsByTagName('channel'):
    	name = ch.getElementsByTagName('name')[0].childNodes[0].data
    	number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

def CAT_ETMNT(main_url):
    thisch = chset and chset.getElementsByTagName('entertainment')[0]
    favorites = thisch.getElementsByTagName('favorite')
    for subch in favorites:
    	name = subch.getElementsByTagName('name')[0].childNodes[0].data
    	number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    if favorites:
        addDir(menu_div,"",16,"")
    for ch in thisch.getElementsByTagName('channel'):
    	name = ch.getElementsByTagName('name')[0].childNodes[0].data
    	number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

def CAT_INFO(main_url):
    thisch = chset and chset.getElementsByTagName('information')[0]
    favorites = thisch.getElementsByTagName('favorite')
    for subch in favorites:
    	name = subch.getElementsByTagName('name')[0].childNodes[0].data
    	number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    if favorites:
        addDir(menu_div,"",17,"")
    for ch in thisch.getElementsByTagName('channel'):
    	name = ch.getElementsByTagName('name')[0].childNodes[0].data
    	number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

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
	addDir(ref.contents[0], "http://www.gomtv.com"+ref['href'], 3, "")

def CAT_PREMIER_LIST(main_url):
    mvlist_url = "http://movie.gomtv.com/list.gom?cateid=%d"
    addDir(u"현재 상영작",mvlist_url % 65,5,"")
    addDir(u"개봉 예정작",mvlist_url % 66,5,"")
    addDir(u"개봉 미정작",mvlist_url % 67,5,"")

def CAT_MOVIE_HOTCLIP(main_url):
    hot_url = "http://movie.gomtv.com/release/hotclip.gom"
    addDir(u"전체보기",hot_url,6,"")
    addDir(u"본예고",hot_url+"?flag=3000",6,"")
    addDir(u"티저예고",hot_url+"?flag=3500",6,"")
    addDir(u"메이킹",hot_url+"?flag=3100",6,"")
    addDir(u"M/V",hot_url+"?flag=3200",6,"")
    addDir(u"인터뷰",hot_url+"?flag=3600",6,"")

def CAT_MOVIE(main_url):
    addDir(u"무료영화","http://movie.gomtv.com/list.gom?cateid=4",7,"")
    addDir(u"무료드라마","http://movie.gomtv.com/list.gom?cateid=189",7,"")
    addDir(u"에니메이션","http://movie.gomtv.com/list.gom?cateid=44",7,"")
    addDir(u"극장개봉정보","-",19,"")
    addDir(u"박스오피스","http://movie.gomtv.com/release/boxoffice.gom",8,"")
    addDir(u"핫클립","-",20,"")

    thisch = chset and chset.getElementsByTagName('movie')[0]
    for subch in thisch.getElementsByTagName('favorite'):
    	name = subch.getElementsByTagName('name')[0].childNodes[0].data
    	number = subch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,2,"")
    channels = thisch.getElementsByTagName('channel')
    if channels:
        addDir(menu_div,"",18,"")
    for ch in channels:
    	name = ch.getElementsByTagName('name')[0].childNodes[0].data
    	number = ch.getElementsByTagName('number')[0].childNodes[0].data
        addDir(name,"http://ch.gomtv.com/"+number,1,"")

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

def MOVIE_LIST(main_url):
    if main_url.endswith("cateid=44") or main_url.endswith("cateid=189"):
	child_fid = 7	    # sub table
    else:
	child_fid = 10	    # movie page
    resp=urllib.urlopen(main_url)
    strain = SoupStrainer( "div", { "id" : "sub_center" } )
    soup = BeautifulSoup( resp.read(), strain, fromEncoding="euc-kr" )
    #-- item list
    strain = SoupStrainer( "div", { "id" : "program_poster" } )
    for item in soup.find(strain).findAll("div", {"class" : "poster"}):
	refs = item.findAll('a')
	thumb = refs[0].find('img')['src']
	url = refs[1]['href']
	if url.startswith('/'):
	    url="http://movie.gomtv.com"+url
	title = refs[1].string
	addDir(title,url,child_fid,thumb)
    #-- next page
    strain = SoupStrainer( "div", { "id" : "page" } )
    nextpage = soup.find(strain).find('span').findNextSibling('a')
    if nextpage:
	addDir(u'다음 페이지>', "http://movie.gomtv.com"+nextpage['href'], 7, '')
    
def PREMIER_LIST(main_url):
    resp=urllib.urlopen(main_url)
    strain = SoupStrainer( "div", { "id" : "sub_center2" } )
    soup = BeautifulSoup( resp.read(), strain, fromEncoding="euc-kr" )
    #-- item list
    strain = SoupStrainer( "div", { "id" : "theater_poster" } )
    for item in soup.find(strain).findAll("div", {"class" : "poster"}):
	refs = item.findAll('a')
	thumb = refs[0].find('img')['src']
	url = refs[1]['href']
	title = refs[1].string
	addDir(title,url,10,thumb)
    #-- next page
    strain = SoupStrainer( "div", { "id" : "page" } )
    nextpage = soup.find(strain).find('span').findNextSibling('a')
    if nextpage:
	addDir(u'다음 페이지>', "http://movie.gomtv.com"+nextpage['href'], 5, '')
    
def MOVIE_HOTCLIP(main_url):
    link=urllib.urlopen(main_url)
    strain = SoupStrainer( "div", { "id" : "sub_center2" } )
    soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
    #-- item list
    strain = SoupStrainer( "div", { "id" : "hotClip_list" } )
    for item in soup.find(strain).findAll('dl'):
	refs = item.findAll('a')
	thumb = refs[0].find('img')['src']
	url = "http://tv.gomtv.com/cgi-bin/gox/gox_clip.cgi?dispid=%s&clipid=%s" % re.compile('/(\d+)/\d+/\d+/(\d+)').search( refs[1]['onclick'] ).group(1,2)
	title = refs[1].find('b').string
	addDir(title,url,9,thumb)
    #-- next page
    strain = SoupStrainer( "div", { "id" : "page" } )
    nextpage = soup.find(strain).find('span').findNextSibling('a')
    if nextpage:
	addDir(u'다음 페이지>', "http://movie.gomtv.com"+nextpage['href'], 6, '')
    
def MOVIE_BOXOFFICE(main_url):
    link=urllib.urlopen(main_url)
    strain = SoupStrainer( "div", { "id" : "boxOffice_poster" } )
    soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
    #-- item list
    strain = SoupStrainer( "div", { "class" : "poster" } )
    for item in soup.findAll(strain):
	refs = item.findAll('a')
	thumb = refs[0].find('img')['src']
	url = refs[0]['href']
	title = refs[1].string
	addDir(title,url,10,thumb)
    
#-----------------------------------                
def GOM_CLIP(main_url):
    vid_url = GomTvLib().GetVideoUrl(main_url)
    xbmc.log( "clip_url=%s"%vid_url, xbmc.LOGDEBUG )
    addLink(u"시청", vid_url, '')

def GOM_VIDEO(main_url):
    gom = GomTvLib()
    if main_url.startswith('http://movie.gomtv.com'):
	print "VIDEO: %s" % main_url
	gom.ParseMoviePage(main_url)
        match = re.compile('http://movie.gomtv.com/(\d+)/(\d+)').match(main_url)
        if __movie_backdoor__ and match:
            (dispid,vodid) = match.group(1,2)
	else:
	    (dispid,vodid) = (gom.dispid, gom.vodid)
	print "dispid=%s / vodid=%s" % (dispid,vodid)
	# free movie
	mov_list = gom.GetMovieUrls(dispid,vodid)
	for title,url in mov_list:
	    addDir(title, url, 9, '')
	# hotclip
	hc_ids = gom.GetHotclipIds():
	if mov_list and hc_ids:
	    addDir(menu_div, "", 10, '')    # divider
	for clipid,title,thumb in hc_ids:
	    st_url = "http://tv.gomtv.com/cgi-bin/gox/gox_clip.cgi?dispid=%s&clipid=%s" % (dispid,clipid)
	    addDir(title, st_url, 9, thumb)
    elif main_url.startswith('http://tv.gomtv.com') or main_url.startswith('http://ch.gomtv.com'):
	print "TV: %s" % main_url
	gom.useHQFirst(__hq_first__)
	gom.ParseChVideoPage(main_url)
	for bjvid,title in gom.sub_list:
	    st_url = "http://tv.gomtv.com/cgi-bin/gox/gox_channel.cgi?isweb=0&chid=%s&pid=%s&bid=%s&bjvid=%s" % (gom.chid,gom.pid,gom.bid,bjvid)
	    addDir(title, st_url, 9, '')
    else:
	print "ERROR: %s is not considered" % main_url

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
elif mode==5:
    PREMIER_LIST(url)
elif mode==6:
    MOVIE_HOTCLIP(url)
elif mode==7:
    MOVIE_LIST(url)
elif mode==8:
    MOVIE_BOXOFFICE(url)
elif mode==9:
    GOM_CLIP(url)
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
    CAT_INFO(url)
elif mode==18:
    CAT_MOVIE(url)
elif mode==19:
    CAT_PREMIER_LIST(url)
elif mode==20:
    CAT_MOVIE_HOTCLIP(url)
elif mode==100:
    __settings__.openSettings()
    __hq_first__ = __settings__.getSetting( "HQVideo" )=="true"

xbmcplugin.endOfDirectory(int(sys.argv[1]))
