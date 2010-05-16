# coding=utf-8
"""
  Movie clip from Daum
"""
import urllib,xbmcplugin,xbmcgui

# plugin constants
__plugin__  = "DaumTV"
__url__     = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/DaumTV"
__credits__ = "XBMC Korean User Group"
__version__ = "0.2.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
if not LIB_DIR in sys.path:
    sys.path.append (LIB_DIR)
pic_dir = xbmc.translatePath( os.path.join(os.getcwd(),'resources','pic')+os.sep )
tvpot_icon = pic_dir+"daum_tvpot.png"

CHSET_FILE = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'daumtv.xml' ) )
import xml.dom.minidom as xml
chset = xml.parse( CHSET_FILE )

# show menu
def CATEGORIES():
    addDir(u"영화 예고편", "http://movie.daum.net/ranking/movieclip_ranking/", 10, pic_dir+"daum_trailer.png")
    addDir(u"뉴스", "http://tvnews.media.daum.net/", 20, pic_dir+"daum_media.png")
    addDir(u"베스트 동영상", "http://tvpot.daum.net/best/", 30, tvpot_icon)
    addDir(u"브랜드", "http://tvpot.daum.net/brand/", 45, tvpot_icon)
    addDir(u"게임", "http://tvpot.daum.net", 40, tvpot_icon)
                       
def CAT_TRAILER(base_url):
    addDir(u"일간 베스트",base_url+"bestTrailer.do?datekey=3",11,'')
    addDir(u"주간 베스트",base_url+"bestTrailer.do?datekey=2",11,'')
    addDir(u"월간 베스트",base_url+"bestTrailer.do?datekey=1",11,'')

def CAT_NEWS(url):
    from daum_news import DaumNews
    site=DaumNews()
    site.parseTop(url)
    for title,url in site.menu_list:
        addDir(title,url,21,'')
                       
def CAT_BEST(base_url):
    addDir(u"일간 베스트", base_url+"BestToday.do?svctab=best&range=0",31,'')
    addDir(u"주간 베스트", base_url+"BestToday.do?svctab=best&range=1",31,'')
    addDir(u"월간 베스트", base_url+"BestToday.do?svctab=best&range=2",31,'')
    addDir(u"10만 플레이", base_url+"BestToday.do?svctab=10m",31,'')
                       
def CAT_GAME(base_url):
    addDir(u"스타리그", base_url+"/game/sl/LeagueList.do?league=osl&type=list&lu=game_osl_closegame",42,pic_dir+"oslBanner.png")
    addDir(u"프로리그", base_url+"/game/sl/LeagueList.do?league=pro&type=list&lu=game_pro_closegame",42,pic_dir+"proleagueBanner.png")
    addDir(u"겜플렉스 스타2", base_url+"/brand/ProgramView.do?ownerid=O_5rgf7M1do0&playlistid=1101578&page=1&viewtype=24",43,'')

def CAT_STARCRAFT(main_url):
    from daum_starcraft import DaumStarcraft
    site = DaumStarcraft()
    site.parseTop(main_url)
    for title,url in site.menu_list:
        addDir(title, url, 41, '')

def CAT_BRAND_TOP(base_url):
    for ch in chset.getElementsByTagName('brand'):
    	name = ch.getElementsByTagName('name')[0].childNodes[0].data
    	id = ch.getElementsByTagName('id')[0].childNodes[0].data
        addDir(name,base_url+"Top.do?ownerid="+id,44,"")

def CAT_BRAND(url):
    from daum_brand import DaumBrand
    site=DaumBrand()
    site.parseTop(url)
    for title,url in site.menu_list:
        addDir(title,url,43,'')

#------------------------------------------------------------------
def BROWSE_TRAILER(main_url):
    from daum_trailer import DaumTrailer
    site=DaumTrailer()
    site.parse(main_url)
    for title,url,thumb in site.video_list:
        addDir(title, url, 1, thumb)

def BROWSE_NEWS(main_url):
    from daum_news import DaumNews
    site=DaumNews()
    site.parse(main_url)
    for title,url,thumb in site.video_list:
	title = title.replace('&#39;',"'")
        addDir(title, url, 1, thumb)
    if site.nextpage:
        addDir(u"다음 페이지>", site.nextpage[1], 21, '')
    if site.prevday:
        addDir(site.prevday[0]+">", site.prevday[1], 21, '')

def BROWSE_BEST(main_url):
    from daum_best import DaumBestClip
    site=DaumBestClip()
    site.parse(main_url)
    for title,url,thumb in site.video_list:
	title = title.replace('\n'," ")
        addDir(title, url, 1, thumb)
    if site.nextpage:            
        addDir(u"다음 페이지>", site.nextpage[1], 31, '')

def BROWSE_STARCRAFT(main_url):
    from daum_starcraft import DaumStarcraft
    site=DaumStarcraft()
    site.parse(main_url)
    for date,cable,mtitle,set_list in site.video_list:
        addDir("---- %s(%s) %s ----" % (date,cable,mtitle), '', 41, '')
        for sname,stitle,url in set_list:
            addDir("%s %s" % (sname,stitle), url, 1, '')
    if site.nextpage:
        addDir(u"다음 페이지>", site.nextpage, 41, '')

def BROWSE_BRAND(main_url):
    from daum_brand import DaumBrand
    site=DaumBrand()
    site.parse(main_url)
    for title,url,thumb in site.video_list:
	title = title.replace('\n'," ")
        addDir(title, url, 1, thumb)
    if site.nextpage:            
        addDir(u"다음 페이지>", site.nextpage, 43, '')

def SHOW_VIDEO(main_url):
    from getdaumvid import GetDaumVideo
    vid_url = GetDaumVideo.parse(main_url)[0]
    addLink(u"시청", vid_url, '')

#--------------------------------------------------------------------                
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

xbmc.log( "Mode: "+str(mode), xbmc.LOGINFO )
xbmc.log( "URL : "+str(url), xbmc.LOGINFO )
xbmc.log( "Name: "+str(name), xbmc.LOGINFO )

if mode==None or url==None or len(url)<1:
    CATEGORIES()
elif mode==1:
    SHOW_VIDEO(url)
# movie trailer
elif mode==10:
    CAT_TRAILER(url)
elif mode==11:
    BROWSE_TRAILER(url)
# news clip
elif mode==20:
    CAT_NEWS(url)
elif mode==21:
    BROWSE_NEWS(url)
# best clip
elif mode==30:
    CAT_BEST(url)
elif mode==31:
    BROWSE_BEST(url)
# game broadcast
elif mode==40:
    CAT_GAME(url)
elif mode==41:
    BROWSE_STARCRAFT(url)
elif mode==42:
    CAT_STARCRAFT(url)
elif mode==43:
    BROWSE_BRAND(url)
elif mode==44:
    CAT_BRAND(url)
elif mode==45:
    CAT_BRAND_TOP(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
