# -*- coding: utf-8 -*-
"""
"""
import os,sys
import Tkinter,tkFileDialog
from Tkconstants import *

class MusicCommand:
	def __init__(self,parent):
		self.dir_opt = options = {}
		options['initialdir'] = os.getcwd()
		options['mustexist'] = True
		options['parent'] = parent
		options['title'] = 'Select Artist directory'

		self.tk_parent = parent

		self.artist_id = None
		self.album_id = []

	def hookTextBox(self, tb):
		self.tb = tb
	def hookPath(self,pathVar):
		self.pathVar = pathVar
	def hookSel(self,nfo,xml,poster,backdrop):
		self.out_nfo = nfo
		self.out_xml = xml
		self.out_poster = poster
		self.out_backdrop = backdrop

	def getdir(self):
		path = tkFileDialog.askdirectory(**self.dir_opt)
		if path is '':
			return
		if sys.platform is 'darwin':
			path = unicodedata.normalize('NFC', path)
		self.dir_opt['initialdir'] = path		# remember previous dir
		self.pathVar.set( path )

		self.musicPath = path
		self.artistName = os.path.split(path)[-1]

		self.tb.insert(END, "Music path: %s\n" % self.musicPath)
		self.tb.insert(END, "Artist name: %s\n" % self.artistName)

		self.artist_id = None

		self.tb.insert(END, "Start searching artist...\n")
		from scrapers.artist.melon import ArtistFetcher
		artists = ArtistFetcher().Search( self.artistName )
		self.tb.insert(END, "%d artists found...\n" % len(artists), 'i')
		for id,name in artists:
			self.tb.insert(END, "Artist[%s]: %s\n" % (id,name))
		if artists:
			if len(artists) == 1:
				self.artist_id = artists[0][0]
			else:
				from lib.listboxchoice import ListBoxChoice
				names = []
				for id,name in artists:
					names.append("[%s] %s" % (id,name))
				selVal = ListBoxChoice(self.tk_parent, "Select Title", "Select one from search results", names).returnValue()
				if selVal:
					self.artist_id = selVal[1:selVal.index(']')]
			if self.artist_id:
				self.tb.insert(END, "Select %s for the given artist\n" % self.artist_id, 'i')
		else:
			self.tb.insert(END, "No result...\n", 'e')

		# scan album directories under artist directory
		self.album_id = []
		self.albumPath = []
		for album_dir in os.listdir( self.musicPath ):
			albumPath = os.path.join(self.musicPath,album_dir)
			if not os.path.isdir( albumPath ):
				continue
			self.albumPath.append( albumPath )
			self.tb.insert(END, "Start searching album...\n")
			from scrapers.album.melon import AlbumFetcher
			albums = AlbumFetcher().Search( album_dir, self.artistName )
			self.tb.insert(END, "%d albums found...\n" % len(albums), 'i')
			for id,title,artist in albums:
				self.tb.insert(END, "Albums[%s]: %s (%s)\n" % (id,title,artist))
			album_id = ''
			if albums:
				if len(albums) == 1:
					album_id = albums[0][0]
				else:
					from gui.listboxchoice import ListBoxChoice
					names = []
					for id,title,artist in albums:
						names.append("[%s] %s (%s)" % (id,title,artist))
					selVal = ListBoxChoice(self, "Select Title", "Select one from search results", names).returnValue()
					if selVal:
						album_id = selVal[1:selVal.index(']')]
				if album_id:
					self.tb.insert(END, "Select %s for the given album\n" % album_id, 'i')
			else:
				self.tb.insert(END, "No result...\n", 'e')
			self.album_id.append( album_id )

		self.tb.see(END)	# automatic scroll down

	def getmeta(self):
		if self.artist_id is None:
			return

		self.artist_meta = None
		self.tb.insert(END, "Start fetching artist metadata...\n")
		from scrapers.artist.melon import ArtistFetcher
		self.artist_meta = ArtistFetcher().ParsePage(self.artist_id)
		self.tb.insert(END, "Metadata for %s is ready...\n" % self.artist_id, 'i')

		self.album_meta = []
		for id in self.album_id:
			self.tb.insert(END, "Start fetching album metadata...\n")
			from scrapers.album.melon import AlbumFetcher
			self.album_meta.append( AlbumFetcher().ParsePage(id) )
			self.tb.insert(END, "Metadata for %s is ready...\n" % id, 'i')

		self.tb.see(END)	# automatic scroll down

	def genfile(self):
		if self.artist_meta is None:
			return
		if self.out_nfo.get():
			outfile = os.path.join(self.musicPath, 'artist.nfo')
			self.artist_meta.SaveNFO(outfile)
			self.tb.insert(END, "NFO file, %s, is generated\n" % outfile)

		for i in range(0,len(self.albumPath)):
			path = self.albumPath[0]
			meta = self.album_meta[0]
			if self.out_nfo.get():
				outfile = os.path.join(path, 'album.nfo')
				meta.SaveNFO(outfile)
				self.tb.insert(END, "NFO file, %s, is generated\n" % outfile)

		self.tb.see(END)	# automatic scroll down

if __name__ == "__main__":
	pass
# vim: ts=4 sw=4
