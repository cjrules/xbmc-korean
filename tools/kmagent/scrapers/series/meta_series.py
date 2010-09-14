# -*- coding: utf-8 -*-
"""
  Retrieve medata for TV series from Daum
"""

import urllib

class SeriesMetaData:
	s_id	= ''
	s_title = ''
	s_year  = ''
	s_plot  = ''
	s_directors = []
	s_writers   = []
	s_actors	= []
	s_network = ''
	s_aired = ''
	s_poster = ''
	s_backdrop_list = []

	EpisodeInfo = {};

	def __init__(self): 
		pass

	#------------------------------------------
	# for tvshow.nfo
	def __str__(self):
		lines = [u'id: %s'%self.s_id,
			 u'title: %s'%self.s_title,
			 u'directors: %s'%'|'.join(self.s_directors),
			 u'writers: %s'%'|'.join(self.s_writers)
			]
		acs = []
		for name,role in self.s_actors:
			acs.append(u'%s as %s'%(name,role))
		lines.append( u'actors: '+'|'.join(acs) )
		lines.append( u'plot: %s'%self.s_plot )
		lines.append( u'poster: %s'%self.s_poster )
		return '\n'.join(lines)

	def SaveSeriesNFO(self, filename): 
		lines = []
		lines.append(u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
		lines.append(u"<tvshow>")
		lines.append(u"  <title>%s</title>" % self.s_title)
		lines.append(u"  <year>%s</year>" % self.s_year)
		lines.append(u"  <thumb>%s</thumb>" % self.s_poster)
		lines.append(u"  <studio>%s</studio>" % self.s_network)
		lines.append(u"  <premiered>%s</premiered>" % self.s_aired)
		lines.append(u"  <director>%s</director>" % self.s_directors[0])
		lines.append(u"  <credits>%s</credits>" % ', '.join(self.s_writers) )
		for name,role in self.s_actors:
			lines.append(u"  <actor>")
			lines.append(u"    <name>%s</name>" % name)
			lines.append(u"    <role>%s</role>" % role)
			lines.append(u"  </actor>")
		lines.append(u"  <plot>%s</plot>" % self.s_plot)
		lines.append(u"  <fanart>")
		for thumb,url in self.s_backdrop_list:
			lines.append(u'    <thumb preview="%s">%s</thumb>' % (thumb,url))
		lines.append(u"  </fanart>")
		lines.append(u"</tvshow>")

		f = open(filename,'w')
		f.write( '\n'.join(lines).encode('utf-8') )
		f.close()

	# for series.xml
	def SaveSeriesXML(self, filename): 
		lines = []
		lines.append(u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
		lines.append(u"<Series>")
		lines.append(u"  <id>%s</id>" % self.s_id)
		lines.append(u"  <SeriesName>%s</SeriesName>" % self.s_title)
		temp = []
		for name,role in self.s_actors:
			temp.append(name)
		lines.append(u"  <Actors>|%s|</Actors>" % '|'.join(temp) )
		lines.append(u"  <ContentRating>%s</ContentRating>" % self.s_rating)
		lines.append(u"  <FirstAired>%s</FirstAired>" % self.s_aired)
		lines.append(u"  <Genre>|%s|</Genre>" % '|'.join(self.s_genres) )
		lines.append(u"  <Overview>%s</Overview>" % self.s_plot)
		lines.append(u"  <Network>%s</Network>" % self.s_network)
		lines.append(u"</Series>")

		f = open(filename,'w')
		f.write( '\n'.join(lines) )
		f.close()

	# for <episode>.nfo
	def SaveEpisodeNFO(self, season, episode, filename): 
		if self.EpisodeInfo.has_key( (season,episode) ):
			temp = self.EpisodeInfo[(season,episode)]
			result = True
		else:
			temp = [u"제%d회"%episode, "", ""]			# dummy info
			result = False
		lines = []
		lines.append(u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
		lines.append(u"<episode>")
		lines.append(u"  <title>%s</title>" % temp[0])
		lines.append(u"  <season>%d</season>" % season)
		lines.append(u"  <episode>%d</episode>" % episode)
		lines.append(u"  <aired>%s</aired>" % temp[1])
		lines.append(u"  <plot>%s</plot>" % temp[2])
		lines.append(u"</episode>")

		f = open(filename,'w')
		f.write( '\n'.join(lines).encode('utf-8') )
		f.close()
		return result

	# for <episode>.xml
	def SaveEpisodeXML(self, season, episode, filename): 
		if not self.EpisodeInfo.has_key( (season,episode) ):
			return
		temp = self.EpisodeInfo[(season,episode)]
		lines = []
		lines.append(u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
		lines.append(u"<Item>")
		lines.append(u"  <EpisodeName>%s</EpisodeName>" % temp[0])
		lines.append(u"  <SeasonNumber>%d</SeasonNumber>" % season)
		lines.append(u"  <EpisodeNumber>%d</EpisodeNumber>" % episode)
		lines.append(u"  <FirstAired>%s</FirstAired>" % temp[1])
		lines.append(u"  <Overview>%s</Overview>" % temp[2])
		lines.append(u"</Item>")

		f = open(filename,'w')
		f.write( '\n'.join(lines) )
		f.close()

	def SavePoster(self, filepath): 
		f = open(filepath, "wb")
		f.write( urllib.urlopen(self.s_poster).read() )
		f.close()

	def SaveBackdrops(self, path, sel_list): 
		import os
		# save the first photo as htbackdrop.jpg
		if len(sel_list) > 0 and len(self.s_backdrop_list) >= sel_list[0]:
			#  download
			f = open( os.path.join(path,'backdrop.jpg'), "wb")
			f.write( urllib.urlopen(self.s_backdrop_list[ sel_list[0] ][1]).read() )
			f.close()
		# save photo pages
		if len(sel_list) > 1:
			count = 0
			for i in sel_list:
				if self.s_backdrop_list[i]:
					count += 1
					#  download
					f = open( os.path.join(path,'backdrop%d.jpg' % count), "wb")
					f.write( urllib.urlopen(self.s_backdrop_list[i][1]).read() )
					f.close()

	def GetEpisodeListXML(self,server):
		lines = []
		for key,val in sorted(self.EpisodeInfo.items(), key=lambda x: x[0][1], reverse=True):
		    lines.append(u"<episode>")
		    #lines.append(u"<title>%s</title>" % val[0])
		    lines.append(u"<season>%d</season>" % key[0])
		    lines.append(u"<epnum>%d</epnum>" % key[1])
		    lines.append(u"<url>%s&ep=%d</url>" % (val[3],key[1]))
		    #lines.append(u"<url>%s</url>" % server % key)
		    lines.append(u"</episode>")
		return ''.join(lines).encode('utf-8')

	def GetEpisodeDetailXML(self,season,episode):
		if not self.EpisodeInfo.has_key( (season,episode) ):
			return ""
		temp = self.EpisodeInfo[(season,episode)]
		lines = []
		lines.append(u"<details>")
		lines.append(u"<title>%s</title>" % temp[0])
		lines.append(u"<aired>%s</aired>" % temp[1])
		lines.append(u"<plot>%s</plot>" % temp[2])
		lines.append(u"</details>")
		return ''.join(lines).encode('utf-8')

if __name__ == '__main__':
	meta = SeriesMetaData()

	print meta.__str__()
	#testdir = u'd:/videos/드라마/지붕 뚫고 하이킥/'
	testdir = u'd:/videos/드라마/모래시계/'
	#print "save series metadata"
	#fetcher.SaveSeriesNFO( testdir+'tvshows.nfo' )
	#print "save poster"
	#fetcher.SavePoster( testdir+'folder.jpg' )
	#print "save backdrop"
	#fetcher.SaveBackdrops( testdir, [1] )

	print "save episode metadata"
	if fetcher.EpisodeFound:
		for epnum in [1, 100]:
			filename = testdir + "1x%d_test.nfo" % epnum
			#fetcher.SaveEpisodeNFO(1, epnum, filename)
# vim: ts=4 sw=4
