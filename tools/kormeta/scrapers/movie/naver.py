# -*- coding: utf-8 -*-
"""
  Retrieve medata for Movie from NAVER
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_movie import MovieMetaData

class MovieFetcher:
	meta = None

	def __init__(self): 
		self.base_url	 = "http://movie.naver.com"
		self.search_url  = self.base_url+"/movie/search/result.nhn?query=%s"
		self.main_url	 = self.base_url+"/movie/bi/mi/basic.nhn?code=%s"
		self.details_url = self.base_url+"/movie/bi/mi/detail.nhn?code=%s"
		self.photo_url   = self.base_url+"/movie/bi/mi/photo.nhn?code=%s"
		self.striptags   = re.compile("<[^>]*>")
		self.meta = MovieMetaData()

	# search with title
	def Search(self,title): 
		resp = urllib.urlopen( self.search_url % urllib.quote_plus(title.encode('euc-kr')) )
		soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")
		result = []
		for item in soup.find("ul", {"class" : re.compile("^search_list_1")}).findAll('li'):
			ref = item.find('a')
			id = re.compile("code=(\d+)").search( ref['href'] ).group(1)
			title = self.striptags.sub('',ref.renderContents())
			title = unicode(title,'utf-8')
			result.append( (id,title) )
		return result

	def ParsePage(self,id):
		resp = urllib.urlopen( self.main_url % id );
		doc = resp.read()
		soup = BeautifulSoup(doc,fromEncoding="euc-kr")

		title,subtitle = re.compile(r'''"&main_title="\+encodeURIComponent\("([^"]*)"\)\+"&sub_title="\+encodeURIComponent\("([^"]*)"\)''').search(doc).group(1,2)
		self.meta.m_title = unicode(title,'euc-kr')
		temp = subtitle.split(',')
		if len(temp) == 1:
			self.meta.m_year = int( subtitle )
		else:
			self.meta.m_aka = unicode(temp[0],'euc-kr')
			self.meta.m_year = int( temp[-1] )

		self.meta.m_rating = float( re.compile('''"&star_point=(\d{1}\.\d{1,2})";''').search(doc).group(1) )

		hlines = soup.find("dl",{"class":"summary"}).findAll('dd')
		# lines 1: 기본정보
		divpts = unicode(hlines[0].renderContents(),'utf-8').split(">|</span>")
		self.meta.m_genres = re.compile('>([^<]*)</a>').findall(divpts[0])
		self.meta.m_runtime = re.compile('>(\d+)</span>').search(divpts[2]).group(1)
		#self.meta.m_year = int( re.compile('>(\d+)</a>').search(divpts[3]).group(1) )

		# lines 2: 감독
		self.meta.m_directors = []
		for ref in hlines[1].findAll('a'):
			self.meta.m_directors.append( ref.string )
		# lines 4: 등급
		self.meta.m_cert = hlines[3].find('a').string
		
		# 줄거리
		lines = []
		for pt in soup.find('div',{"class" : re.compile("^box_story_1")}).findAll('p'):
			lines.append( pt.renderContents() )
		plot = '\n'.join(lines).replace('<br>','\n')
		plot = plot.replace("&nbsp;"," ").replace('<br />','\n')
		self.meta.m_plot = unicode(plot,'utf-8')
		
		# 포스터
		self.meta.m_poster = soup.find('div',{"class" : "poster"}).find('img')['src']

		self.meta.m_id = id
		self.meta.m_writers = []
		self.meta.m_actors = []
		self.meta.m_backdrop_list = []

		self.ParseCastPage(id)
		self.ParsePhotoPageList(id)

		return self.meta

	def ParseCastPage(self,id):
		resp = urllib.urlopen( self.details_url % id );
		soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")

		for item in soup.find('div', id='cast_1').findAll('th', {"class" : "name"}):
			name = item.a.string
			role = item.find( text=re.compile(u' 역') )
			role = role[:role.rfind(u' 역')]
			self.meta.m_actors.append( (name,role) )

		for item in soup.find('h6', text=u'각본').parent.parent.findAll('li'):
			name = item.a.string
			self.meta.m_writers.append( name )

	def ParsePhotoPageList(self,id):
		this_url = self.photo_url % id
		self.ParsePhotoPage(this_url)

		resp = urllib.urlopen( this_url )
		strain = SoupStrainer("div",{"class" : re.compile("^pagenavigation")})
		soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")
		for page in soup.find('td').findAll('a'):
			print page
			url = self.base_url+page['href']
			self.ParsePhotoPage(url)

	def ParsePhotoPage(self,url):
		resp = urllib.urlopen( url )
		strain = SoupStrainer("div",{"class" : "photo_list"})
		soup = BeautifulSoup(resp.read(),strain,fromEncoding="euc-kr")
		for item in soup.findAll('li'):
			thumb = item.find('img')['src']
			self.meta.m_backdrop_list.append( (thumb, thumb.replace('/mit120/','/mit500/')) )

if __name__ == '__main__':
	import os
	fetcher = MovieFetcher()
	print "search"
	movies = fetcher.Search(u"전우치")
	for id,title in movies:
		print "%s: %s" % (id,title)
	if movies:
		print "parse"
		meta = fetcher.ParsePage(movies[0][0])
		print meta.__str__()

		testdir = os.path.join('d:'+os.sep,'Videos','영화','전우치')
		filename = unicode(os.path.join(testdir,'movie.nfo'), 'utf-8')
		print "save nfo: %s" % filename
		meta.SaveNFO( filename )
# vim: ts=4 sw=4
