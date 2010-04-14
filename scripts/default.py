# -*- coding: utf-8 -*-
import sys,os,xbmc
import urllib,md5
import re

__scriptname__ = "GomtvSub"
__author__     = "edge"
__url__        = "http://xbmc-korea.com"
__svn_url__    = "http://xbmc-korean.googlecode.com/svn/trunk/scripts/GomtvSub"
__credits__    = ""
__version__    = "0.1.0"

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
        except IOError:
            print "File could not be opened"
            sys.exit(1)

	# calculate MD5 key from file
	buff = f.read(1024*1024)     # 1MB
	#key = hashlib.new("md5", buff).hexdigest()
	m = md5.new(); m.update(buff); key = m.hexdigest()
	f.close()

###-------------------- Search Subtitle from GomTV site ------------------################
	queryAddr = "http://gom.gomtv.com/jmdb/search.html?key=%s"%key
	req = urllib.urlopen(queryAddr)
	link = req.read(-1)

	match = re.compile('''<div><a href="/jmdb/view.html\?intSeq=(\d+).*?&searchSeq=(\d+)">''').findall(link)
	#for intSeq,searchSeq in match:
	#    print "found %s, %s"%(intSeq,searchSeq)

###---------------------- Download Subtitle -------------------################
	if len(match) > 0:
	    # download the first item
	    try:
		queryAddr = "http://gom.gomtv.com/jmdb/save.html?intSeq=%s&capSeq=%s"%(match[0][0],match[0][1])
		req = urllib.urlopen(queryAddr)
		f = open(smiFullPath,'w')
	    except IOError:
		print "File could not be written"
		sys.exit(1)
	    f.write( req.read(-1) )
	    f.close()

	    import xbmcgui
	    dialog = xbmcgui.Dialog()
	    selected = dialog.ok(u"검색된 자막 갯수: %d".encode("utf-8") % len(match),
			    smiFullPath, u"에 저장되었습니다.".encode("utf-8") )
	    xbmc.Player().setSubtitles(smiFullPath)
	else:
	    import xbmcgui
	    dialog = xbmcgui.Dialog()
	    selected = dialog.ok(u"검색된 자막이 없습니다.".encode("utf-8"))

        if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause
    # end of __main__
