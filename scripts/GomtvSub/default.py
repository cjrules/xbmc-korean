# -*- coding: utf-8 -*-
import sys,os,xbmc
import urllib2,md5
import re

__scriptname__ = "GomtvSub"
__author__     = "edge"
__url__        = "http://xbmc-korea.com"
__svn_url__    = "http://xbmc-korean.googlecode.com/svn/trunk/scripts/GomtvSub"
__credits__    = ""
__version__    = "1.0.0"

#############-----------------Is script runing from OSD? -------------------------------###############

#if not xbmc.getCondVisibility('videoplayer.isfullscreen') :
if not xbmc.Player().isPlayingVideo() :
    import xbmcgui
    dialog = xbmcgui.Dialog()
    selected = dialog.ok("GomtvSub", u"곰tv 자막검색".encode("utf-8"), "http://gom.gomtv.com/jmdb/" )
else:
    window = False
    skin = "main"
    skin1 = str(xbmc.getSkinDir().lower())
    skin1 = skin1.replace("-"," ")
    skin1 = skin1.replace("."," ")
    skin1 = skin1.replace("_"," ")
    if ( skin1.find( "eedia" ) > -1 ):
         skin = "MiniMeedia"
    if ( skin1.find( "tream" ) > -1 ):
         skin = "MediaStream"
    if ( skin1.find( "edux" ) > -1 ):
         skin = "MediaStream_Redux"
    if ( skin1.find( "aeon" ) > -1 ):
         skin = "Aeon"
    if ( skin1.find( "alaska" ) > -1 ):
         skin = "Alaska"
    if ( skin1.find( "confluence" ) > -1 ):
         skin = "confluence"     
  
    try: xbox = xbmc.getInfoLabel( "system.xboxversion" )
    except: xbox = ""
    if xbox != "" and len(skin) > 13:
      skin = skin.ljust(13)

    print "GomtvSub version [" +  __version__ +"]"
    print "Skin Folder: [ " + skin1 +" ]"
    print "GomtvSub skin XML: [ " + skin +" ]"
   
    if ( __name__ == "__main__" ):
        if not xbmc.getCondVisibility('Player.Paused') : xbmc.Player().pause()

###--------------------- Calculate Key from Movie File ----------------################
        movieFullPath = xbmc.Player().getPlayingFile()
	smiFullPath = movieFullPath[:movieFullPath.rfind('.')]+'.smi'
        
        try:
            f=open(movieFullPath,"rb")
	    buff = f.read(1024*1024)     # 1MB
        except IOError:
            print "File could not be read"
            sys.exit(1)
	f.close()

	# calculate MD5 key from file
	#key = hashlib.new("md5", buff).hexdigest()
	m = md5.new(); m.update(buff); key = m.hexdigest()

###----------------- Search subtitle in GomTV site ---------------################
	queryAddr = "http://gom.gomtv.com/jmdb/search.html?key=%s"%key
	req = urllib2.Request(queryAddr)
	resp = urllib2.urlopen(req)
	link = resp.read(); resp.close()

	url_match  = re.compile('''<div><a href="(.*?)">''').findall(link)
	date_match = re.compile('''<td>(\d{4}.\d{2}.\d{2})</td>''').findall(link)
	if len(url_match) != len(date_match): 
            print "Unusual result page"
            sys.exit(1)

	import xbmcgui

	if len(url_match) > 0:
###------------------ Select a subtitle to download ---------------################
	    dialog = xbmcgui.Dialog()
	    selected = dialog.select(u"검색된 자막 갯수: %d".encode("utf-8") % len(date_match),
			    date_match )
	    print "user selects %d"%selected

	    if selected>=0:
		req = urllib2.Request( "http://gom.gomtv.com"+url_match[selected] )
		resp = urllib2.urlopen(req)
		link = resp.read(); resp.close()
		downid = re.search('''javascript:save\('(\d+)','(\d+)','.*?'\);''',link).group(1,2)

###----------------- Download the selected subtitle -----------------################
		queryAddr = "http://gom.gomtv.com/jmdb/save.html?intSeq=%s&capSeq=%s"%downid
		req = urllib2.Request(queryAddr)
		resp = urllib2.urlopen(req)
		try:
		    f = open(smiFullPath,'w')
		    f.write( resp.read() )
		except IOError:
		    print "File could not be written"
		    sys.exit(1)
		f.close(); resp.close()

		dialog = xbmcgui.Dialog()
		ignored = dialog.ok(u"다운로드 성공".encode("utf-8"),
				u"%s 자막이".encode("utf-8")%date_match[selected],
				smiFullPath, u"에 저장되었습니다.".encode("utf-8") )
		xbmc.Player().setSubtitles(smiFullPath)
	else:
	    dialog = xbmcgui.Dialog()
	    selected = dialog.ok(u"검색실패".encode("utf-8"),
			    u"%s로".encode("utf-8")%os.path.basename(movieFullPath),
			    u"검색된 자막이 없습니다.".encode("utf-8"))

        if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause

    # end of __main__
    sys.modules.clear()
