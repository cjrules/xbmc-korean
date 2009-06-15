"""
    Plugin for viewing your Picasa Web Albums content
"""

# main imports
import sys
import xbmc

# plugin constants
__plugin__ = "Picasa"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/Picasa"
__version__ = "1.3.5"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        from PicasaAPI import xbmcplugin_categories as plugin
    elif ( "category='presets_photos'" in sys.argv[ 2 ] ):
        from PicasaAPI import xbmcplugin_categories as plugin
    elif ( "category='presets_users'" in sys.argv[ 2 ] ):
        from PicasaAPI import xbmcplugin_categories as plugin
    else:
        from PicasaAPI import xbmcplugin_photos as plugin
    plugin.Main()
