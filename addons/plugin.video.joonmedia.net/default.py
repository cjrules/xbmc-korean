# -*- coding: utf-8 -*-
"""
  JoonMedia - Korea Drama/TV Shows Streaming Service
"""

import urllib
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__plugin__  = "JoonMedia"
__addonID__ = "plugin.video.joonmedia.net"
__author__  = "xbmc-korea"
__url__     = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/addons/plugin.video.joonmedia.net"
__credits__ = "XBMC Korean User Group"
__version__ = "1.2.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

import os
LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
if not LIB_DIR in sys.path:
  sys.path.append (LIB_DIR)

__settings__ = xbmcaddon.Addon( __addonID__ )

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
  addDir(u"한국영화","http://joonmedia.net/videos/movies",1,"")
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
    try: xbmc.log( "TV program: %s" % title.encode("euc-kr"), xbmc.LOGDEBUG )
    except: pass
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
        continue    # skip
      title = ref.string
      url = ref['href']
      try: xbmc.log( "TV program: %s" % title.encode("euc-kr"), xbmc.LOGDEBUG )
      except: pass
      addDir(title, url, 3, '')

def TVSHOW(main_url):
  link = urllib.urlopen(main_url)
  soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
  colsel = int(__settings__.getSetting("VideoColumn"))
  episodes = soup("div", {"class" : "column"})[colsel-1].findAll('li')
  for episode in episodes:
    title = ''.join(episode.find('b').findAll(text=lambda text:isinstance(text, NavigableString)))
    for ref in episode.findAll('a'):
      url = ref['href']
      suppl = ''.join(ref.findAll(text=lambda text:isinstance(text, NavigableString))).strip()
      title2 = u"%s (%s)" % (title,suppl)
      try: xbmc.log( "Found page: %s" % title2.encode("euc-kr"), xbmc.LOGDEBUG )
      except: pass
      if suppl.find(u"멀티로딩")==0:
        addDir( title2.replace(u"멀티로딩",u"유큐"), url, 5, GetFLV.img("youku") )
      elif suppl.find(u"유큐")==0 or suppl.find(u"유쿠")==0:
        pass	# always paired with 멀티로딩
      elif suppl.find(u"토두")==0:
        addDir( title2, url, 4, GetFLV.img("tudou") )
      elif suppl.find(u"56com")==0:
        addDir( title2, url, 4, GetFLV.img("56.com") )
      elif suppl.find(u"베오")==0:
        addDir( title2+u" [preview]", url, 4, GetFLV.img("veoh") )
      elif suppl.find(u"하이스피드")==0:
        addDir( title2, url, 5, '' )
      elif suppl.find(u"유튜브")==0 or suppl.find(u"유투브")==0 or suppl.lower()==u"youtube":
        addDir( title2, url, 6, GetFLV.img("youtube") )
      elif suppl.find(u"데일리모션")==0:
        addDir( title2, url, 7, GetFLV.img("dailymotion") )
      else:
        xbmc.log( "Unsupported %s at %s" % (suppl.encode("euc-kr"),main_url), xbmc.LOGWARNING )

def EPISODE(main_url):
  link = urllib.urlopen(main_url)
  soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
  vid_list = []
  for item in soup.findAll('embed'):
    swf = item['src']
    thumb = GetFLV.img(swf)
    xbmc.log( "Container[0]: %s" % swf, xbmc.LOGDEBUG )
    vid_list.extend( GetFLV.flv(swf) )
  PLAY_LIST(vid_list, thumb)

def EPISODE_DIRECT(main_url):
  # BeautifulSoup can not handle a statement not protected by quote
  import re
  tDoc = urllib.urlopen(main_url).read().decode('utf-8')
  vid_list = []
  for blk in re.compile('src=\S*vcastr_file=(\S*)').findall(tDoc):
    vid_list.extend( blk.split('|') )
  vid_list.extend( re.compile('</script>\s*<a\s*href="(.*?)"').findall(tDoc) )
  PLAY_LIST(vid_list, '')

def EPISODE_YOUTUBE(main_url):
  link = urllib.urlopen(main_url)
  soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
  vid_list = []
  for item in soup.findAll('embed'):
    if item.has_key('flashvars'):
      pkg = item['flashvars']
      ptn2 = 'file='
      pkg = pkg[pkg.find(ptn2)+len(ptn2):pkg.find('&amp;')]
      pkg = urllib.unquote_plus(pkg)
      thumb = GetFLV.img(pkg)
      xbmc.log( "Container[1]: %s" % pkg, xbmc.LOGDEBUG )
      if pkg.endswith('xml'):
        xml = urllib.urlopen(pkg).read()
        import re
        swf_list = re.compile('<location>([^<]*)</location>').findall(xml)
      else:
        swf_list = [pkg]
      for swf in swf_list:
        vid_list.extend( GetFLV.flv(swf) )
    else:
      swf = item['src']
      if '&' in swf:
        swf = swf[:swf.find('&')]
      thumb = GetFLV.img(swf)
      xbmc.log( "Container[2]: %s" % swf, xbmc.LOGDEBUG )
      vid_list.extend( GetFLV.flv(swf) )
  PLAY_LIST(vid_list, thumb)

def EPISODE_PARAM(main_url):
  link = urllib.urlopen(main_url)
  strain = SoupStrainer( "param", { "name" : "movie" } )
  soup = BeautifulSoup( link.read(), strain, fromEncoding="utf-8" )
  vid_list = []
  for item in soup.findAll('param'):
    cntnr=item['value']
    xbmc.log( "Container[3]: %s" % cntnr, xbmc.LOGDEBUG )
    thumb = GetFLV.img(cntnr)
    vid_list.extend( GetFLV.flv(cntnr) )
  PLAY_LIST(vid_list, thumb)

def PLAY_LIST(vid_list, thumb):
  xbmc.log( "PLAY_LIST %d" % len(vid_list), xbmc.LOGDEBUG )
  playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
  playlist.clear()
  i=0
  for vid in vid_list:
    i=i+1; title="Part %d"%i
    item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
    item.setInfo( type="Video", infoLabels={ "Title": title } )
    playlist.add(vid, item)
  xbmc.Player().play(playlist)

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
  try: xbmc.log( "addLink(%s,%s)" % (name.encode("euc-kr"), url), xbmc.LOGDEBUG )
  except: pass
  name=name.encode("utf-8")
  iconimage=iconimage.encode("utf-8")
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
  return ok

def addDir(name,url,mode,iconimage):
  name=name.encode("utf-8")
  iconimage=iconimage.encode("utf-8")
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  xbmc.log( "addDir(%s)" % u, xbmc.LOGDEBUG )
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

if mode==None or mode < 4:
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
# vim: softtabstop=2 shiftwidth=2 expandtab
