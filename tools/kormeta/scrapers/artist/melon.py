# -*- coding: utf-8 -*-
"""
  Retrieve medata for Music Artist from Melon
"""

import urllib
import simplejson
import re
from meta_artist import ArtistMetaData

class ArtistFetcher:
	type = "artist"
	site = "Naver"
	meta = None

	def __init__(self): 
		self.base_url   = "http://www.melon.com"
		self.image_base = "http://image.melon.com"
		self.search_url = self.base_url+"/cds/search/web/searchartist_list.json?menu_id=artist&query=%s"
		self.main_url   = self.base_url+"/cds/artist/web/artistdetailalbum_list.json?artistId=%s"
		self.photo_url  = self.base_url+"/cds/artist/web/artistdetailphoto_list.json?artistId=%s"
		self.meta = ArtistMetaData()

	# search with title
	def Search(self,title): 
		jstr = urllib.urlopen( self.search_url % urllib.quote_plus(title.encode('euc-kr')) ).read();
		json = simplejson.loads(jstr)
		result = []
		for item in json['artistList']:
			title = item['artistRepNm'].replace('<b>','[B]').replace('</b>','[/B]')
			result.append( (item['artistId'], title) )
		return result

	def ParsePage(self,id):
		jstr = urllib.urlopen( self.main_url % id ).read();
		json = simplejson.loads(jstr)
		#open('a.txt','w').write(str(json))

		obj = json['artistDtlEntity']
		self.meta.m_id = obj['ARTISTID']
		self.meta.m_name = obj['ARTISTREPNM']
		self.meta.m_thumb = self.image_base+obj['ARTISTIMGPATH']

		if obj['ACTTYPENAME'] == u"솔로":
			self.meta.m_born = obj['BIRTHDAY']
			self.meta.m_died = obj['DEATHDAY']
		elif obj['ACTTYPENAME'] == u"듀엣" or obj['ACTTYPENAME'] == u"그룹":
			self.meta.m_formed = obj['BIRTHDAY']
			self.meta.m_disbanded = obj['DEATHDAY']

		self.meta.m_years = re.findall("(\d+)", obj['ARTISTACTYEARBASKET'])

		self.meta.m_genres = obj['ARTISTGNR'].split(',')
		self.meta.m_styles = obj['ARTISTSTYLE'].split(',')

		self.meta.m_biography = obj['ARTISTREVW']
		#self.meta.m_biography = self.meta.m_biography.replace("&amp;","&")
		#self.meta.m_biography = self.meta.m_biography.replace("&#039;","'").replace("&#8211;","-")

		self.meta.m_albums = []
		for item in json['artistAlbumList']:
			#self.meta.m_albums.append( (item['ALBUMNAMEWEBLIST'], item['ISSUEDATE'], self.image_base+item['ALBUMIMGPATH']) )
			self.meta.m_albums.append( (item['ALBUMNAMEWEBLIST'], item['ISSUEDATE']) )

		self.ParsePhotoPage(id)

		return self.meta

	def ParsePhotoPage(self,id):
		jstr = urllib.urlopen( self.photo_url % id ).read();
		json = simplejson.loads(jstr)

		self.meta.m_backdrop_list = []
		for item in json['artistImgList']:
			self.meta.m_backdrop_list.append( (self.image_base+item['ARTISTIMGPATH'], None) )

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

		"""
		testdir = os.path.join('d:'+os.sep,'Music','빅마마')
		filename = unicode(os.path.join(testdir,'artist.nfo'), 'utf-8')
		print "save nfo: %s" % filename
		meta.SaveNFO( filename )
		"""
# vim: ts=4 sw=4
