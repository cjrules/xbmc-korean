# -*- coding: utf-8 -*-
"""
  Movie Meta Data
"""

import urllib

class MovieMetaData:
	m_id = ''
	m_title = ''
	m_year = ''
	m_cert = ''
	m_directors = []
	m_writers = []
	m_actors = []
	m_poster = ''
	m_backdrop_list = []

	def __init__(self):
		pass

	def __str__(self):
		x = [u'id: %s'%self.m_id,
			 u'title: %s'%self.m_title,
			 u'genres: %s'%'|'.join(self.m_genres),
			 u'directors: %s'%'|'.join(self.m_directors),
			 u'writers: %s'%'|'.join(self.m_writers)
			]
		y = []
		for name,role in self.m_actors:
			y.append(u'%s as %s'%(name,role))
		x.append( u'actors: '+'|'.join(y) )
		x.append( u'plot: %s'%self.m_plot )
		x.append( u'poster: %s'%self.m_poster )
		for thumb,url in self.m_backdrop_list:
			x.append( u'backdrop: %s'%url )
		return '\n'.join(x)

	#---------------------------------
	# XBMC .nfo file
	def SaveNFO(self, filename): 
		lines = []
		lines.append(u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
		lines.append(u"<movie>")
		lines.append(u"  <title>%s</title>" % self.m_title)
		lines.append(u"  <year>%s</year>" % self.m_year)
		lines.append(u"  <thumb>%s</thumb>" % self.m_poster)
		lines.append(u"  <rating>%s</rating>" % self.m_rating)
		lines.append(u"  <runtime>%s</runtime>" % self.m_runtime)
		lines.append(u"  <mpaa>%s</mpaa>" % self.m_cert)
		lines.append(u"  <director>%s</director>" % self.m_directors[0])
		lines.append(u"  <credits>%s</credits>" % ', '.join(self.m_writers) )
		for name,role in self.m_actors:
			lines.append(u"  <actor>")
			lines.append(u"    <name>%s</name>" % name)
			lines.append(u"    <role>%s</role>" % role)
			lines.append(u"  </actor>")
		lines.append(u"  <plot>%s</plot>" % self.m_plot)
		lines.append(u"  <fanart>")
		for thumb,url in self.m_backdrop_list:
			lines.append(u'    <thumb preview="%s">%s</thumb>' % (thumb,url))
		lines.append(u"  </fanart>")
		lines.append(u"</movie>")

		f = open(filename,'w')
		f.write( '\n'.join(lines).encode('utf-8') )
		f.close()

	# Windows Media Center mymovies.xml
	def SaveXML(self, filename): 
		lines = []
		lines.append(u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
		lines.append(u"<Title>")
		lines.append(u"  <LocalTitle>%s</LocalTitle>" % self.m_title)
		lines.append(u"  <OriginalTitle>%s</OriginalTitle>" % self.m_aka)
		lines.append(u"  <SortTitle>%s</SortTitle>" % self.m_title)
		lines.append(u"  <ProductionYear>%s</ProductionYear>" % self.m_year)
		lines.append(u"  <MPAARating>%s</MPAARating>" % self.m_cert)
		lines.append(u"  <RunningTime>%s</RunningTime>" % self.m_runtime)
		lines.append(u"  <Persons>")
		# Actors
		for name,role in self.m_actors:
			lines.append(u"    <Person>")
			lines.append(u"      <Name>%s</Name>" % name)
			lines.append(u"      <Type>Actor</Type>")
			lines.append(u"      <Role>%s</Role>" % role)
			lines.append(u"    </Person>")
		# Director
		for name in self.m_directors:
			lines.append(u"    <Person>")
			lines.append(u"      <Name>%s</Name>" % name)
			lines.append(u"      <Type>Director</Type>")
			lines.append(u"      <Role />")
			lines.append(u"    </Person>")
		lines.append(u"  </Persons>")
		# Genres
		lines.append(u"  <Genres>")
		for genre in self.m_genres:
			lines.append(u"    <Genre>%s</Genre>" % genre)
		lines.append(u"  </Genres>")
		# Plot
		lines.append(u"  <Description>%s</Description>" % self.m_plot)
		lines.append(u"</Title>")

		f = open(filename,'w')
		f.write( '\n'.join(lines).encode('utf-8') )
		f.close()

	def SavePoster(self, filepath): 
		f = open(filepath, "wb")
		f.write( urllib.urlopen(self.m_poster).read() )
		f.close()

	def SaveBackdrops(self, path, sel_list): 
		import os
		# save the first photo as htbackdrop.jpg
		if len(sel_list) > 0 and len(self.m_backdrop_list) >= sel_list[0]:
			#  download
			f = open( os.path.join(path,'backdrop.jpg'), "wb")
			f.write( urllib.urlopen(self.m_backdrop_list[ sel_list[0] ][1]).read() )
			f.close()
		# save photo pages
		if len(sel_list) > 1:
			count = 0
			for i in sel_list:
				if self.m_backdrop_list[i]:
					count += 1
					#  download
					f = open( os.path.join(path,'backdrop%d.jpg' % count), "wb")
					f.write( urllib.urlopen(self.m_backdrop_list[i][1]).read() )
					f.close()

if __name__ == '__main__':
	import sys,os
	libdir = os.path.join('..','..','libs')
	if not libdir in sys.path:
		sys.path.append( libdir )
	fetcher = MovieFetcher()

	print "parse"
	fetcher.ParsePage(movies[0][0])
	testdir = u'd:/videos/영화/전우치/'
	print fetcher.__str__()
	print "save metadata"
	fetcher.SaveXML( testdir+'mymovies.xml' )
	print "save poster"
	fetcher.SavePoster( testdir+'folder.jpg' )
	print "save backdrop"
	fetcher.SaveBackdrops( testdir, [0,1] )
# vim ts=4 sw=4
