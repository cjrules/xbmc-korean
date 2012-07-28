# -*- coding: utf-8 -*-
"""
  BayKoreans - Korea Drama/TV Shows Streaming Service
"""
import xbmcaddon, xbmcplugin, xbmcgui
import urllib, urllib2, re
from BeautifulSoup import BeautifulSoup, SoupStrainer

__addonid__ = "plugin.video.baykoreans.net"
__addon__ = xbmcaddon.Addon(__addonid__)

UserAgent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
root_url = "http://baykoreans.net"
show_thumb = __addon__.getSetting('showThumb').lower() == 'true'

from extract_withflvcd import extract_withFLVCD

def rootList():
  ## not parsing homepage for faster speed
  addDir("방영 드라마",root_url+"/drama",1,"")
  addDir("종영 드라마",root_url+"/drama_fin",1,"")
  addDir("예능 | 오락",root_url+"/entertain",1,"")
  addDir("시사 | 교양",root_url+"/current",1,"")
  addDir("영화",root_url+"/movie",4,"")
  #addDir("영화 예고편",root_url+"/trailer",6,"")
  addDir("애니 극장판",root_url+"/animation",4,"")
  #addDir("애니 장편",root_url+"/animation_featured",7,"")
  addDir("스포츠",root_url+"/sports",1,"")
  addDir("뮤직비디오",root_url+"/music",1,"")
  endDir()

#-----------------------------------                
def _progList(main_url):
  req = urllib2.Request(main_url)
  req.add_header('User-Agent', UserAgent)
  resp = urllib2.urlopen(req)
  doc = resp.read()
  resp.close()
  soup = BeautifulSoup(doc, fromEncoding='utf-8')

  strain = SoupStrainer("td", {"class":"title"})
  for item in soup.findAll(strain):
    thumb = ""
    if item.div and show_thumb:
      thumb = item.div.img['src']
    if item.p.a:
      title = item.p.a.string.replace('&amp;','&').encode('utf-8')
      url = item.p.a['href']
      if not url.startswith('http://'):
      	url = root_url + url
      addDir(title, url, 3, thumb)

  strain = SoupStrainer("div", {"class":"pagination"})
  cur = soup.find(strain).find("strong")
  p = cur.findPreviousSibling("a")
  if not p.has_key("class"):
    url = root_url+p['href']
    addDir("< 이전", url, 2, "")
  p = cur.findNextSibling("a")
  if not p.has_key("class"):
    url = root_url+p['href']
    addDir("다음 >", url, 2, "")

def progList(main_url):
  _progList(main_url)
  endDir()

def progListUpdate(main_url):
  _progList(main_url)
  endDir(True)

#-----------------------------------                
def _movieList(main_url):
  req = urllib2.Request(main_url)
  req.add_header('User-Agent', UserAgent)
  resp = urllib2.urlopen(req)
  doc = resp.read()
  resp.close()
  soup = BeautifulSoup(doc, fromEncoding='utf-8')

  strain = SoupStrainer("div", {"class":"title"})
  for item in soup.findAll(strain):
    title = item.a.string.replace('&amp;','&').encode('utf-8')
    url = item.a['href']
    if not url.startswith('http://'):
      url = root_url + url

    thumb = ""
    if show_thumb:
      thumb = item.findNextSibling("div", {"class":"thumb"}).find('img')['src']
    addDir(title, url, 3, thumb)

  strain = SoupStrainer("div", {"class":"pagination"})
  cur = soup.find(strain).find("strong")
  p = cur.findPreviousSibling("a")
  if not p.has_key("class"):
    url = root_url+p['href']
    addDir("< Prev", url, 5, "")
  p = cur.findNextSibling("a")
  if not p.has_key("class"):
    url = root_url+p['href']
    addDir("Next >", url, 5, "")

def movieList(main_url):
  _movieList(main_url)
  endDir()

def movieListUpdate(main_url):
  _movieList(main_url)
  endDir(True)

#-----------------------------------                
def videoList(main_url, main_title):
  req = urllib2.Request(main_url)
  req.add_header('User-Agent', UserAgent)
  resp = urllib2.urlopen(req)
  doc = resp.read()
  resp.close()
  ptn = re.compile('<script language="javascript">document\.write\(unescape\("(.*?)"\)\);</script>')
  clist = []
  for enc in ptn.findall(doc):
    dec = unescape(enc)
    clist.append(dec)
  soup = BeautifulSoup('\n'.join(clist))
  for item in soup.findAll('a'):
    url = item['href']
    title = item.span.string.split('|')[0].strip()

    if not url.startswith('http://'):
      url = root_url + url
    base_url = url[ : url.find('/',7)] 
    if url.find('/?xink=') > 0:
      xink = re.search('xink=(.*)', url).group(1)
      if url.find('/tudou.y/') > 0:
        addDir(title, xink, 12, "", title=main_title)
      elif url.find('/sohu/') > 0:
        addDir(title, "http://my.tv.sohu.com/u/vw/"+xink, 11, "")
      elif url.find('youtube') > 0: # /tube/
        addDir(title, xink, 13, "", title=main_title)
      elif url.find('dailymotion') > 0: # /tube/
        addDir(title, xink, 14, "", title=main_title)
      elif url.find('/xink/') > 0:
        addDir(title, xink, 10, "")
      elif url.find('/preview/') > 0: # url list
        addDir(title, xink, 15, "", title=main_title)
      else:
        xbmc.log("Unsupported URL, "+url, xbmc.LOGWARNING)
    elif url.find('/?link=') > 0:
      req = urllib2.Request(url)
      req.add_header('User-Agent', UserAgent)
      resp = urllib2.urlopen(req)
      doc = resp.read()
      resp.close()
      vid_url = re.search(r'\)\);</script>([^>]*)">', doc).group(1)
      addLink(title, base_url+"/linkout/getfile/"+vid_url, "")
    else:
      addDir(title, url, 10, "")
  endDir()

def replace_entities(match):
  try:
    return unichr(int(match.group(1), 16))
  except:
    return match.group()

def unescape(s):
  return re.compile(r"\\x([A-F0-9]{2})").sub(replace_entities, s)

#-----------------------------------                
def playFLVCD(main_url):
  try:
    vid_list = extract_withFLVCD(main_url)
  except:
    xbmc.log("Fail to extract with FLVCD: " + main_url, xbmc.LOGWARNING)
    dialog = xbmcgui.Dialog()
    dialog.ok("Error", "Fail to extract video link with FLVCD")
    return

  pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
  pl.clear()
  for vid in vid_list:
    li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": vid['title']})
    pl.add(vid['url']+"|User-Agent="+UserAgent, li)
    xbmc.log("Video: "+vid['url'], xbmc.LOGDEBUG)
  xbmc.Player().play(pl)

def playSohu(main_url):
  import extract_sohu
  try:
    vid_list = extract_sohu.extract_video_from_url(main_url)
  except:
    xbmc.log("Fail to extract Sohu, " + main_url, xbmc.LOGWARNING)
    dialog = xbmcgui.Dialog()
    dialog.ok("Error", "Fail to extract video link with FLVCD")
    return

  pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
  pl.clear()
  for vid in vid_list:
    li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": vid['title']})
    pl.add(url+"|User-Agent="+UserAgent, li)
    xbmc.log("Video: "+vid['url'], xbmc.LOGDEBUG)
  xbmc.Player().play(pl)

def playTudouId(iid,title):
  import extract_tudou
  try:
    #icode = extract_tudou.revert_icode(iid)
    #vid_list = extract_tudou.extract_video(icode)
    vid_list = extract_tudou.extract_video_from_iid(iid)
    vid_url = vid_list[0]['url']
  except:
    xbmc.log("Fail to extract Tudou %s" % iid, xbmc.LOGWARNING)
    dialog = xbmcgui.Dialog()
    dialog.ok("Fail to extract video link", iid)
    return

  xbmc.log("Tudou: "+vid_url, xbmc.LOGDEBUG)
  li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
  li.setInfo('video', {"Title": title})
  xbmc.Player().play(vid_url+"|User-Agent="+UserAgent, li)

def playYoutube(main_url, title):
  fmttbl = {"270p":18, "360p":34, "480p":35, "720p":22, "1080p":37}
  import extract_youtube

  vid = main_url[ main_url.rfind('/')+1 : ]
  vid_urls = extract_youtube.extract_video(vid)
  qual = int(fmttbl[__addon__.getSetting('youtubeQuality')])
  if vid_urls.has_key(qual):
    url = vid_urls[qual]
    xbmc.log("Youtube: "+url, xbmc.LOGDEBUG)
    li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": title})
    xbmc.Player().play(url, li)
  elif len(vid_urls):
    dialog = xbmcgui.Dialog()
    dialog.ok("Warning", "You'd be better try again with other Youtube quality")

def playDmotion(main_url, title):
  import extract_dailymotion
  vid = extract_dailymotion.extract_id(main_url)
  vid_urls = extract_dailymotion.extract_video(vid)

  qual = __addon__.getSetting('dailymotionQuality')
  if not vid_urls.has_key(qual):
    return

  pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
  pl.clear()
  for url in vid_urls[qual]:
    li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": title})
    pl.add(url+"|User-Agent="+UserAgent, li)
    xbmc.log("Video: "+url, xbmc.LOGDEBUG)
  xbmc.Player().play(pl)

def playList(main_url, title):
  urls = main_url.split('|')

  pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
  pl.clear()
  for i in range(len(urls)):
    url = urls[i]
    title2 = "{0:s} - {1:d}".format(title, i+1)
    li = xbmcgui.ListItem(title2, iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": title2})
    pl.add(url+"|User-Agent="+UserAgent, li)
    xbmc.log("Video: "+url, xbmc.LOGDEBUG)
  xbmc.Player().play(pl)

#-----------------------------------                
def addDir(name,url,mode,thumb,title=""):
  li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
  u = sys.argv[0]+"?url="+urllib.quote_plus(url)
  u += "&mode="+str(mode)
  u += "&name="+urllib.quote_plus(name)
  u += "&title="+urllib.quote_plus(title)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def endDir(update=False):
  xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=update)

def addLink(name,url,thumb):
  li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
  li.setInfo( type="Video", infoLabels={ "Title": name } )
  xbmcplugin.addDirectoryItem(int(sys.argv[1]),url,li)

#-----------------------------------                
def get_params():
  param = []
  paramstring = sys.argv[2]
  if len(paramstring)>=2:
    params = sys.argv[2]
    cleanedparams = params.replace('?','')
    if (params[len(params)-1]=='/'):
      params = params[0:len(params)-2]
    pairsofparams = cleanedparams.split('&')
    param = {}
    for i in range(len(pairsofparams)):
      splitparams = {}
      splitparams = pairsofparams[i].split('=')
      if (len(splitparams)) == 2:
        param[splitparams[0]] = splitparams[1]
  return param

params = get_params()
url = None
name = None
mode = None
title = None

try:
  url = urllib.unquote_plus(params["url"])
except:
  pass
try:
  name = urllib.unquote_plus(params["name"])
except:
  pass
try:
  mode = int(params["mode"])
except:
  pass
try:
  title = urllib.unquote_plus(params["title"])
except:
  pass

if mode == None:
  rootList()
elif mode == 1:
  progList(url)
elif mode == 2:
  progListUpdate(url)
elif mode == 3:
  videoList(url,name)
elif mode == 4:
  movieList(url)
elif mode == 5:
  movieListUpdate(url)
elif mode == 10:
  playFLVCD(url)
elif mode == 11:
  playSohu(url)
elif mode == 12:
  playTudouId(url,title)
elif mode == 13:
  playYoutube(url,title)
elif mode == 14:
  playDmotion(url,title)
elif mode == 15:
  playList(url,title)

# vim:sts=2:sw=2:et
