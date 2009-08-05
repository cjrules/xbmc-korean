"""
svn repo installer plugin

Nuka1195
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import urllib
import re
from xml.sax.saxutils import unescape

from xbmcplugin_lib import *

# Script constants
__date__ = '24-06-2009'
log("Module: %s Dated: %s loaded!" % (__name__, __date__))

class Parser:
	""" Parser Class: grabs all tag versions and urls """
	# regexpressions
	revision_regex = re.compile( '<h2>.+?Revision ([0-9]*): ([^<]*)</h2>' )
	asset_regex = re.compile( '<li><a href="([^"]*)">([^"]*)</a></li>' )

	def __init__( self, htmlSource ):
		log("%s __init__!" % (self.__class__))
		# set our initial status
		self.dict = { "status": "fail", "revision": 0, "assets": [], "url": "" }
		# fetch revision number
		self._fetch_revision( htmlSource )
		# if we were successful, fetch assets
		if ( self.dict[ "revision" ] != 0 ):
			self._fetch_assets( htmlSource )

	def _fetch_revision( self, htmlSource ):
		try:
			# parse revision and current dir level
			revision, url = self.revision_regex.findall( htmlSource )[ 0 ]
			# we succeeded :), set our info
			self.dict[ "url" ] = url
			self.dict[ "revision" ] = int( revision )
		except:
			pass

	def _fetch_assets( self, htmlSource ):
		try:
			assets = self.asset_regex.findall( htmlSource )
			if ( len( assets ) ):
				for asset in assets:
					if ( asset[ 0 ] != "../" ):
						self.dict[ "assets" ] += [ unescape( asset[ 0 ] ) ]
				self.dict[ "status" ] = "ok"
		except:
			pass


class Main:
	# base path
	BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile/" ), "Thumbnails", "Pictures" )

	def __init__( self ):
		log( "%s init!" % self.__class__ )
		ok = False
		# parse sys.argv for our current url
		self._parse_argv()
		# if this is first run list all the repos
		if ( sys.argv[ 2 ] == "" ):
			ok = self._get_repos()
		else:
			# get the repository info
			repo_info = get_repo_info( self.args.repo )
			if repo_info:
				self.REPO_URL, self.REPO_ROOT, self.REPO_STRUCTURES = repo_info
				# if category is root, set our repo root
				if ( self.args.category == "root" ):
					self.args.category = self.REPO_ROOT

				# get XBMC revision
				self.XBMC_REVISION = get_xbmc_revision()
				# get the list
				ok = self._show_categories()
		# send notification we're finished, successfully or unsuccessfully
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

	def _clear_log( self, repo ):
		base_path = os.path.join( xbmc.translatePath( "special://profile/" ), "plugin_data", "programs", os.path.basename( os.getcwd() ) )
		for page in range( 3 ):
			path = os.path.join( base_path, "%s%d.txt" % ( repo, page, ) )
			# remove log file
			if ( os.path.isfile( path ) ):
				os.remove( path )

	def _parse_argv( self ):
		# if first run set title to blank
		if ( sys.argv[ 2 ] == "" ):
			self.args = Info( title="" )
		else:
			# call _Info() with our formatted argv to create the self.args object
			exec "self.args = Info(%s)" % ( urllib.unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ), )

	def _get_repos( self ):
		try:
			# we fetch the log here only at start of plugin
			#import xbmcplugin_logviewer
			# add the check for updates item to the media list
			url = "%s?category='updates'" % ( sys.argv[ 0 ], )
			# set the default icon
			icon = "DefaultFolder.png"
			# set thumbnail
			thumbnail = os.path.join( os.getcwd(), "resources", "media", "update_checker.png" )
			# create our listitem, fixing title
			listitem = xbmcgui.ListItem( xbmc.getLocalizedString( 30500 ), iconImage=icon, thumbnailImage=thumbnail )
			# set the title
			listitem.setInfo( type="Video", infoLabels={ "Title": xbmc.getLocalizedString( 30500 ) } )
			cm = [ ( xbmc.getLocalizedString( 30610 ), "XBMC.RunPlugin(%s?showreadme=True&repo=None&readme=None)" % ( sys.argv[ 0 ], ), ) ]
			listitem.addContextMenuItems( cm, replaceItems=True )
			# add our item
			ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=listitem, isFolder=True )

			# now add all the repos
			repos = load_repos()
			for repo in repos:
				cm = []
				# create the url
				url = "%s?category='root'&repo=%s&title=%s" % ( sys.argv[ 0 ], repr( urllib.quote_plus( repo ) ), repr( urllib.quote_plus( repo ) ), )
				# set thumbnail
				thumbnail = os.path.join( os.getcwd(), "resources", "media", "svn_repo.png" )
				# create our listitem, fixing title
				listitem = xbmcgui.ListItem( repo, iconImage=icon, thumbnailImage=thumbnail )
				# set the title
				listitem.setInfo( type="Video", infoLabels={ "Title": repo } )
				# grab the log for this repo
				if ( "(tagged)" not in repo ):
					#parser = xbmcplugin_logviewer.ChangelogParser( repo, parse=False )
					#parser.fetch_changelog()
					# clear logs on first run
					self._clear_log( repo )
					# add view log context menu item
					cm += [ ( xbmc.getLocalizedString( 30600 ), "XBMC.RunPlugin(%s?showlog=True&repo=%s&category=None&revision=None&parse=True)" % ( sys.argv[ 0 ], urllib.quote_plus( repr( repo ) ), ), ) ]
				# add view readme context menu item
				cm += [ ( xbmc.getLocalizedString( 30610 ), "XBMC.RunPlugin(%s?showreadme=True&repo=None&readme=None)" % ( sys.argv[ 0 ], ), ) ]
				# add context menu items
				listitem.addContextMenuItems( cm, replaceItems=True )
				# add the item to the media list
				ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=listitem, isFolder=True )
				# if user cancels, call raise to exit loop
				if ( not ok ): raise
		except:
			# user cancelled dialog or an error occurred
			logError()
			ok = False
		if ( ok ):
			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
		return ok

	def _show_categories( self ):
		ok = False
		# fetch the html source
		items = self._get_items()
		# if successful
		if ( items and items[ "status" ] == "ok" ):
			# if there are assets, we have categories
			ok = self._fill_list( items[ "url" ], items[ "revision" ], items[ "assets" ] )
		return ok

	def _fill_list( self, repo_url, revision, assets ):
		try:
			ok = False
			# enumerate through the list of categories and add the item to the media list
			for item in assets:
				cm = []
				isFolder = True
				for name, noffset, install, ioffset, voffset in self.REPO_STRUCTURES:
					try:
						if ( repo_url.split( "/" )[ int( noffset ) ].lower() == name.lower() ):
							isFolder = False
							break
					except:
						pass
				if ( isFolder ):
					heading = "category"
					thumbnail = ""
					label2 = ""
					version = ""
				else:
					heading = "download_url"
					thumbnail = "%s%s/%sdefault.tbn" % ( self.REPO_URL, repo_url.replace( " ", "%20" ), item.replace( " ", "%20" ), )
					version, label2, path = self._check_compatible( "%s%s/%sdefault.py" % ( self.REPO_URL, repo_url.replace( " ", "%20" ), item.replace( " ", "%20" ), ), self.REPO_URL, install, int( ioffset ), int( voffset ) )
					version = " (v%s)" % version
#					readme = check_readme( "%s%s/%sresources/readme.txt" % ( self.REPO_URL, repo_url, item, ) )
					readme_url_base = "%s%s/%s" % ( self.REPO_URL, repo_url, item, )
					readme = check_readme( readme_url_base )
					
				if ( label2.startswith( "[COLOR=FF00FF00]" ) or label2.startswith( "[COLOR=FFFF0000]" ) ):
					url = path
				elif "SVN%20Repo%20Installer" in item:
					# set special case if self updating
					url = '%s?self_update=True&%s="%s/%s"&repo=%s&install="%s"&ioffset=%s&voffset=%s&title=%s' % ( sys.argv[ 0 ], heading, urllib.quote_plus( repo_url ), urllib.quote_plus( item ), repr( urllib.quote_plus( self.args.repo ) ), install, ioffset, voffset, repr( urllib.quote_plus( self.args.repo ) ), )
				else:
					url = '%s?%s="%s/%s"&repo=%s&install="%s"&ioffset=%s&voffset=%s&title=%s' % ( sys.argv[ 0 ], heading, urllib.quote_plus( repo_url ), urllib.quote_plus( item ), repr( urllib.quote_plus( self.args.repo ) ), install, ioffset, voffset, repr( urllib.quote_plus( self.args.repo ) ), )
				# add uninstall item
				if ( not isFolder and not "SVN%20Repo%20Installer" in item and os.path.isfile( path ) ):
					cm +=  [ ( xbmc.getLocalizedString( 30022 ), "XBMC.RunPlugin(%s?delete=%s&title=%s&delete_from_list=True)" % ( sys.argv[ 0 ], urllib.quote_plus( repr( os.path.dirname( path ) ) ), repr( urllib.quote_plus( item[ : -1 ] ) ), ), ) ]
					
				# set the default icon
				if isFolder:
					icon = "DefaultFolder.png"
				else:
					icon = "DefaultFile.png"
				# create our listitem, fixing title
				listitem = xbmcgui.ListItem( "%s%s" % ( urllib.unquote_plus( item[ : -1 ] ), version, ), label2=label2, iconImage=icon, thumbnailImage=thumbnail )
				# set the title
				listitem.setInfo( type="Video", infoLabels={ "Title": "%s%s" % ( urllib.unquote_plus( item[ : -1 ] ), version, ), "Genre": label2 } )
				if ( not isFolder ):
					cm += [ ( xbmc.getLocalizedString( 30600 ), "XBMC.RunPlugin(%s?showlog=True&repo=%s&category=%s&revision=None&parse=True)" % ( sys.argv[ 0 ], urllib.quote_plus( repr( self.args.repo ) ), urllib.quote_plus( repr( item[ : -1 ].replace( "%20", " " )  )  ), ), ) ]
					# add context menu items
					if ( readme ):
						cm += [ ( xbmc.getLocalizedString( 30610 ), "XBMC.RunPlugin(%s?showreadme=True&repo=None&readme=%s)" % ( sys.argv[ 0 ], urllib.quote_plus( repr( readme ) ), ), ) ]
				listitem.addContextMenuItems( cm, replaceItems=True )
				# add the item to the media list
				ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=listitem, isFolder=isFolder, totalItems=len( assets ) )
				# if user cancels, call raise to exit loop
				if ( not ok ): raise
		except:
			# user cancelled dialog or an error occurred
			logError()
			ok = False
		if ( ok ):
			# set our plugin category
			xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
			# sort by genre so all update status' are grouped
			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
		return ok

	def _check_compatible( self, url, repo_url, install, ioffset, voffset ):
		log("_check_compatible() url=%s" % url)
		try:
			# get items svn info
			ok = True
			version = xbmc.getLocalizedString( 30013 )
			htmlSource = readURL( url )

			# parse source for revision and version
			version = parseDocTag( htmlSource, "version")
			revision = int(parseDocTag( htmlSource, "XBMC_Revision"))
			# compatible - 0 == unknown, so allow it
			ok = bool((not self.XBMC_REVISION) or (self.XBMC_REVISION >= revision))
		except:
			pass

		# create path
		items = url.replace( repo_url, "" ).split( "/" )
		# base path
		drive = xbmc.translatePath( "/".join( [ "special://home", install ] ) )
		if ( voffset != 0 ):
			items[ voffset - 1 ] = "%s - %s" % ( items[ voffset - 1 ].replace( "%20", " " ), items[ voffset ], )
			del items[ voffset ]
		path = os.path.join( drive, os.path.sep.join( items[ ioffset : ] ).replace( "%20", " " ) )

		# make label2 according to state
		if ( not ok ):
			verState = "v%s (%s)" % ( version, xbmc.getLocalizedString( 30015 ), )		# eg. Incompatible
		elif not ( os.path.isfile( path ) ):
			verState = xbmc.getLocalizedString( 30021 )									# install
		else:
			# read installed path
			htmlSource = open( path, "r" ).read()
			# parse source for version
			ver = parseDocTag( htmlSource, "version" )
			if not ver or version > ver:
				verState = "v%s (%s)" % ( version, xbmc.getLocalizedString( 30014 ) )   # New
			else:
				verState = xbmc.getLocalizedString( 30011 )								# OK
			version = ver		# so it shows current installed version

		label2 = makeLabel2( verState )
		return version, label2, path

	def _get_items( self ):
		try:
			# open url
			url = self.REPO_URL + self.args.category
			htmlSource = readURL( url )
			# parse source and return a dictionary
			return Parser( htmlSource ).dict
		except:
			# oops print error message
			print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
			return {}
