# -*- coding: utf-8 -*-
"""
  Retrieve medata for Music Album from Daum
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_album import AlbumMetaData

class AlbumFetcher:
    type = "album"
    site = "Daum"
    meta = None

    def __init__(self): 
        self.base_url    = "http://music.daum.net"
        self.search_url  = self.base_url+"/search/album.do?query=%s"
        self.details_url = self.base_url+"/album/album.do?albumId=%s"
        self.meta = AlbumMetaData()

    # search with title
    def Search(self,title,artist):
        resp = urllib.urlopen( self.search_url % urllib.quote_plus("%s %s" % (title,artist)) )
	soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")
        result = []
	for item in soup.findAll("div",{"class" : "collCont"}):
	    id = re.compile("albumId=(\d+)").search(item.a['href']).group(1)
	    title = unicode(''.join(item.a.findAll(text=True)), 'utf-8')
	    title = title.replace("&#233;",u"é")
	    artist = unicode(''.join(item.find("dd",{"class":"con"}).a.findAll(text=True)), 'utf-8')
            result.append( (id,title,artist) )
        return result

    def ParsePage(self,id):
        resp = urllib.urlopen( self.details_url % id );
	soup = BeautifulSoup(resp.read(),fromEncoding="utf-8")

        self.meta.m_id = id

	strain = SoupStrainer("div",{"id" : "wAbmInf"})
	sect = soup.find(strain)
	self.meta.m_thumb = sect.find("p",id="AlbumPic").find('img')['src']
	self.meta.m_thumb = re.compile("S\d{3}x\d{3}").sub("image", self.meta.m_thumb)
	self.meta.m_name = sect.find("div",{"class":"infDt"}).ul.li.next.string
	count = 0
	self.meta.m_genres = []
	self.meta.m_styles = []
	for genre in sect.find("ul",{"class":"data2"}).find("li",{"class":re.compile("^itm6")}).findAll('a'):
	    if (count%2) == 0:
		self.meta.m_genres.append( genre.string.replace(';','') )
	    else:
		self.meta.m_styles.append( genre.string.replace(';','') )
	    count = count+1
	self.meta.m_release = sect.find("ul",{"class":"data2"}).find("li",{"class":re.compile("^itm7")}).span.string

	self.meta.m_rating = float( soup.find("span",{"class":"starBig pink"}).em.string )

	strain = SoupStrainer("div",{"id" : "wAbmInfoT"})
	sect = soup.find(strain)
	self.meta.m_review = ''.join(sect.find('p',id="albumDesc").findAll(text=True)).strip()
	self.meta.m_review = unicode(self.meta.m_review, 'utf-8')

	# can not extract
	self.meta.m_albums = []

	return self.meta

if __name__ == '__main__':
    import sys,os
    libdir = os.path.join('..','..','libs')
    if not libdir in sys.path:
	sys.path.append( libdir )
    fetcher = AlbumFetcher()

    print "search"
    albums = fetcher.Search("Blossom","빅마마")
    for id,title,artist in albums:
        print "%s: %s (%s)" % (id,title,artist)
    if albums:
        print "parse"
        meta = fetcher.ParsePage(albums[0][0])
	print meta.__str__()
