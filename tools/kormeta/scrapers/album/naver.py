# -*- coding: utf-8 -*-
"""
  Retrieve medata for Music Album from NAVER
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_album import AlbumMetaData

class AlbumFetcher:
    meta = None

    def __init__(self): 
        self.base_url   = "http://music.naver.com"
        self.search_url = self.base_url+"/search.nhn?where=album&query=%s"
        self.main_url   = self.base_url+"/album.nhn?tubeid=%s"
        self.striptags  = re.compile("<[^>]*>")
        self.meta = AlbumMetaData()
        self.striptags = re.compile("<.*?>")

    # search with title
    def Search(self,title,artist):
        srchstr = "%s %s" % (title,artist)
        resp = urllib.urlopen( self.search_url % urllib.quote_plus(srchstr.encode('euc-kr')) )
	soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")
        result = []
	for item in soup.findAll("a",{"class" : "c u"}):
	    id = re.compile("'(\d+)'").search(item['href']).group(1)
	    title = unicode(self.striptags.sub('',item.renderContents()), 'utf-8')
	    artist = item.findNextSibling('a').span.string
            result.append( (id,title,artist) )
        return result

    def ParsePage(self,id):
        resp = urllib.urlopen( self.main_url % id );
	soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")

        self.meta.m_id = id
	self.meta.m_title = soup.find('h2').string
	self.meta.m_artist = [ soup.find("dt",id="artistName").span.a.string ]

	strain = SoupStrainer("div",{"class" : "album_info"})
	sect = soup.find(strain)
	self.meta.m_thumb = sect.find("img",{"id":"albumBigThumb"})['src']
	self.meta.m_genres = sect.find("img",alt=u"장르").parent.nextSibling.nextSibling.next.string.strip().split('/')
	self.meta.m_release = sect.find("img",alt=u"발매일").parent.nextSibling.nextSibling.next.string.strip()

	self.meta.m_rating = float( sect.find("span",{"class":"text_point"}).string )

	self.meta.m_review = self.striptags.sub('',soup.find("div", id="albumDesc").renderContents().strip())
	self.meta.m_review = self.meta.m_review.replace("&amp;","&")
	self.meta.m_review = self.meta.m_review.replace("&#039;","'").replace("&#8211;","-")
	self.meta.m_review = unicode(self.meta.m_review, 'utf-8')

	self.meta.m_tracks = []
	for item in soup.findAll("td",{"class" : "num"}):
	    pos = int( item.string )
	    track = item.findNextSiblings('td')[1].a.string
	    self.meta.m_tracks.append( (pos,track) )

	return self.meta

if __name__ == '__main__':
    import sys,os
    libdir = os.path.join('..','..','libs')
    if not libdir in sys.path:
	sys.path.append( libdir )
    fetcher = AlbumFetcher()

    print "search"
    albums = fetcher.Search(u"Blossom",u"빅마마")
    for id,title,artist in albums:
        print "%s: %s (%s)" % (id,title,artist)
    if albums:
        print "parse"
        meta = fetcher.ParsePage(albums[0][0])
	print meta.__str__()

	import os
	testdir = os.path.join('d:'+os.sep,'Music','빅마마','4집 - Blossom')
	filename = unicode(os.path.join(testdir,'album.nfo'), 'utf-8')
	print "save nfo: %s" % filename
	meta.SaveNFO( filename )
