# -*- coding: utf-8 -*-
"""
  133133.com - 요싼싼넷
"""
import urllib,re
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.133133.com"
__addon__ = xbmcaddon.Addon( __addonid__ )
_L = __addon__.getLocalizedString

import os.path
LIB_DIR = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)
import yss133

root_url = "http://www.133133.com"

tPrevPage = u"[B]<%s[/B]" % _L(30100)
tNextPage = u"[B]%s>[/B]" % _L(30101)

#-----------------------------------------------------
def rootList():
  ## not parsing homepage for faster speed
  list_url = root_url+"/ucc/list.php?cate1="
  addDir(u"영화보기",list_url+"영화",1,"")
  addDir(u"드라마",list_url+"드라마",1,"")
  addDir(u"오락프로",list_url+"오락프로",1,"")
  addDir(u"애니메이션",list_url+"애니메이션",1,"")
  addDir(u"음악관련",list_url+"음악관련",1,"")
  addDir(u"뮤직비디오",list_url+"뮤비",1,"")
  addDir(u"최근프로보기",root_url+"/ucc/new_list.php",5,"")
  endDir()

def _progList(main_url):
  info = yss133.parseList(main_url)
  for item in info['link']:
    addDir(item['title'], item['url'], 3, item['thumb'])
  if 'prevpage' in info and info['prevpage']:
    addDir(tPrevPage, info['prevpage'], 2, "")
  if 'nextpage' in info and info['nextpage']:
    addDir(tNextPage, info['nextpage'], 2, "")

def progList(main_url):
  _progList(main_url)
  endDir()

def progListNext(main_url):
  _progList(main_url)
  endDir(True)

def newList(main_url):
  for days in yss133.parseNewList(main_url):
    addDir(u"[COLOR FFFF0000]%s[/COLOR]" % days['name'], "-", 0, "")
    for title, url in days['list']:
      addDir(title, url, 3, "")
  endDir()

def _episodeList(main_url):
  info = yss133.parseProg(main_url)
  for episode in info:
    for url in episode['list']:
      title = episode['title']
      if url.find('youku.com') >= 0:
        title += u" [유쿠]"
      elif url.find('tudou.com') >= 0:
        title += u" [토두]"
      elif url.find('sohu.com') >= 0:
        title += u" [소후]"
      addDir(title, url, 4, "")

def episodeList(main_url):
  _episodeList(main_url)
  endDir()

#-----------------------------------                
def playVideo(main_url):
  if main_url.find('tudou.com') > 0:
    import extract_tudou
    vid_list = extract_tudou.extract_video_from_url(main_url)
  elif main_url.find('youku.com') > 0 or main_url.find('yinyuetai.com') > 0:
    from extract_withflvcd import extract_withFLVCD
    vid_list = extract_withFLVCD(urllib.quote_plus(main_url))
  elif url.find('sohu.com') > 0:
    import extract_sohu
    vid_list = extract_sohu.extract_video_from_url(main_url)
  else:
    xbmc.Dialog().ok("Unsupported site", main_url)
    return

  if len(vid_list) == 0:
    xbmcgui.Dialog().ok("Fail to extract video", main_url)
    return

  pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
  pl.clear()
  for vid in vid_list:
    li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": vid['title'] } )
    pl.add(vid['url'], li)
  xbmc.Player().play(pl)

#-----------------------------------                
def get_params():
  param=[]
  paramstring=sys.argv[2]
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
  name=name.encode('utf-8')
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
  return ok

def addDir(name,url,mode,iconimage):
  name=name.encode('utf-8')
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  u+="&mode="+str(mode)
  u+="&name="+urllib.quote_plus(name)
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
xbmc.log( "Mode: "+str(mode), xbmc.LOGINFO)
xbmc.log( "URL : "+str(url), xbmc.LOGINFO)
xbmc.log( "Name: "+str(name), xbmc.LOGINFO)

if mode==None:
  rootList()
elif mode==1:
  progList(url)
elif mode==2:
  progListNext(url)
elif mode==3:
  episodeList(url)
elif mode==4:
  playVideo(url)
elif mode==5:
  newList(url)

# vim:sts=2:sw=2:et
