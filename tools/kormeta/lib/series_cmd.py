# -*- coding: utf-8 -*-
"""
"""
import os,sys
import Tkinter,tkFileDialog
from Tkconstants import *

class SeriesCommand:
	def __init__(self,parent):
		self.dir_opt = options = {}
		options['initialdir'] = os.getcwd()
		options['mustexist'] = True
		options['parent'] = parent
		options['title'] = 'Select directory containing Series'

		self.tk_parent = parent

		self.id = None
		self.max_backdrop = 3	# maximum number of backdrops

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
			path = unicodedata.normalize('NFC', path)
		self.dir_opt['initialdir'] = path		# remember previous dir
		self.pathVar.set( path )

		self.videoPath = path
		self.videoTitle = os.path.split(path)[-1]

		self.tb.insert(END, "TV series path: %s\n" % self.videoPath)
		self.tb.insert(END, "TV series name: %s\n" % self.videoTitle)

		from lib.localscan import LocalScan
		scan = LocalScan()
		self.tb.insert(END, "Scan episode files...\n")
		avifiles = scan.ScanVideo( self.videoPath )
		self.epfiles = scan.GetEpisodeInfo(avifiles)
		self.tb.insert(END, "%d episode files found...\n" % len(self.epfiles), 'i')

		from scrapers.series.daum import SeriesFetcher
		self.fetcher = SeriesFetcher()

		self.tb.insert(END, "Start searching Daum...\n")
		series = self.fetcher.Search( self.videoTitle )
		self.tb.insert(END, "%d series found...\n" % len(series), "i")
		if series:
			self.id = None
			for id,title in series:
				self.tb.insert(END, "Series[%s]: %s\n" % (id,title))

			if len(series) == 1:
				self.id = series[0][0]
			else:
				from lib.listboxchoice import ListBoxChoice
				titles = []
				for id,title in series:
					titles.append("[%s] %s" % (id,title))
				selVal = ListBoxChoice(self.tk_parent, "Select Title", "Select one from search results", titles).returnValue()
				if selVal:
					self.id = selVal[1:selVal.index(']')]
			self.tb.insert(END, "Select %s for the given series\n" % self.id, 'i')
		else:
			self.tb.insert(END, "No result...\n", 'e')
		self.tb.see(END)	# automatic scroll down

	def getmeta(self):
		if self.id is None:
			return
		self.tb.insert(END, "Start fetching metadata...\n")
		self.meta = self.fetcher.ParseSeriesPage(self.id)
		self.tb.insert(END, "Metadata is ready...\n", 'i')
		self.tb.see(END)	# automatic scroll down

	def genfile(self):
		if self.id is None or self.meta.s_title is None:
			return
		if self.out_xml.get():
			outfile = os.path.join(self.videoPath, 'series.xml')
			self.meta.SaveSeriesXML(outfile)
			self.tb.insert(END, "XML file, %s, is generated\n" % outfile)
			# copy cover & backdrop
			if self.out_poster.get():
				outfile = os.path.join(self.videoPath, 'folder.jpg')
				self.meta.SavePoster(outfile)
				self.tb.insert(END, "Poster file, %s, is generated\n" % outfile)
			if self.out_backdrop.get():
				self.meta.SaveBackdrops(self.videoPath, range(0,self.max_backdrop))
				self.tb.insert(END, "Backdrop file is generated\n")
		if self.out_nfo.get():
			outfile = os.path.join(self.videoPath, 'tvshow.nfo')
			self.meta.SaveSeriesNFO(outfile)
			self.tb.insert(END, "NFO file, %s, is generated\n" % outfile)

		if self.epfiles is None:
			self.tb.insert(END, "No episode info found in site...\n", "e")
		else:
			self.tb.insert(END, "Fetching episode metadata...\n")
			self.fetcher.ParseEpisodePageList(self.id)
			self.tb.insert(END, "Episode metadata is ready...\n", 'i')
			for epnum,epfile in self.epfiles:
				outpath = os.path.splitext(epfile)
				if self.out_xml.get() and self.meta.EpisodeList[ (self.fetcher.Season,epnum) ]:
					outfile = outpath[0]+'.xml'
					self.meta.SaveEpisodeXML(self.fetcher.Season, epnum, outfile)
					self.tb.insert(END, "XML file, %s, is generated\n" % outfile)
				if self.out_nfo.get():
					# if no episode info exists, then makes dummy file
					outfile = outpath[0]+'.nfo'
					if self.meta.SaveEpisodeNFO(self.fetcher.Season, epnum, outfile):
						self.tb.insert(END, "NFO file, %s, is generated\n" % outfile)
					else:
						self.tb.insert(END, "NFO file, %s, is generated in default\n" % outfile)
		self.tb.see(END)	# automatic scroll down

# vim: ts=4 sw=4
