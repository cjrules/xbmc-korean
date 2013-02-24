# -*- coding: utf-8 -*-
"""
  Download subtitle from Korean sites
"""
import sys,os
import xbmc,xbmcaddon

__addon__ = xbmcaddon.Addon()
__scriptname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
__cwd__ = __addon__.getAddonInfo('path')

_ = __language__

if not xbmc.getCondVisibility('Player.Paused') : xbmc.Player().pause()  #Pause if not paused

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)

from gui import *

#############-----------------Is script runing from OSD? -------------------------------###############
if not xbmc.getCondVisibility('videoplayer.isfullscreen') :
  __addon__.openSettings()
  if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause
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

  print "KorSubtitle version [" +  __version__ +"]"
  print "Skin Folder: [ " + skin1 +" ]"
  print "KorSubtitle skin XML: [ " + skin +" ]"
   
  if ( __name__ == "__main__" ):
    # main body
    gui()

    if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause
    sys.modules.clear()
  # end of __main__
# vim: softtabstop=2 shiftwidth=2 expandtab
