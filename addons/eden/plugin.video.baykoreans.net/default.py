# -*- coding: utf-8 -*-
"""
  BayKoreans - Korea Drama/TV Shows Streaming Service
"""
import xbmcaddon, xbmcplugin, xbmcgui
import urllib, urllib2, re
from BeautifulSoup import BeautifulSoup, SoupStrainer
import xml.dom.minidom
from random import randint

__plugin__  = "BayKoreans"
__addonid__ = "plugin.video.baykoreans.net"
__addon__ = xbmcaddon.Addon(__addonid__)

UserAgent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
root_url = "http://baykoreans.net"
show_thumb = __addon__.getSetting('showThumb').lower() == 'true'

def rootList():
  ## not parsing homepage for faster speed
  addDir("방영 드라마",root_url+"/drama",1,"")
  addDir("종영 드라마",root_url+"/drama_fin",1,"")
  addDir("예능|오락",root_url+"/entertain",1,"")
  addDir("시사|교양",root_url+"/current",1,"")
  addDir("영화",root_url+"/movie",1,"")
  addDir("영화 예고편",root_url+"/trailer",1,"")
  addDir("애니 극장판",root_url+"/animation",1,"")
  addDir("애니 장편",root_url+"/animation_featured",1,"")
  addDir("스포츠",root_url+"/sports",1,"")
  addDir("뮤직비디오",root_url+"/music",1,"")
  endDir()

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
      title = item.p.a.string.encode('utf-8')
      url = item.p.a['href']
      if not url.startswith('http://'):
      	url = root_url + url
      addDir(title, url, 3, thumb)

  strain = SoupStrainer("div", {"class":"pagination"})
  cur = soup.find(strain).find("strong")
  p = cur.findPreviousSibling("a")
  if not p.has_key("class"):
    url = root_url+p['href']
    addDir("< Prev", url, 2, "")
  p = cur.findNextSibling("a")
  if not p.has_key("class"):
    url = root_url+p['href']
    addDir("Next >", url, 2, "")

def progList(main_url):
  _progList(main_url)
  endDir()

def progListUpdate(main_url):
  _progList(main_url)
  endDir(True)

def videoList(main_url):
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
        addDir(title, xink, 5, "")
      elif url.find('/sohu/') > 0:
        addDir(title, "http://my.tv.sohu.com/u/vw/"+xink, 4, "")
      elif url.find('/xink/') > 0:
        addDir(title, xink, 4, "")
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
      addDir(title, url, 4, "")
  endDir()

def playFLVCD(main_url):
  vid_list = []

  try:
    url = "http://www.flvcd.com/parse.php?kw="+main_url
    hdl = urllib.urlopen(url)
    doc = hdl.read().decode('gb2312')
    hdl.close()

    vlist = re.compile('<input[^>]*name="inf" value="(.*?)">', re.S).search(doc).group(1)
    for item in vlist.split('<$>'):
      try:
        title = re.compile(r"<N>(.*)", re.U).search(item).group(1).encode('utf-8')
        url = re.compile(r"<U>(.*)").search(item).group(1)
        vid_list.append( {"title":title, "url":url} )
      except:
        pass
  except:
    xbmc.log("Unsupported FLVCD result", xbmc.LOGWARNING)
    dialog = xbmcgui.Dialog()
    dialog.ok("Error", "Fail to get video link")
    return

  pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
  pl.clear()
  for vid in vid_list:
    li = xbmcgui.ListItem(vid['title'], iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": title})
    pl.add(vid['url']+"|User-Agent="+UserAgent, li)
    xbmc.log("Video: "+vid['url'], xbmc.LOGDEBUG)
  xbmc.Player().play(pl)

def playTudouId(iid,title):
  values = {
    'it' : iid,
    "hd" : "1",
    "mt" : "0",
  }
  url = "http://v2.tudou.com/v.action?"+urllib.urlencode(values)
  hdl = urllib.urlopen(url)
  doc = hdl.read()
  hdl.close()
  dom = xml.dom.minidom.parseString(doc)
  try:
    icode = dom.getElementsByTagName('v')[0].getAttribute('code')
    xbmc.log("Tudou: "+icode, xbmc.LOGDEBUG)
  except:
    xbmc.log("Tudou video({0:s}) not exist anymore".format(iid), xbmc.LOGDEBUG)
    dialog = xbmcgui.Dialog()
    dialog.ok("Error", "Invalid video link")
    return

  try:
    url = "http://www.flvcd.com/parse.php?kw=http://www.tudou.com/programs/view/{0:s}/".format(icode)
    hdl = urllib.urlopen(url)
    doc = hdl.read().decode('gb2312')
    hdl.close()
    vid_url = re.search('<a href\s*=\s*"(http://\d.+?)" target="_blank"', doc).group(1)
    vid_url = urllib.unquote(vid_url)
    vid_url = vid_url.replace("?1", "?8") # trick to make streaming
    xbmc.log("Tudou: "+vid_url, xbmc.LOGDEBUG)
    li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
    li.setInfo('video', {"Title": title})
    xbmc.Player().play(vid_url+"|User-Agent="+UserAgent, li)
  except:
    dialog = xbmcgui.Dialog()
    dialog.ok("Error", "Fail to get video link")

#-----------------------------------                
def replace_entities(match):
  try:
    return unichr(int(match.group(1), 16))
  except:
    return match.group()

def unescape(s):
  return re.compile(r"\\x([A-F0-9]{2})").sub(replace_entities, s)

#-----------------------------------                
def addDir(name,url,mode,thumb):
  li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
  u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
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

if mode == None:
  rootList()
elif mode == 1:
  progList(url)
elif mode == 2:
  progListUpdate(url)
elif mode == 3:
  videoList(url)
elif mode == 4:
  playFLVCD(url)
elif mode==5:
  playTudouId(url,name)

# vim:sts=2:sw=2:et
