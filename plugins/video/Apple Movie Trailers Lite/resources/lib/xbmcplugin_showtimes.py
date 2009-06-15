"""
Showtimes module

Nuka1195
"""

import sys
import os

import xbmc
import xbmcgui
import xbmcplugin

from urllib import unquote_plus


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class GUI( xbmcgui.WindowXMLDialog ):
    ACTION_CANCEL_DIALOG = ( 9, 10, )

    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        #xbmcgui.lock()
        self._parse_argv()
        self._get_settings()
        self._get_scraper()
        #xbmcgui.unlock()
        self.doModal()

    def onInit( self ):
        self._show_dialog()
        self._get_showtimes( movie=self.args.title, day=self.settings[ "day" ] )

    def _parse_argv( self ):
        # call _Info() with our formatted argv to create the self.args object
        exec "self.args = _Info(%s)" % ( unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ), )

    def _show_dialog( self ):
        self._set_title_info( self.args.title, "", "%s:" % ( xbmc.getLocalizedString(30602 ), ), "" )

    def _set_title_info( self, title="", location="", date="", phone="" ):
        self.clearList()
        self.setProperty( "Title", title )
        self.setProperty( "Locale", self.settings[ "local" ] )
        self.setProperty( "Location", location )
        self.setProperty( "Date", date )
        self.setProperty( "Phone", phone )
        self.addItem( xbmc.getLocalizedString( 30601 ) )

    def _get_settings( self ):
        self.settings = {}
        self.settings[ "local" ] = xbmcplugin.getSetting( "local" )
        self.settings[ "scraper" ] = xbmcplugin.getSetting( "scraper" )
        self.settings[ "day" ] = int( xbmcplugin.getSetting( "day" ) )

    def _get_scraper( self ):
        exec "import resources.scrapers.%s.showtimesScraper as showtimesScraper" % ( self.settings[ "scraper" ], )
        self.ShowtimesFetcher = showtimesScraper.ShowtimesFetcher( self.settings[ "local" ] )

    def _get_showtimes( self, movie=None, day=0 ):
        self.movie_showtimes = self.ShowtimesFetcher.get_showtimes( movie, day )
        if ( self.movie_showtimes[ "date" ] is None ):
            date = xbmc.getLocalizedString( 30600 )
        else:
            self.setProperty( "Title", self.movie_showtimes[ "title" ] )
            date = "%s: %s" % ( xbmc.getLocalizedString( 30602 ), self.movie_showtimes[ "date" ], )
        self.setProperty( "Date", date )
        self._fill_list()

    def _get_selection( self, choice ):
        self._set_title_info( self.movie_showtimes[ "theaters" ][ choice ][ 0 ], self.movie_showtimes[ "theaters" ][ choice ][ 1 ], "%s:" % ( xbmc.getLocalizedString( 30602 ), ), self.movie_showtimes[ "theaters" ][ choice][ 3 ] )
        self._get_showtimes( self.movie_showtimes[ "theaters" ][ choice ][ 4 ], int( self.movie_showtimes[ "day" ] ) )

    def _fill_list( self ):
        self.clearList()
        if ( self.movie_showtimes[ "theaters" ] ):
            for theater in self.movie_showtimes[ "theaters" ]:
                list_item = xbmcgui.ListItem( theater[ 0 ] )
                list_item.setProperty( "Address", theater[ 1 ] )
                list_item.setProperty( "ShowTimes", theater[ 2 ] )
                list_item.setProperty( "Phone", theater[ 3 ] )
                self.addItem( list_item )
        else:
            self.addItem( xbmc.getLocalizedString( 30600 ) )

    def _close_dialog( self ):
        self.close()

    def onClick( self, controlId ):
        self._get_selection( self.getCurrentListPosition() )

    def onFocus( self, controlId ):
        pass

    def onAction( self, action ):
        try:
            if ( action in self.ACTION_CANCEL_DIALOG ):
                self._close_dialog()
        except: pass
