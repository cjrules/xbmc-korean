# -*- coding: utf-8 -*-
"""
  Retrieve medata for Movie from Daum
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_movie import MovieMetaData

class MovieFetcher:
    type = "movie"
    site = "Daum"
    meta = None

    def __init__(self): 
        self.base_url    = "http://movie.daum.net"
        self.search_url  = self.base_url+"/search.do?type=movie&q=%s"
        self.details_url = self.base_url+"/moviedetail/moviedetailMain.do?movieId=%s"
        self.story_url   = self.base_url+"/moviedetail/moviedetailStory.do?movieId=%s"
        self.cast_url    = self.base_url+"/moviedetail/moviedetailCastCrew.do?movieId=%s"
        self.photo_url   = self.base_url+"/moviedetail/moviedetailPhotoList.do?movieId=%s&order=recommend"
        self.meta = MovieMetaData()

    # search with title
    def Search(self,title): 
        resp = urllib.urlopen( self.search_url % urllib.quote_plus(title.encode('utf-8')) )
	soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
        result = []
	for item in soup.findAll("span",{"class" : "fl srch"}):
	    id = re.compile("movieId=(\d+)").search(item.a['href']).group(1)
	    title = ''.join(item.a.findAll(text=True))
            result.append( (id,title) )
        return result

    def ParsePage(self,id):
        resp = urllib.urlopen( self.details_url % id );
	strain = SoupStrainer("div",{"id" : "movieinfoDetail"})
	soup = BeautifulSoup(resp.read(),strain,fromEncoding="utf-8")

	header = soup.find("p",{"class":"header"})
        self.meta.m_title = header.strong.string	# class=title_kor
        self.meta.m_year = header.a.string
        aka = header.find("em",{"class":"title_AKA"})
	temp = aka.find("span",{"class":"eng"})
	if temp:
	    self.meta.m_aka = temp.string
	else:
	    self.meta.m_aka = aka.contents[0]

        self.meta.m_genres = []
	sect = soup.find("dl",{"class":"cu mainInfo"})
	secName = sect.dt.strong.renderContents()
	if secName != "요약정보":
	    print "ERROR: unexpected "+secName
	ptCount = 0
	for tt in sect.dd.contents:
	    if hasattr(tt,'name'):
		if tt.name == 'span':
		    if tt['class'] == 'bar':
			ptCount = ptCount + 1
		    elif tt['class'] == 'rating':
			self.meta.m_cert = tt.img['title']
		elif tt.name == 'a':
		    text = tt.string.strip()
		    if text:
			if ptCount == 0:
			    self.meta.m_genres.append( text )
	    else:
		text = tt.string.strip()
		if text:
		    if ptCount == 2:
			self.meta.m_runtime = text
		    elif ptCount == 4:
			self.meta.m_cert = text

	self.meta.m_rating = float( soup.find("span",{"class":"star_big pink"}).em.string )
        self.meta.m_poster = re.compile('C\d{3}x\d{3}').sub('image', soup.find('p', {"class" : "poster"}).a.img['src'])

        self.meta.m_id = id
        self.meta.m_directors = []
        self.meta.m_writers = []
        self.meta.m_actors = []
        self.meta.m_backdrop_list = []

        self.ParsePlotPage(id)
        self.ParseCastPage(id)
        self.ParsePhotoPageList(id)

	return self.meta

    def ParsePlotPage(self,id):
        resp = urllib.urlopen( self.story_url % id );
	strain = SoupStrainer("div",{"id" : "synopsis"})
	soup = BeautifulSoup(resp.read(),strain,fromEncoding="utf-8")
	plot = ''.join(soup.find('div',{"class" : "txt"}).findAll(text=True))
        self.meta.m_plot = plot.strip().replace('\r','')

    def ParseCastPage(self,id):
        resp = urllib.urlopen( self.cast_url % id );
	soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")

	pt = soup.find("h5",text=re.compile(u"^\s*감독\s*$"))
	if pt:
	    for item in pt.parent.parent.findAll("span",{"class" : "name"}):
		self.meta.m_directors.append( item.a.string )

	pt = soup.find("h5",text=re.compile(u"^\s*각본\s*$"))
	if pt:
	    for item in pt.parent.parent.findAll("span",{"class" : "name"}):
		self.meta.m_writers.append( item.a.string )

	pt = soup.find("h5",text=re.compile(u"^\s*주연\s*$"))
	if pt:
	    for item in pt.parent.parent.findAll("dl"):
		name = item.find('img')['alt'].strip()
		role = item.find('span',{"class" : "etcs"}).string.strip()
		role = role[:role.rfind(u' 역')]
		self.meta.m_actors.append( (name,role) )

    def ParsePhotoPageList(self,id):
        this_url = self.photo_url % id
        self.ParsePhotoPage(this_url)

        resp = urllib.urlopen( this_url )
	strain = SoupStrainer("div",{"id" : "photoViewer"})
	soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
	for page in soup.find("div",{"class" : "pagination"}).findAll('a'):
	    url = self.base_url+page['href']
	    self.ParsePhotoPage(url)

    def ParsePhotoPage(self,url):
        resp = urllib.urlopen( url )
	strain = SoupStrainer("div",{"id" : "photoViewer"})
	soup = BeautifulSoup(resp.read(),strain,fromEncoding="utf-8")
	for item in soup.find("table",{"id" : "tPicTop"}).findAll("td"):
	    img = item.find('img')['src']
            self.meta.m_backdrop_list.append( (img, re.sub('S\d{3}x\d{3}', 'image', img)) )

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
