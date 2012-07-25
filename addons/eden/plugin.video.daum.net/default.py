# -*- coding: utf-8 -*-
"""
  Movie clip from Daum
"""
import urllib, re
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.daum.net"
__addon__   = xbmcaddon.Addon(__addonid__)
__cwd__     = __addon__.getAddonInfo('path')

xbmc.log( "[PLUGIN] '%s: initialized!" % __addon__.getAddonInfo('name'), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join(__cwd__, 'resources', 'lib') )
if not LIB_DIR in sys.path:
  sys.path.append (LIB_DIR)
pic_dir = xbmc.translatePath( os.path.join(__cwd__,'resources','pic')+os.sep )
tvpot_icon = pic_dir+"daum_tvpot.png"

# show menu
def CATEGORIES():
  addDir(u"영화 예고편", "http://movie.daum.net/ranking/movieclip_ranking/", 10, pic_dir+"daum_trailer.png")
  addDir(u"뉴스", "http://media.daum.net/tv/", 20, pic_dir+"daum_media.png")
  addDir(u"베스트 동영상", "http://tvpot.daum.net/best/", 30, tvpot_icon)
  addDir(u"브랜드", "http://tvpot.daum.net/brand/", 40, tvpot_icon)
  addDir(u"게임", "http://tvpot.daum.net", 50, tvpot_icon)
  endDir()

def CAT_TRAILER(base_url):
  addDir(u"일간 베스트",base_url+"bestTrailer.do?datekey=3",11,'')
  addDir(u"주간 베스트",base_url+"bestTrailer.do?datekey=2",11,'')
  addDir(u"월간 베스트",base_url+"bestTrailer.do?datekey=1",11,'')
  endDir()

def CAT_NEWS(url):
  from daum_news import DaumNews
  site=DaumNews()
  site.parseTop(url)
  for title,url in site.menu_list:
    addDir(title,url,21,'')
  endDir()

def CAT_BEST(base_url):
  addDir(u"전체/ 기간:전체/ 플레이:전체/ 인기순 ", base_url+"TotalBest.do?cateid=&dateterm=all&playterm=all&sort=play",31,'')
  addDir(u"전체/ 기간:전체/ 플레이:전체/ 최신순 ", base_url+"TotalBest.do?cateid=&dateterm=all&playterm=all&sort=wtime",31,'')
  addDir(u"전체/ 기간:1주/ 플레이:전체/ 인기순 ", base_url+"TotalBest.do?cateid=&dateterm=week&playterm=all&sort=play",31,'')
  addDir(u"전체/ 기간:전체/ 플레이:50만/ 인기순 ", base_url+"TotalBest.do?cateid=&dateterm=all&playterm=50M&sort=play",31,'')
  addDir(u"연예/ 인기순 ", base_url+"TotalBest.do?cateid=22&sort=play",31,'')
  endDir()

def CAT_BRAND_TOP(base_url):
  from daum_brand import DaumBrand
  for title,bid in DaumBrand.getList(base_url):
    if bid:
      url = base_url + "Top.do?ownerid=" + bid
      addDir(title,url,41,'')
    else:
      addDir(title,'',40,'')
  endDir()

def CAT_BRAND(url):
  from daum_brand import DaumBrand
  site=DaumBrand()
  site.parseTop(url)
  for title,url in site.menu_list:
    addDir(title,url,42,'')
  endDir()

def CAT_GAME(base_url):
  addDir(u"스타리그", base_url+"/game/sl/LeagueList.do?league=osl&type=list&lu=game_osl_closegame",51,pic_dir+"oslBanner.png")
  addDir(u"프로리그", base_url+"/game/sl/LeagueList.do?league=pro&type=list&lu=game_pro_closegame",51,pic_dir+"proleagueBanner.png")
  addDir(u"MSL", base_url+"/game/sl/LeagueList.do?league=msl&type=list&lu=game_msl_closegame",51,"")
  endDir()

def CAT_STARCRAFT(main_url):
  from daum_starcraft import DaumStarcraft
  site = DaumStarcraft()
  site.parseTop(main_url)
  for title,url in site.menu_list:
    addDir(title, url, 52, '')
  endDir()

#------------------------------------------------------------------
def BROWSE_TRAILER(main_url):
  from daum_trailer import DaumTrailer
  site=DaumTrailer()
  site.parse(main_url)
  for title,url,thumb in site.video_list:
    addDir(title, url, 1000, thumb)
  endDir()

def BROWSE_NEWS(main_url,contPage):
  from daum_news import DaumNews
  site=DaumNews()
  site.parse(main_url)
  for title,url,thumb in site.video_list:
    title = title.replace('&#39;',"'")
    addDir(title, url, 1001, thumb)
  if site.prevpage:
    addDir(u"<이전 페이지", site.prevpage, 22, '')
  if site.nextpage:
    addDir(u"다음 페이지>", site.nextpage, 22, '')
  endDir(contPage)

def BROWSE_BEST(main_url, contPage):
  from daum_best import DaumBestClip
  site=DaumBestClip()
  site.parse(main_url)
  for title,url,thumb in site.video_list:
    title = title.replace('\n'," ")
    addDir(title, url, 1000, thumb)
  if site.prevpage:
    addDir(u"<이전 페이지", site.prevpage, 32, '')
  if site.nextpage:
    addDir(u"다음 페이지>", site.nextpage, 32, '')
  endDir(contPage)

def BROWSE_BRAND(main_url,contPage):
  from daum_brand import DaumBrand
  site=DaumBrand()
  site.parse(main_url)
  for title,url,thumb in site.video_list:
    title = title.replace('\n'," ")
    addDir(title, url, 1000, thumb)
  if site.prevpage:
    addDir(u"<이전 페이지", site.prevpage, 43, '')
  if site.nextpage:
    addDir(u"다음 페이지>", site.nextpage, 43, '')
  endDir(contPage)

def BROWSE_STARCRAFT(main_url, contPage):
  from daum_starcraft import DaumStarcraft
  site=DaumStarcraft()
  site.parse(main_url)
  for date,cable,mtitle,set_list in site.video_list:
    addDir("[COLOR FFFF0000]%s(%s) %s[/COLOR]" % (date,cable,mtitle), '', 53, '')
    for sname,stitle,url in set_list:
      addDir("%s %s" % (sname,stitle), url, 1000, '')
  if site.prevpage:
    addDir(u"<이전 페이지", site.prevpage, 53, '')
  if site.nextpage:
    addDir(u"다음 페이지>", site.nextpage, 53, '')
  endDir(contPage)

#--------------------------------------------------------------------
def PLAY_SWFURL(main_url, title):
  from getdaumvid import GetDaumVideo
  vid = re.compile('vid=([^&]*)').search(main_url).group(1)
  vid_url = GetDaumVideo.DaumGetFlvByVid(None, vid)

  li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
  li.setInfo('video', {"Title": title})
  xbmc.Player().play(vid_url, li)

def PLAY_CLIP(main_url, title):
  from getdaumvid import GetDaumVideo
  urls = GetDaumVideo.parse(main_url)
  if len(urls):
    li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": title})
    xbmc.Player().play(urls[0], li)
  else:
    xbmcgui.Dialog().ok("Can not find video", main_url)

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
  try: xbmc.log( "addLink(%s,%s)" % (name, url), xbmc.LOGDEBUG )
  except: pass
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

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

xbmc.log( "Mode: "+str(mode), xbmc.LOGINFO )
xbmc.log( "URL : "+str(url), xbmc.LOGINFO )
xbmc.log( "Name: "+str(name), xbmc.LOGINFO )

if mode==None:
  CATEGORIES()
# movie trailer
elif mode==10:
  CAT_TRAILER(url)
elif mode==11:
  BROWSE_TRAILER(url)
# news clip
elif mode==20:
  CAT_NEWS(url)
elif mode==21 or mode==22:
  BROWSE_NEWS(url,mode==22)
# best clip
elif mode==30:
  CAT_BEST(url)
elif mode==31 or mode==32:
  BROWSE_BEST(url,mode==32)
# brands
elif mode==40:
  CAT_BRAND_TOP(url)
elif mode==41:
  CAT_BRAND(url)
elif mode==42 or mode==43:
  BROWSE_BRAND(url,mode==43)
# game broadcast
elif mode==50:
  CAT_GAME(url)
elif mode==51:
  CAT_STARCRAFT(url)
elif mode==52 or mode==53:
  BROWSE_STARCRAFT(url,mode==53)
# play
elif mode==1000:
  PLAY_CLIP(url,name)
elif mode==1001:
  PLAY_SWFURL(url,name)

# vim: softtabstop=2 shiftwidth=2 expandtab
