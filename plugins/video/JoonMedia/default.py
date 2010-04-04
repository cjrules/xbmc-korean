# coding=utf-8
"""
  JoonMedia - Korea Drama/TV Shows Streaming Service
"""

import urllib,urllib2,re,xbmcplugin,xbmcgui

# plugin constants
__plugin__ = "JoonMedia"
__author__ = "edge"
__url__ = "http://xbmc-korea.com/"
__svn_url__ = "http://xbmc-korean.googlecode.com/svn/trunk/plugins/video/DramaStyle"
__credits__ = "XBMC Korean User Group"
__version__ = "0.2.1"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

browser_hdr = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ko-KR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

#-----------------------------------------------------
def CATEGORIES():
    ## not parsing homepage for faster speed
    addDir("드라마","http://joonmedia.net/videos/dramas",1,"")
    addDir("오락","http://joonmedia.net/videos/shows",1,"")
    addDir("음악","http://joonmedia.net/videos/music",1,"")
    addDir("다시보기","http://joonmedia.net/videos/classics",1,"")
    addDir("영화","http://joonmedia.net/videos/movies",1,"")
    addDir("일본영화","http://joonmedia.net/videos/jpmovies",1,"")
    addDir("중국영화","http://joonmedia.net/videos/chmovies",1,"")
    addDir("서양영화","http://joonmedia.net/videos/enmovies",1,"")
    addDir("다큐","http://joonmedia.net/videos/docu",1,"")
    addDir("시사교양","http://joonmedia.net/videos/edu",1,"")

def VIDEO(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', browser_hdr)
    response=urllib2.urlopen(req);link=response.read();response.close()
    
    mgrp=re.split('''<div class="column">\s*<div class="box">''', link.decode("utf-8"))
    xbmc.log( "#tvshows=%d"%len(mgrp), xbmc.LOGDEBUG )
    for mgdata in mgrp[1:]:	# skip the first block
	tit_match = re.search('''<a href="(.*?)" class="arrow">(.*?)</a>''', mgdata)
	url = tit_match.group(1)
	title = tit_match.group(2)
	thmb_match = re.search('''<img src="(.*?)" width="[1-9]''', mgdata)
	thumb = thmb_match.group(1)
	xbmc.log( "TV program: %s" % title.encode("euc-kr"), xbmc.LOGDEBUG )
	addDir(title, url, 2, thumb)

def TVSHOW(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', browser_hdr)
    response=urllib2.urlopen(req);link=response.read();response.close()
    
    mgrp=re.split("</li><li>", link.decode("utf-8"))
    xbmc.log( "#episode=%d"%len(mgrp), xbmc.LOGDEBUG )
    for mgdata in mgrp:
	tit_match = re.search('''<b>([^<]*)<br></b>''', mgdata)
	title = tit_match.group(1)
	xbmc.log( "Episode: %s" % title.encode("euc-kr"), xbmc.LOGDEBUG )
	match2=re.compile('''<a href="([^"]*)" target="_blank">\s?(|<br/>)([^<]+)''').findall(mgdata)
	for url,dummy,sup in match2:
	    sup = sup.strip()
	    title2 = "%s (%s)" % (title,sup)
	    xbmc.log( "Found page: %s" % title2.encode("euc-kr"), xbmc.LOGDEBUG )
	    if sup.find(u"멀티로딩")==0:
		addDir( title2.replace(u"멀티로딩",u"유큐"), url, 3, '' )
	    elif sup==u"하이스피드":
		addDir( title2, url, 4, '' )
	    elif sup==u"토두" or sup==u"56com" or sup==u"베오":
		addDir( title2, url, 5, '' )
	    #elif sup.find(u"유튜브")>=0:
	    #	addDir( title2, url, 6, '' )

def EPISODE(main_url,parmode):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', browser_hdr)
    response=urllib2.urlopen(req);link=response.read();response.close()

    match=re.compile('''vcastr_file=(\S*) ''').findall(link)
    i=0
    for flv in match:
	if parmode=="multi":
	    xbmc.log( "multifile parsing", xbmc.LOGDEBUG )
	    flvs=flv.split('|')
	    for flv2 in flvs:
		i=i+1;addLink("Part %d" % i, flv2, "")
	else:
	    i=i+1;addLink("Part %d" % i, flv, "")

def EPISODE_HACK(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', browser_hdr)
    response=urllib2.urlopen(req);link=response.read();response.close()

    match=re.compile('''<embed src="(.*?)" ''').findall(link)
    for cntnr in match:
	xbmc.log( "Container = %s" % cntnr, xbmc.LOGDEBUG )
	GetFLV(cntnr)

def EPISODE_YOUTUBE(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', browser_hdr)
    response=urllib2.urlopen(req);link=response.read();response.close()

    match=re.compile('''flashvars="file=(.*?)&amp;''').findall(link)
    for cntnr in match:
	xbmc.log( "Container = %s" % cntnr, xbmc.LOGDEBUG )
	GetFLV(cntnr)

def GetFLV(url):
    name = 'Watch'
    if url.find('tudou')>0:
	req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+url)
	req.add_header('User-Agent', browser_hdr)
	response=urllib2.urlopen(req);link=response.read();response.close()
	match=re.search('<a href\s*=\s*"(.+?)" target="_blank" ', link)
	if match:
	    flv=re.sub('&amp;','&',match.group(1))
	    flv=re.sub('\?1','?8',flv)	#trick to enable on-the-fly streaming
	    addLink(name, flv, "")
    elif url.find('56.com')>0:
	req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+url)
	req.add_header('User-Agent', browser_hdr)
	response=urllib2.urlopen(req);link=response.read();response.close()
	match=re.search('<a href\s*=\s*"(.+?)" target="_blank" ', link)
	if match:
	    addLink(name, match.group(1), "")
    elif url.find('youku')>0:
	req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+url)
	req.add_header('User-Agent', browser_hdr)
	response=urllib2.urlopen(req);link=response.read();response.close()
	match=re.compile('<a href\s*=\s*"(.+?)" target="_blank" ').findall(link)
	i=0;
	for url in match:
	    i=i+1;addLink(name+" part-"+str(i),url,"")
    elif url.find('veoh')>0:
	#match=re.search(r'http://www.veoh.com/videos/(.+)',url)
	match=re.search('permalinkId=(\w+)&',url)
	req = urllib2.Request('http://www.veoh.com/rest/videos/'+match.group(1)+'/details')
	req.add_header('User-Agent', browser_hdr)
	response=urllib2.urlopen(req);link=response.read();response.close()

	veoh=re.search('fullPreviewHashPath="(.+?)"',link)
	thumb=re.search('fullHighResImagePath="(.+?)"',link)
	addLink(name, veoh.group(1), thumb.group(1))
    elif url.find('youtube')>0:
	# no more working...
	bit=re.search('http://www.youtube.com/.+?v=(.+?)',url)
	req = urllib2.Request(url)
	req.add_header('User-Agent', browser_hdr)
	response=urllib2.urlopen(req);link=response.read();response.close()
	match=re.compile('"t": "(.+?)"').findall(link)
	for youtube in match:
	    addLink(name+"-YOUTUBE","http://www.youtube.com/get_video?video_id="+bit.group(1)+"&t="+youtube,"http://www.webtvwire.com/wp-content/uploads/2007/06/youtube.jpg")
	    addLink(name+"-YOUTUBE Hi-def","http://www.youtube.com/get_video?video_id="+bit.group(1)+"&t="+youtube+"&fmt=18","http://www.webtvwire.com/wp-content/uploads/2007/06/youtube.jpg")
    
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
    xbmc.log( "addLink(%s,%s)" % (name, url), xbmc.LOGDEBUG )
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
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
    VIDEO(url)
elif mode==2:
    TVSHOW(url)
elif mode==3:
    EPISODE(url,'single')
elif mode==4:
    EPISODE(url,'multi')
elif mode==5:
    EPISODE_HACK(url)
elif mode==6:
    EPISODE_YOUTUBE(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
