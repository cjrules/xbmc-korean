# -*- coding: utf-8 -*-
"""
  Retrieve medata for Music Artist from Daum
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_artist import ArtistMetaData

class ArtistFetcher:
    type = "artist"
    site = "Daum"
    meta = None

    def __init__(self): 
        self.base_url    = "http://music.daum.net"
        self.search_url  = self.base_url+"/search/artist.do?query=%s"
        self.details_url = self.base_url+"/artist/intro.do?artistDetailId=%s"
        self.album_url   = self.base_url+"/artist/album.do?artistDetailId=%s&orderCondition=0&albumType=R"
        self.photo_url   = self.base_url+"/artist/photo.do?artistDetailId=%s"
        self.meta = ArtistMetaData()

    # search with title
    def Search(self,title): 
        resp = urllib.urlopen( self.search_url % urllib.quote_plus(title) );
	soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
        result = []
	for item in soup.findAll("div",{"class" : "collCont"}):
	    id = re.compile("artistDetailId=(\d+)").search(item.find('a')['href']).group(1)
	    title = ''.join(item.a.findAll(text=True))
            result.append( (id,title) )
        return result

    def ParsePage(self,id):
        resp = urllib.urlopen( self.details_url % id );
	soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")

        self.meta.m_id = id

	strain = SoupStrainer("div",{"id" : "wArtiInf"})
	sect = soup.find(strain)
	self.meta.m_thumb = sect.find("p",id="ArtiPic").find('img')['src']
	self.meta.m_name = sect.find("div",{"class":"infDt"}).ul.li.next.string
	self.meta.m_aka = sect.find("div",{"class":"infDt"}).ul.li.findNextSibling('li').next.string.strip()
	self.meta.m_years = []
	for year in sect.findAll("span",{"class":re.compile("^year y\d+")}):
	    self.meta.m_years.append( year.string )
	count = 0
	self.meta.m_genres = []
	for genre in sect.find("ul",{"class":"data2"}).findAll("li",{"class":"itm1 fl"})[1].findAll('a'):
	    count = count+1
	    if (count%2) == 0:
		self.meta.m_genres.append( genre.string.replace(';','') )
	self.meta.m_styles = []

	strain = SoupStrainer("div",{"id" : "wArtiProf"})
	header = soup.find(strain)

	self.meta.m_rating = float( soup.find("span",{"class":"starBig pink"}).em.string )
	self.meta.m_biography = ""

        self.ParseAlbumPage(id)
        self.ParsePhotoPage(id)

	return self.meta

    def ParseAlbumPage(self,id):
        resp = urllib.urlopen( self.album_url % id );
	strain = SoupStrainer("div",{"id" : "albumList1"})
	soup = BeautifulSoup(resp.read(),strain,fromEncoding="utf-8")

	self.meta.m_albums = []
	for item in soup.findAll("ul",{"class":"infLst fl"}):
	    title = item.find("li",{"class":"c1"}).a.string
	    date = item.find("li",{"class":re.compile("^c4")}).string.strip()
	    self.meta.m_albums.append( (title,date) )

    def ParsePhotoPage(self,id):
        resp = urllib.urlopen( self.photo_url % id );
	strain = SoupStrainer("div",{"id" : "wArtiPic"})
	soup = BeautifulSoup(resp.read(),strain,fromEncoding="utf-8")

        self.meta.m_backdrop_list = []
	for item in soup.find("table",{"id" : "tPicTop"}).findAll("td"):
	    img = item.find('img')['src']
            self.meta.m_backdrop_list.append( (img, re.sub('S\d{3}x\d{3}', 'image', img)) )

if __name__ == '__main__':
    import sys,os
    libdir = os.path.join('..','..','libs')
    if not libdir in sys.path:
	sys.path.append( libdir )
    fetcher = ArtistFetcher()

    print "search"
    artists = fetcher.Search("빅마마")
    for id,name in artists:
        print "%s: %s" % (id,name)
    if artists:
        print "parse"
        meta = fetcher.ParsePage(artists[0][0])
	print meta.__str__()
