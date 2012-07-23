# -*- coding: utf-8 -*-
"""
  Clip from NAVER
"""
import urllib
import xbmcplugin,xbmcgui
import re

# plugin constants
__plugin__  = "NAVER Video"
__addonID__ = "plugin.video.naver.com"
__url__     = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/addons/plugin.video.naver.com"
__credits__ = "XBMC Korean User Group"
__version__ = "0.0.1"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

# show menu
def CATEGORIES():
  addDir(u"뮤직비디오", "http://music.naver.com/video.nhn", 100, '')
  addDir(u"무비클립", "http://movie.naver.com/movie/running/movieclip.nhn", 110, '')
  addDir(u"프로야구 중계", "http://news.naver.com/sports/index.nhn?category=kbo&ctg=schedule", 120, '')

def CAT_MUSIC_VIDEO(base_url):
  addDir(u"최신 뮤직비디오",base_url+"?m=newest",101,'')
  addDir(u"인기 뮤직비디오",base_url+"?m=population",101,'')

def BROWSE_MUSIC_VIDEO(main_url):
  doc = urllib.urlopen(main_url).read()
  # video item
  for sect in doc.split('<span class="ln12">'):
     query = re.compile('''<span class="b2"><a href="javascript:goURL_videoDetail_key\('(\d+)'[^>]*>(.*?)</span>(.*?)</a>''').search(sect)
     if query:
       url = "http://music.naver.com/video.nhn?m=detail&mvid="+query.group(1)
       pos = sect.rfind("<img src=http")+9
       thumb = sect[ pos : sect.find('.jpg',pos)+4 ]
       title = "".join( query.group(2,3) ).decode('euc-kr')
       addDir(title,url,1000,thumb)
  # next page
  selNext = False
  for url,bdon in re.compile('<a href="([^"]*)"[^>]*><span[^>]*><b class=(board[^>]*)>\d+').findall(doc):
    if selNext:
      addDir(u"다음 페이지>", "http://music.naver.com"+url, 101, '')
      break
    if bdon == "boardon":
      selNext = True

#--------------------------------------------------------------------
def CAT_MOVIE_CLIP(base_url):
  addDir(u"예고편",base_url+"?subcategoryid=TRAILER",111,'')
  addDir(u"뮤직비디오",base_url+"?subcategoryid=MUSICVIDEO",111,'')
  addDir(u"메이킹",base_url+"?subcategoryid=MAKING",111,'')
  addDir(u"인터뷰",base_url+"?subcategoryid=INTERVIEW",111,'')

def BROWSE_MOVIE_CLIP(main_url):
  doc = urllib.urlopen(main_url).read()
  # video item
  for title,url,thumb in re.compile('''<h5 class="movieclip"><a[^>]*>([^<]*)</a></h5>\s*<a href="([^"]*)"[^>]*><img src="([^"]*)"[^>]*>''',re.S).findall(doc):
     url = "http://movie.naver.com"+url
     addDir(title.decode('euc-kr'),url,1000,thumb)
  # next page
  query = re.compile('<td[^>]*class="next"><a href="([^"]*)">').search(doc)
  if query:
    addDir(u"다음 페이지>", "http://movie.naver.com"+query.group(1), 111, '')

def LIST_MOVIE_CLIP(main_url):
  doc = urllib.urlopen(main_url).read()
  for url,thumb,title in re.compile('''<div class="thumb"><a href="(mediaView[^"]*)"><img src="([^"]*)"[^>]*>.*?<p><a[^>]*>([^<]*)</a></p>''',re.S).findall(doc):
    addDir(title.decode('euc-kr'), "http://movie.naver.com/movie/bi/mi/"+url, 1000, thumb)

def PLAY_VIDEO(main_url):
  doc = urllib.urlopen(main_url).read()
  query = re.compile(r'''(mms://[^"']*)''').search(doc)
  if query:
    xbmc.Player().play( query.group(1) )

#--------------------------------------------------------------------
def BROWSE_KBO_LIVE(main_url):
  doc = urllib.urlopen(main_url).read()
  doc = doc.split('<p class="p_title">')[0]   # upper table
  for lrow in doc.split(r'<tr class="border">'):
    lrow = lrow[ lrow.find("<td>") : ]
    for sect in lrow.split("<tr>"):
      query = re.compile(r'''<a href="javascript:popUp\('([^']*)''').search(sect)
      # or <img[^>]*alt="TV중계">
      if query:
        title = re.compile('<.*?>',re.S).sub("",sect).strip().decode("euc-kr")
        addDir(title, url, 1001, '')

def PLAY_KBO_LIVE(main_url):
  # low bit-rate
  ref_url = main_url.replace("tvRelay","sdPlayerPopup")
  pkg_url = main_url.replace("/gameCenter/tvRelay.nhn", "/mediaPlayer/livePlayer.nhn") + "&low=true&direct="
  req = urllib2.Request(pkg_url)
  req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)')
  req.add_header('Referer',ref_url)
  doc = urllib2.urlopen(req).read()
  query = re.compile(r'''(mms://[^"']*)''').search(doc)
  if query:
    xbmc.Player().play( query.group(1) )

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

if mode==None or url==None or len(url)<1:
  CATEGORIES()
# music video
elif mode==100:
  CAT_MUSIC_VIDEO(url)
elif mode==101:
  BROWSE_MUSIC_VIDEO(url)
# movie clip
elif mode==110:
  CAT_MOVIE_CLIP(url)
elif mode==111:
  BROWSE_MOVIE_CLIP(url)
elif mode==112:
  LIST_MOVIE_CLIP(url)
# live
elif mode==120:
  BROWSE_KBO_LIVE(url)
# common
elif mode==1000:
  PLAY_VIDEO(url)
elif mode==1001:
  PLAY_KBO_LIVE(url)

if mode < 1000:
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
# vim: softtabstop=2 shiftwidth=2 expandtab
