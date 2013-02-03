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
_L = __addon__.getLocalizedString

xbmc.log( "[PLUGIN] '%s: initialized!" % __addon__.getAddonInfo('name'), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join(__cwd__, 'resources', 'lib') )
if not LIB_DIR in sys.path:
  sys.path.append (LIB_DIR)
image_dir = xbmc.translatePath( os.path.join(__cwd__,'resources','images')+os.sep )
tvpot_icon = image_dir+"daum_tvpot.png"

prevPage = u"[B]<{0:s}[/B]".format(_L(30000))
nextPage = u"[B]{0:s}>[/B]".format(_L(30001))

# show menu
def CATEGORIES():
  addDir(u"영화 예고편", "http://movie.daum.net/ranking/movieclip_ranking/", 10, image_dir+"daum_trailer.png")
  addDir(u"뉴스", "http://media.daum.net/tv/", 20, image_dir+"daum_media.png")
  addDir(u"베스트 동영상", "http://tvpot.daum.net/best/", 30, tvpot_icon)
  addDir(u"브랜드", "_1", 40, tvpot_icon)
  addDir(u"키즈짱", "http://kids.daum.net", 50, tvpot_icon)
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

def CAT_BRAND_TOP(url,contPage):
  page = int(url[1:])
  from daum_brand import DaumBrand
  site=DaumBrand()
  site.parseList(page)
  for title,ownerid,thumb in site.menu_list:
    addDir(title, ownerid, 42, thumb)
  if site.prevpage:
    addDir(prevPage, "_%d"% (page-1), 41, '')
  if site.nextpage:
    addDir(nextPage, "_%d"% (page+1), 41, '')
  endDir(contPage)

def CAT_BRAND(ownerid):
  from daum_brand import DaumBrand
  site=DaumBrand()
  site.parseTop(ownerid)
  for title, playlistid, thumb in site.menu_list:
    if playlistid:
      addDir(title, "%s-%d-1"% (ownerid, playlistid), 43, thumb)
    else:
      addDir(u"[COLOR FFFF0000]%s[/COLOR]"% title,'',0,thumb)
  endDir()

def CAT_KIDS(base_url):
  addDir(u"팡팡동영상", "http://infant.kids.daum.net/vod",51,'')
  endDir()

def CAT_KIDS_VOD(main_url):
  from daum_kids import DaumKids
  site = DaumKids()
  site.parseTop(main_url)
  for title,url,thumb in site.menu_list:
    if url.find('categoryId=') > 0:
      addDir(title, url, 53, thumb)
    else:
      addDir(title, url, 52, thumb)
  endDir()

def CAT_KIDS_SERIES(main_url):
  from daum_kids import DaumKids
  site = DaumKids()
  site.parseSeries(main_url)
  for title,url,thumb in site.menu_list:
    addDir(title, url, 53, thumb)
  endDir()

#------------------------------------------------------------------
def BROWSE_TRAILER(main_url):
  from daum_trailer import DaumTrailer
  site=DaumTrailer()
  site.parse(main_url)
  for title,url,thumb in site.video_list:
    addDir(title, url, 1002, thumb)
  endDir()

def BROWSE_NEWS(main_url,contPage):
  from daum_news import DaumNews
  site=DaumNews()
  site.parse(main_url)
  for title,vid,thumb in site.video_list:
    title = title.replace('&#39;',"'")
    addDir(title, vid, 1000, thumb)
  if site.prevpage:
    addDir(prevPage, site.prevpage, 22, '')
  if site.nextpage:
    addDir(nextPage, site.nextpage, 22, '')
  endDir(contPage)

def BROWSE_BEST(main_url, contPage):
  from daum_best import DaumBestClip
  site=DaumBestClip()
  site.parse(main_url)
  for title,url,thumb in site.video_list:
    title = title.replace('\n'," ")
    addDir(title, url, 1001, thumb)
  if site.prevpage:
    addDir(prevPage, site.prevpage, 32, '')
  if site.nextpage:
    addDir(nextPage, site.nextpage, 32, '')
  endDir(contPage)

def BROWSE_BRAND(plst,contPage):
  ownerid,plstr,pgstr = re.compile("(.+?)-(\d+)-(\d+)").match(plst).group(1,2,3)
  playlistid = int(plstr)
  page = int(pgstr)

  from daum_brand import DaumBrand
  site=DaumBrand()
  site.parse(ownerid,playlistid,page)
  for title,vid,thumb in site.video_list:
    addDir(title, vid, 1000, thumb)
  if site.prevpage:
    addDir(prevPage, "%s-%d-%d"% (ownerid,playlistid,page-1), 44, '')
  if site.nextpage:
    addDir(nextPage, "%s-%d-%d"% (ownerid,playlistid,page+1), 44, '')
  endDir(contPage)

def BROWSE_KIDS(main_url,contPage):
  from daum_kids import DaumKids
  site = DaumKids()
  site.parse(main_url)
  for title,url,thumb in site.menu_list:
    addDir('[COLOR FFFF0000]%s[/COLOR]'% title, url, 53, thumb)
  for title,url,thumb in site.video_list:
    addDir(title, url, 1003, thumb)
  if site.prevpage:
    addDir(prevPage, site.prevpage, 54, '')
  if site.nextpage:
    addDir(nextPage, site.nextpage, 54, '')
  endDir(contPage)

#--------------------------------------------------------------------
def PLAY_VID(vid, title):
  from getdaumvid import DaumGetFlvByVid2
  vid_url = DaumGetFlvByVid2(None, vid)
  print "daum vid=%s url=%s" % (vid, vid_url)

  li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
  li.setInfo('video', {"Title": title})
  xbmc.Player().play(vid_url, li)

def PLAY_CLIP(main_url):
  clipid = re.compile('clipid=(\d*)').search(main_url).group(1)
  from getdaumvid import DaumGetClipInfo
  title,vid,thumb = DaumGetClipInfo(int(clipid))
  if vid:
    from getdaumvid import DaumGetFlvByVid2
    vid_url = DaumGetFlvByVid2(None, vid)
    print "daum vid=%s url=%s" % (vid, vid_url)
    if not thumb:
      thumb = "DefaultVideo.png"
    li = xbmcgui.ListItem(title, iconImage=thumb)
    li.setInfo('video', {"Title": title})
    xbmc.Player().play(vid_url, li)
  else:
    xbmcgui.Dialog().ok("No info on clip, ", clipid)

def PLAY_SITE(main_url, title):
  import getdaumvid
  urls = getdaumvid.parse(main_url)
  if len(urls) > 0:
    li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": title})
    xbmc.Player().play(urls[0], li)
  else:
    xbmcgui.Dialog().ok("No video found")

def PLAY_KIDS_VOD(main_url, title):
  from daum_kids import DaumKids
  site = DaumKids()
  vid = site.extract_video_id(main_url)
  from getdaumvid import DaumGetFlvByVid2
  vid_url = DaumGetFlvByVid2(None, vid)
  print "daum vid=%s url=%s" % (vid, vid_url)

  li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
  li.setInfo('video', {"Title": title})
  xbmc.Player().play(vid_url, li)

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
elif mode==40 or mode==41:
  CAT_BRAND_TOP(url,mode==41)
elif mode==42:
  CAT_BRAND(url)
elif mode==43 or mode==44:
  BROWSE_BRAND(url,mode==44)
# kids jjang
elif mode==50:
  CAT_KIDS(url)
elif mode==51:
  CAT_KIDS_VOD(url)
elif mode==52:
  CAT_KIDS_SERIES(url)
elif mode==53 or mode==54:
  BROWSE_KIDS(url,mode==54)
# play
elif mode==1000:
  PLAY_VID(url,name)
elif mode==1001:
  PLAY_CLIP(url)
elif mode==1002:
  PLAY_SITE(url,name)
elif mode==1003:
  PLAY_KIDS_VOD(url,name)

# vim: softtabstop=2 shiftwidth=2 expandtab
