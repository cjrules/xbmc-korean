# -*- coding: utf-8 -*-
"""
  Download subtitle continuously
"""
import sys,os
import xbmc,xbmcgui,xbmcvfs
import urllib2

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__

def download_subtitle(queryAddr, smiPath):
  try: resp = urllib2.urlopen(queryAddr)
  except urllib2.URLError, e:
    print e.reason
    xbmcgui.Dialog().ok(__scriptname__, _(109), _(108) )
    return None

  smiTempPath = xbmc.translatePath( "special://temp/" + os.path.basename(smiPath) )
  try:
    f = open(smiTempPath,'w')
  except IOError:
    xbmc.log("Not writable temp directory", xbmc.LOGERROR)
    return None

  ###----- Download the file
  fileSz = int( resp.info()['Content-Length'] )
  stepSz = 10*1024        # 10KB step size

  dialog = xbmcgui.DialogProgress()
  dialog.create(__scriptname__, _(105) )
  sz = 0
  dialog.update( 0 )
  while True:
    if dialog.iscanceled():
      break
    buf = resp.read(stepSz)
    if not buf: break
    sz += len(buf)
    f.write( buf )
    dialog.update( 100*sz/fileSz )
  f.close(); resp.close()
  dialog.close()

  if sz < fileSz:
    xbmcgui.Dialog().ok(__scriptname__, _(106) )
    return None

  ###----- Try to store in the original path
  ok = xbmcvfs.copy(smiTempPath, smiPath)
  if not ok:
    xbmc.log("Not writable movie directory", xbmc.LOGWARNING)
    xbmcgui.Dialog().ok(__scriptname__, _(110), _(107), smiTempPath )
    return smiTempPath
  os.remove(smiTempPath)
  xbmcgui.Dialog().ok(__scriptname__, _(107), smiPath )
  return smiPath
# vim: softtabstop=2 shiftwidth=2 expandtab
