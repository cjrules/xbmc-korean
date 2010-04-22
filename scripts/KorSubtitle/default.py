# -*- coding: utf-8 -*-
import sys,os,xbmc

__scriptname__ = "KorSubtitle"
__scriptid__   = "com.xbmc-korea.subtitle.script"
__author__     = "xbmc-korea.com"
__url__        = "http://code.google.com/p/xbmc-korean"
__svn_url__    = "http://code.google.com/p/xbmc-korean/svn/trunk/scripts/KorSubtitle"
__credits__    = ""
__version__    = "1.0.0"

if not xbmc.getCondVisibility('Player.Paused') : xbmc.Player().pause()	    #Pause if not paused

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)

__language__ = xbmc.Language( os.getcwd() ).getLocalizedString
_ = sys.modules[ "__main__" ].__language__
__settings__ = xbmc.Settings( path=os.getcwd() )    # old-stype script

from gomtv_jmdb import *
from qple_jamak import *
from subt_down  import *

#############-----------------Is script runing from OSD? -------------------------------###############
if not xbmc.getCondVisibility('videoplayer.isfullscreen') :
    __settings__.openSettings()
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

        movieFullPath = xbmc.Player().getPlayingFile()
	smiFullPath = movieFullPath[:movieFullPath.rfind('.')]+'.smi'
        
        try:
            f=open(movieFullPath,"rb")
        except IOError:
            print "File can not be open"
            sys.exit(1)

	###----- fetch list of available subtitles
	subt_list = []
	dialog = xbmcgui.DialogProgress()
	ignored = dialog.create(__scriptname__ )
	if __settings__.getSetting( "GomTV" )=='true':
	    dialog.update( 0, _(100) )
	    subt_list += gomtv_jamak_from_file(f)
	if __settings__.getSetting( "Qple" )=='true':
	    dialog.update( 50, _(101) )
	    subt_list += qple_jamak_from_file(f)
	dialog.close()
	f.close()

	###----- select a subtitle to download
	if len(subt_list)==0:
	    dialog = xbmcgui.Dialog()
	    ignored = dialog.ok(__scriptname__,
			    _(102)%os.path.basename(movieFullPath) )
	else:
	    title_list = []
	    for i in range(0,len(subt_list)):
		if subt_list[i][0] == 'gomtv':
		    title = "[Gom] "+subt_list[i][1]
		elif subt_list[i][0] == 'qple':
		    title = "[Qpl] "+subt_list[i][1]
		else:
		    title = subt_list[i][1]
		title_list.append( title )
	    print title_list

	    dialog = xbmcgui.Dialog()
	    selected = dialog.select( _(103)%len(title_list), title_list )

	    if selected >= 0:
		if subt_list[selected][0] == 'gomtv':
		    smiAddr = gomtv_jamak_url( subt_list[selected][2] )
		else:
		    smiAddr = subt_list[selected][2]

		if download_subtitle(smiAddr, smiFullPath):
		    # enable the downloaded subtitle
		    xbmc.Player().setSubtitles(smiFullPath)

	if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause
	sys.modules.clear()
    # end of __main__
