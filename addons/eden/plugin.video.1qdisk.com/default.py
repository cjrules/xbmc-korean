# -*- coding: utf-8 -*-
"""
  1qdisk.com - 원큐디스크
"""
import urllib,re
import xbmcaddon,xbmcplugin,xbmcgui

# plugin constants
__addonid__ = "plugin.video.1qdisk.com"
__addon__ = xbmcaddon.Addon( __addonid__ )
_L = __addon__.getLocalizedString

import os.path
LIB_DIR = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)
import q1qdisk

root_url = "http://1qdisk.com"

tPrevPage = u"[B]<%s[/B]" % _L(30100)
tNextPage = u"[B]%s>[/B]" % _L(30101)

#-----------------------------------------------------
def rootList():
  ## not parsing homepage for faster speed
  #list_url = root_url + "/vod/list.html?cate=%s&free=Y"
  list_url = root_url + "/vod/list.html?cate=%s"
  addDir(u"영화",list_url%"100000",1,"")
  addDir(u"드라마",list_url%"200000",1,"")
  addDir(u"예능프로",list_url%"300000",1,"")
  addDir(u"스포츠",list_url%"400000",1,"")
  addDir(u"애니",list_url%"500000",1,"")
  addDir(u"시사다큐",list_url%"600000",1,"")
  addDir(u"게임",list_url%"800000",1,"")
  addDir(u"기타",list_url%"700000",1,"")
  endDir()

def _progList(main_url):
  info = q1qdisk.parseList(main_url)
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

def _episodeList(main_url):
  info = q1qdisk.parseProg(main_url)
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
  elif url.find('sohu.com') > 0:
    import extract_sohu
    vid_list = extract_sohu.extract_video_from_url(main_url)
  elif main_url.find('youku.com') > 0:
    from extract_withflvcd import extract_withFLVCD
    vid_list = extract_withFLVCD(urllib.quote_plus(main_url))
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

# vim:sts=2:sw=2:et
