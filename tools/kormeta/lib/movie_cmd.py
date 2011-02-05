# -*- encoding: utf-8 -*-
"""
"""
import os,sys
import Tkinter,tkFileDialog
from Tkconstants import *

#from scrapers.movie.naver import MovieFetcher
from scrapers.movie.daum import MovieFetcher

class MovieCommand:
	def __init__(self,parent):
		self.dir_opt = options = {}
		options['initialdir'] = os.getcwd()
		options['mustexist'] = True
		options['parent'] = parent
		options['title'] = 'Select directory containing Movie'

		self.tk_parent = parent

		self.id = None
		self.max_backdrop = 5		# maximum number of backdrops

	def hookTextBox(self,tb):
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
			import unicodedata
			path = unicodedata.normalize('NFC', path)
		self.dir_opt['initialdir'] = path		# remember previous dir
		self.pathVar.set( path )

		self.videoPath = path
		self.videoTitle = os.path.split(path)[-1]

		self.tb.insert(END, "Movie path: %s\n" % self.videoPath)
		self.tb.insert(END, "Movie name: %s\n" % self.videoTitle)

		self.tb.insert(END, "Start searching %s...\n" % MovieFetcher.site)
		movies = MovieFetcher().Search( self.videoTitle )
		self.tb.insert(END, "%d movies found...\n" % len(movies), 'i')
		if movies:
			self.id = None
			for id,title in movies:
				self.tb.insert(END, "Movie[%s]: %s\n" % (id,title))

			if len(movies) == 1:
				self.id = movies[0][0]
			else:
				from lib.listboxchoice import ListBoxChoice
				titles = []
				for id,title in movies:
					titles.append("[%s] %s" % (id,title))
				selVal = ListBoxChoice(self.tk_parent, "Select Title", "Select one from search results", titles).returnValue()
				if selVal:
					self.id = selVal[1:selVal.index(']')]
			self.tb.insert(END, "Select %s for the given movie\n" % self.id, 'i')
		else:
			self.tb.insert(END, "No result...\n", 'e')
		self.tb.see(END)	# automatic scroll down

	def getmeta(self):
		if self.id is None:
			return
		self.tb.insert(END, "Start fetching metadata...\n")
		self.meta = MovieFetcher().ParsePage(self.id)
		self.tb.insert(END, "Metadata for %s is ready...\n" % self.id, 'i')
		self.tb.see(END)	# automatic scroll down

	def genfile(self):
		if self.id is None or self.meta.m_title is None:
			return
		if self.out_xml.get():
			outfile = os.path.join(self.videoPath, 'mymovies.xml')
			self.meta.SaveXML(outfile)
			self.tb.insert(END, "XML file, %s, is generated\n" % outfile)
			if self.out_poster.get():
				outfile = os.path.join(self.videoPath, 'folder.jpg')
				self.meta.SavePoster(outfile)
				self.tb.insert(END, "Poster file, %s, is generated\n" % outfile)
			if self.out_backdrop.get():
				self.meta.SaveBackdrops(self.videoPath, range(0,self.max_backdrop))
				self.tb.insert(END, "Backdrop files are generated\n")
		if self.out_nfo.get():
			outfile = os.path.join(self.videoPath, 'movie.nfo')
			self.meta.SaveNFO(outfile)
			self.tb.insert(END, "NFO file, %s, is generated\n" % outfile)
		self.tb.see(END)	# automatic scroll down

# vim: ts=4 sw=4
