# -*- coding: utf-8 -*-
"""
  Retrieve medata for Music Artist from NAVER
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString
import re
from meta_artist import ArtistMetaData

class ArtistFetcher:
	type = "artist"
	site = "Naver"
	meta = None

	def __init__(self): 
		self.base_url   = "http://music.naver.com"
		self.search_url = self.base_url+"/search.nhn?where=artist&query=%s"
		self.main_url   = self.base_url+"/artist.nhn?artistId=%s"
		self.album_url  = self.base_url+"/artist.nhn?m=album&artistId=%s"
		self.photo_url  = self.base_url+"/artist.nhn?m=photo&artistId=%s"
		self.striptags  = re.compile("<[^>]*>")
		self.meta = ArtistMetaData()
		self.striptags = re.compile("<.*?>")

	# search with title
	def Search(self,title): 
		resp = urllib.urlopen( self.search_url % urllib.quote_plus(title.encode('euc-kr')) );
		soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")
		result = []
		for item in soup.findAll("a", {"class" : "c u b2"}):
			id = re.compile("'(\d+)'").search(item['href']).group(1)
			title = unicode(self.striptags.sub('',item.renderContents()), 'utf-8')
			result.append( (id,title) )
		return result

	def ParsePage(self,id):
		resp = urllib.urlopen( self.main_url % id );
		soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")

		self.meta.m_id = id
		self.meta.m_name = soup.find('h2').string

		strain = SoupStrainer("div",{"class" : "artist_info"})
		sect = soup.find(strain)
		self.meta.m_thumb = sect.find("div",{"class":"albumartist_thumb"}).img['src']

		chk = sect.find("img",alt=u"출생")
		if chk:
			self.meta.m_born = chk.parent.nextSibling.nextSibling.next.string.strip()

		chk = sect.find("img",alt=u"사망")
		if chk:
			self.meta.m_died = chk.parent.nextSibling.nextSibling.next.string.strip()

		chk = sect.find("img",alt=u"결성")
		if chk:
			self.meta.m_formed = chk.parent.nextSibling.nextSibling.next.string.strip()

		chk = sect.find("img",alt=u"해체")
		if chk:
			self.meta.m_disbanded = chk.parent.nextSibling.nextSibling.next.string.strip()

		self.meta.m_years = []
		chk = sect.find("img",alt=u"활동연대")
		if chk:
			self.meta.m_years = chk.parent.nextSibling.nextSibling.next.string.strip().split(',')

		self.meta.m_styles = []
		chk = sect.find("img",alt=u"활동유형")
		if chk:
			self.meta.m_styles = chk.parent.nextSibling.nextSibling.next.string.strip().split(',')

		self.meta.m_genres = []
		chk = sect.find("img",title=u"장르")
		if chk:
			self.meta.m_genres = chk.parent.nextSibling.nextSibling.next.string.strip().split(',')

		self.meta.m_biography = self.striptags.sub('',soup.find("div", id="artistBio").renderContents().strip())
		self.meta.m_biography = self.meta.m_biography.replace("&amp;","&")
		self.meta.m_biography = self.meta.m_biography.replace("&#039;","'").replace("&#8211;","-")
		self.meta.m_biography = unicode(self.meta.m_biography,'utf-8')

		self.ParseAlbumPage(id)
		self.ParsePhotoPage(id)

		return self.meta

	def ParseAlbumPage(self,id):
		resp = urllib.urlopen( self.album_url % id );
		strain = SoupStrainer("ul",{"class" : "music_list", "id" : "mainAlbum"})
		soup = BeautifulSoup(resp.read(),strain,fromEncoding="euc-kr")

		self.meta.m_albums = []
		for item in soup.findAll("li"):
			title = item.dt.a.string
			date = item.find("dd",{"class":"date"}).string
			self.meta.m_albums.append( (title,date) )

	def ParsePhotoPage(self,id):
		resp = urllib.urlopen( self.photo_url % id );
		soup = BeautifulSoup(resp.read(),fromEncoding="euc-kr")

		self.meta.m_backdrop_list = []
		thumb_base = 'http://down.music.naver.com/music/photo/thumbnail/'
		photo_base = 'http://down.music.naver.com/music/photo/'
		for item in soup.findAll("a",{"href" : re.compile("^javascript:imageZoom")}):
			photo = re.compile("imageZoom\('/music/photo/thumbnail/(.*)'\);").search(item['href']).group(1)
			self.meta.m_backdrop_list.append( (thumb_base+photo, photo_base+photo) )

if __name__ == '__main__':
	import sys,os
	libdir = os.path.join('..','..','libs')
	if not libdir in sys.path:
		sys.path.append( libdir )
	fetcher = ArtistFetcher()

	print "search"
	artists = fetcher.Search(u"빅마마")
	for id,name in artists:
		print "%s: %s" % (id,name)
	if artists:
		print "parse"
		meta = fetcher.ParsePage(artists[0][0])
		print meta.__str__()

		testdir = os.path.join('d:'+os.sep,'Music','빅마마')
		filename = unicode(os.path.join(testdir,'artist.nfo'), 'utf-8')
		print "save nfo: %s" % filename
		meta.SaveNFO( filename )
# vim: ts=4 sw=4
