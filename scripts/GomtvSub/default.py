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
    selected = dialog.ok(__scriptname__,
			"Download Subtitle from GomTV Database",
			"http://gom.gomtv.com/jmdb/" )
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
	print "Subtitle will be saved at "+smiFullPath
        
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

	import xbmcgui
	browser_hdr = 'GomPlayer 2, 1, 23, 5007 (KOR)'

###----------------- Search subtitle in GomTV site ---------------################
	class SearchFailed(Exception):
	    pass

	try:
	    queryAddr1 = "http://gom.gomtv.com/jmdb/search.html?key=%s"%key
	    print "search subtitle at %s"%queryAddr1
	    req = urllib2.Request(queryAddr1)
	    req.add_header('User-Agent', browser_hdr)
	    resp = urllib2.urlopen(req)
	    link = resp.read(); resp.close()

	    match = re.match('''<script>location.href = '(.*?)';</script>''',link)
	    if match:
		# auto redirected when there is only one result
		queryAddr2 = "http://gom.gomtv.com/jmdb/"+match.group(1)
		subTitle = "Subtitle "
	    else:
		# regular search result page
		url_match  = re.compile('''<div><a href="(.*?)">''').findall(link)
		date_match = re.compile('''<td>(\d{4}.\d{2}.\d{2})</td>''').findall(link)
		if len(url_match) != len(date_match): 
		    print "Unusual result page"
		    raise SearchFailed

###------------------ Select a subtitle to download ---------------################
		if len(url_match)==0:
		    dialog = xbmcgui.Dialog()
		    ignored = dialog.ok(__scriptname__,
				    "No subtitle is found for %s"%os.path.basename(movieFullPath) )
		    raise SearchFailed
		else:
		    dialog = xbmcgui.Dialog()
		    selected = dialog.select("Subtitles Found: %d"%len(date_match), date_match )

		    if selected < 0:	# cancelled by user
			raise SearchFailed
		    else:
			queryAddr2 = "http://gom.gomtv.com"+url_match[selected]
			subTitle = date_match[selected]

###----------------- Retrieve the selected subtitle -----------------################
	    print "download script from %s"%queryAddr2
	    req = urllib2.Request(queryAddr2)
	    req.add_header('User-Agent', browser_hdr)
	    req.add_header('Referer', queryAddr1)
	    resp = urllib2.urlopen(req)
	    link = resp.read(); resp.close()
	    downid = re.search('''javascript:save\('(\d+)','(\d+)','.*?'\);''',link).group(1,2)

	    queryAddr3 = "http://gom.gomtv.com/jmdb/save.html?intSeq=%s&capSeq=%s"%downid
	    print "actual script is located at %s"%queryAddr3
	    req = urllib2.Request(queryAddr3)
	    req.add_header('User-Agent', browser_hdr)
	    req.add_header('Referer', queryAddr2)
	    resp = urllib2.urlopen(req)
	    try:
		f = open(smiFullPath,'w')
	    except IOError:
		print "File could not be written"
		raise SearchFailed

###----------------- Download the file -----------------################
	    fileSz = int( resp.info()['Content-Length'] )
	    stepSz = 10*1024	# 10KB step size

	    dialog = xbmcgui.DialogProgress()
	    ignored = dialog.create(__scriptname__, 'Downloading subtitle...')
	    sz = 0
	    while 1:
		if dialog.iscanceled():
		    break
		buf = resp.read(stepSz)
		if not buf: break
		sz += len(buf)
		f.write( buf )
		dialog.update( 100*sz/fileSz )
	    f.close(); resp.close()
	    dialog.close()

	    dialog = xbmcgui.Dialog()
	    if sz < fileSz:
		ignored = dialog.ok(__scriptname__,
				"Download cancelled" )
	    else
		ignored = dialog.ok(__scriptname__,
				"%s is saved to"%subTitle,
				smiFullPath )
		# enable the downloaded subtitle
		xbmc.Player().setSubtitles(smiFullPath)

	except SearchFailed:
	    pass
	if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause

    # end of __main__
    sys.modules.clear()
