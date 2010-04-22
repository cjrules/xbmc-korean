# -*- coding: utf-8 -*-
import sys,xbmcgui
import urllib2

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__

def download_subtitle(queryAddr, smiPath):
    req = urllib2.Request(queryAddr)
    try: resp = urllib2.urlopen(req)
    except urllib2.URLError, e:
	print e.reason
	return False
    try:
	f = open(smiPath,'w')
    except IOError:
	print "File can not be written"
	sys.exit(1)

    ###----- Download the file
    fileSz = int( resp.info()['Content-Length'] )
    stepSz = 10*1024	# 10KB step size

    dialog = xbmcgui.DialogProgress()
    ignored = dialog.create(__scriptname__, _(105) )
    sz = 0
    dialog.update( 0 )
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
	ignored = dialog.ok(__scriptname__, _(106) )
	return False

    ignored = dialog.ok(__scriptname__,
		    _(107), smiPath )
    return True
