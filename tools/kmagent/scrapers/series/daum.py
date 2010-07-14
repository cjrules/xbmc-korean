# -*- coding: utf-8 -*-
"""
  Retrieve medata for TV series from Daum
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_series import SeriesMetaData

class SeriesFetcher:
	meta = None

	EpisodeFound = False
	Season = 1;

	def __init__(self): 
		self.base_url	= "http://movie.daum.net"
		self.search_url  = self.base_url+"/search.do?type=tv&q=%s"
		self.details_url = self.base_url+"/tv/detail/main.do?tvProgramId=%s"
		self.cast_url	= self.base_url+"/tv/detail/castcrew.do?tvProgramId=%s"
		self.photo_url   = self.base_url+"/tv/detail/photo/list.do?tvProgramId=%s&order=recommend"
		self.episode_base_url = self.base_url+"/tv/detail/episode.do"
		self.episode_url = self.episode_base_url+"?tvProgramId=%s"
		self.striptags = re.compile('<.*?>',re.U)
		self.meta = SeriesMetaData()

	# search with title
	def Search(self,title): 
		resp = urllib.urlopen( self.search_url % urllib.quote_plus(title.encode('utf-8')) );
		print self.search_url % urllib.quote_plus(title.encode('utf-8'))
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
		result = []
		for item in soup.findAll("span",{"class" : "fl srch"}):
			id = re.compile("tvProgramId=(\d+)").search(item.find('a')['href']).group(1)
			if item.a.b is None:
				title = item.a.string
			else:
				title = item.a.b.string
			result.append( (id,title) )
		return result

	def ParseSeriesPage(self,id):
		resp = urllib.urlopen( self.details_url % id );
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")

		strain = SoupStrainer("div",{"id" : "tvInfoDetail"})
		header = soup.find(strain).find("p",{"class":"header"})
		self.meta.s_title = header.strong.string		# class=title_kor
		self.meta.s_year = header.em.string[1:-1]
		aka = header.find("em",{"class":"title_AKA"})
		temp = aka.find("span",{"class":"eng"})
		if temp:
			self.meta.s_aka = temp.string
		else:
			self.meta.s_aka = aka.contents and aka.contents[0]

		self.meta.s_genres = []
		sect = soup.find("dl",{"class":"cu mainInfo"}).find("span",{"class" : "baseinfo"})
		pts = self.striptags.sub('',sect.renderContents()).split('|')
		self.meta.s_network = pts[0].strip()

		self.meta.s_rating = float( soup.find("span",{"class":"star_big pink"}).em.string )
		self.meta.s_poster = re.compile('C\d{3}x\d{3}').sub('image', soup.find('p', {"class" : "poster"}).a.img['src'])
		self.meta.s_plot = self.striptags.sub('', soup.find("div",{"id":"synopsis"}).find("div",{"class":"txt"}).renderContents()).strip()
		self.meta.s_plot = unicode(self.meta.s_plot.replace("&#39;","'"),'utf-8')

		self.meta.s_id = id
		self.meta.s_directors = []
		self.meta.s_writers = []
		self.meta.s_actors = []
		self.meta.s_backdrop_list = []

		self.ParseSeriesCastPage(id)
		self.ParseSeriesPhotoPageList(id)

		return self.meta

	def ParseSeriesCastPage(self,id):
		resp = urllib.urlopen( self.cast_url % id );
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")

		pt = soup.find("h5",text=re.compile(u"^\s*출연\s*$"))
		if pt:
			for item in pt.parent.parent.findAll("dl"):
				name = item.find('img')['alt'].strip()
				role = item.find('span',{"class" : "etcs"}).string.strip()
				if role.rfind(u" 역") >= 0:
					role = role[:role.rfind(u" 역")]
				else:
					role = ''
				self.meta.s_actors.append( (name,role) )

		pt = soup.find("h5",text=re.compile(u"^\s*제작진\s*$"))
		if pt:
			for item in pt.parent.parent.findAll('li'):
				if item.contents[0].string.startswith(u"극본"):
					for person in item.contents[1:]:
						name = person.string.strip()
						if name:
							self.meta.s_writers.append(name)
				elif item.contents[0].string.startswith(u"연출"):
					for person in item.contents[1:]:
						name = person.string.strip()
						if name:
							self.meta.s_directors.append(name)

	def ParseSeriesPhotoPageList(self,id):
		this_url = self.photo_url % id
		self.ParseSeriesPhotoPage(this_url)

		resp = urllib.urlopen( this_url )
		strain = SoupStrainer("div",{"id" : "photoViewer"})
		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
		for page in soup.find("div",{"class" : "pagination"}).findAll('a'):
			url = self.base_url+page['href']
			self.ParseSeriesPhotoPage(url)

	def ParseSeriesPhotoPage(self,url):
		resp = urllib.urlopen( url )
		strain = SoupStrainer("div",{"id" : "photoViewer"})
		soup = BeautifulSoup(resp.read(),strain,fromEncoding="utf-8")
		for item in soup.find("table",{"id" : "tPicTop"}).findAll("td"):
			img = item.find('img')['src']
			self.meta.s_backdrop_list.append( (img, re.sub('S\d{3}x\d{3}', 'image', img)) )

	#------------------------------------------
	def ParseEpisodePageList(self,id):
		self.ParseEpisodePageListByUrl( self.episode_url % id )

	def ParseEpisodePageListByUrl(self,url):
		self.EpisodeFound = False
		#print url
		resp = urllib.urlopen(url);
		if not resp: return			# uncommon

		soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
		if soup.find("p", {"class" : "sorry"}):
			return			# not supported
		self.EpisodeFound = True
		self.GetEpisodeInfoByContent(soup)

		curpg = soup.find('span', {"class" : "current"})
		for pg in curpg.findNextSiblings('a'):
			url = self.episode_base_url+pg['href']
			if '~' in pg.contents[0]:
				self.ParseEpisodePageListByUrl(url)
			else:
				resp = urllib.urlopen(url)
				self.GetEpisodeInfoByContent( BeautifulSoup(resp.read(),fromEncoding="utf-8") )

	def GetEpisodeInfoByContent(self,soup):
		for item in soup.findAll('li',{'id' : re.compile("^itemId_")}):
			epnum = item['id'][item['id'].rfind('_')+1:]
			titles = item.find("span",{"class" : "episode_num"}).string.split('&nbsp;')
			plot = unicode( self.striptags.sub('',item.find("p",{"class" : "txt"}).renderContents()).strip(), 'utf-8' )
			self.meta.EpisodeInfo[(self.Season,int(epnum))] = (titles[0], " ".join(titles[1:]), plot)
			#print "%s:%s:%s" % (epnum,titles[0]," ".join(titles[1:]))

if __name__ == '__main__':
	fetcher = SeriesFetcher()

	print "search series"
	series = fetcher.Search(u"지붕 뚫고 하이킥")
	for id,title in series:
		print "%s: %s" % (id,title)

	id = series[0][0]
	print "parse series"
	meta = fetcher.ParseSeriesPage(id)
	print meta.__str__()

	import os
	testdir = os.path.join('d:'+os.sep,'Videos','드라마','지붕 뚫고 하이킥')
	outfile = unicode(os.path.join(testdir,'tvshow.nfo'), 'utf-8')
	print "save nfo: %s" % outfile
	meta.SaveSeriesNFO( outfile )

	print "parse episode"
	fetcher.ParseEpisodePageList(id)
	print "found episode: %d" % len(meta.EpisodeInfo)
	if len(meta.EpisodeInfo) > 0:
		print "save episode metadata"
		outfile = unicode( os.path.join(testdir,'하이킥.EP 001.nfo'), 'utf-8' )
		meta.SaveEpisodeNFO(fetcher.Season, 1, outfile)
		outfile = unicode( os.path.join(testdir,'하이킥.EP 100.nfo'), 'utf-8' )
		meta.SaveEpisodeNFO(fetcher.Season, 100, outfile)
# vim: ts=4 sw=4
