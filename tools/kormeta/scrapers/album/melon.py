# -*- coding: utf-8 -*-
"""
  Retrieve medata for Music Album from Melon
"""

import urllib
import simplejson
from meta_album import AlbumMetaData

class AlbumFetcher:
	type = "album"
	site = "Naver"
	meta = None

	def __init__(self): 
		self.base_url   = "http://www.melon.com"
		self.search_url = self.base_url+"/cds/search/web/searchalbum_list.json?menu_id=album&query=%s"
		self.main_url   = self.base_url+"/cds/album/web/albumdetailmain_list.json?albumId=%s"
		self.image_base = "http://image.melon.com"
		self.meta = AlbumMetaData()

	# search with title
	def Search(self,title,artist):
		srchstr = "%s %s" % (title,artist)
		jstr = urllib.urlopen( self.search_url % urllib.quote_plus(srchstr.encode('euc-kr')) ).read()
		json = simplejson.loads(jstr)
		result = []
		for item in json['albumList']:
			result.append( (item['albumId'], item['titleWebListOrg'], item['mainArtistNmBasketOrg'].split('|')[0]) )
		return result

	def ParsePage(self,id):
		jstr = urllib.urlopen( self.main_url % id ).read();
		json = simplejson.loads(jstr)
		#open('a.txt','w').write(str(json))
		
		obj = json['albumDtlEntity']
		self.meta.m_id = obj['ALBUMID']
		self.meta.m_title = obj['ALBUMREPNM']
		self.meta.m_thumb = self.image_base+obj['ALBUMIMGPATH']
		self.meta.m_artist = obj['REPARTISTNAMEBASKET'].split(',')
		self.meta.m_genres = obj['ALBUMGNR'].split(',')
		self.meta.m_styles = obj['ALBUMSTYLE'].split(',')
		self.meta.m_release = obj['ISSUEDATE']
		self.meta.m_review = obj['ALBUMREVW']

		self.meta.m_rating = float( json['totAvrgScore'] )

		#self.meta.m_review = self.meta.m_review.replace("&amp;","&")
		#self.meta.m_review = self.meta.m_review.replace("&#039;","'").replace("&#8211;","-")

		self.meta.m_tracks = []
		for disc in json['albumCdSongList']:
			for item in disc:
				self.meta.m_tracks.append( (int(item['TRACKNO']), item['SONGNAMEWEBLIST']) )

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

	"""
	testdir = os.path.join('d:'+os.sep,'Music','빅마마','4집 - Blossom')
	filename = unicode(os.path.join(testdir,'album.nfo'), 'utf-8')
	print "save nfo: %s" % filename
	meta.SaveNFO( filename )
	"""
# vim: ts=4 sw=4
