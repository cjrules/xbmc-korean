import sys
import os

import xbmc
import xbmcgui
import xbmcplugin


class _ButtonIndexError:
    pass


class DirectoryItem:
    def __init__( self, *args, **kwargs ):
        self.url = ""
        self.listitem = ""
        self.isFolder = False
        self.totalItems = 0


class MediaWindow:
    """ Media window class utilities """
    # constants
    BUTTON_MIN = 1
    BUTTON_MAX = 10
    
    def __init__( self, hId, wId=None, category=None, content=None, sortmethods=None, fanart=None ):
        # set our handle id
        self.m_handle = hId
        # get the current window if no window id supplied
        if ( wId is None ):
            self.m_window = xbmcgui.Window( xbmcgui.getCurrentWindowId() )
        else:
            self.m_window = xbmcgui.Window( wId )
        # reset button counter
        self.m_buttonId = 0
        # set plugin category property
        if ( category is not None ):
            xbmcplugin.setPluginCategory( handle=self.m_handle, category=category )
        # set plugin content
        if ( content is not None ):
            xbmcplugin.setContent( handle=self.m_handle, content=content )
        # set plugin sortmethods
        self._setSortMethods( sortmethods )
        # set fanart
        self._setFanart( fanart )

    def _setSortMethods( self, sortmethods ):
        # if there are sortmethods add them
        if ( sortmethods is not None ):
            # enumerate thru and add each sort method
            for sortmethod in sortmethods:
                xbmcplugin.addSortMethod( self.m_handle, sortmethod )

    def _setFanart( self, fanart ):
        # if user passed fanart tuple (path, method,)
        if ( fanart is not None ):
            # if skin has fanart image use it
            fanart_image = os.path.join( sys.modules[ "__main__" ].__plugin__, fanart[ 1 ] + "-fanart.png" )
            if ( xbmc.skinHasImage( fanart_image ) ):
                xbmcplugin.setPluginFanart( handle=self.m_handle, image=fanart_image )
            # set our fanart from user setting
            elif ( fanart[ 0 ] ):
                xbmcplugin.setPluginFanart( handle=self.m_handle, image=fanart[ 0 ] )

    def add( self, item ):
        return xbmcplugin.addDirectoryItem( handle=self.m_handle, url=item.url, listitem=item.listitem, isFolder=item.isFolder, totalItems=item.totalItems )

    def end( self, succeeded=True ):
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=self.m_handle, succeeded=succeeded )

    def setButton( self, label, onclick=None, onfocus=None, onunfocus=None, bId=None ):
        # increment bId if none supplied
        if ( bId is None ):
            bId = self.m_buttonId + 1
        # if it's not a valid button id raise button error
        if ( not ( self.BUTTON_MIN <= bId <= self.BUTTON_MAX ) ):
            raise _ButtonIndexError
        # set the counter
        self.m_buttonId = bId
        # localize label if it's an integer
        try:
            id = int( label )
            label = xbmc.getLocalizedString( id )
        except:
            pass
        # set button label property
        self.m_window.setProperty( "PluginButton%s.Label" % bId, label )
        # set optional button properties
        if ( onclick is not None ):
            self.m_window.setProperty( "PluginButton%s.OnClick" % bId, onclick )
        if ( onfocus is not None ):
            self.m_window.setProperty( "PluginButton%s.OnFocus" % bId, onfocus )
        if ( onunfocus is not None ):
            self.m_window.setProperty( "PluginButton%s.OnUnFocus" % bId, onunfocus )
