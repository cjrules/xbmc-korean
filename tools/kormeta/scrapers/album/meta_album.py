# -*- coding: utf-8 -*-
"""
  Music Album Meta Data
"""

import urllib

class AlbumMetaData:
    def __init__(self):
	self.m_id = ''
	self.m_title = ''
	self.m_artists = []
	self.m_genres = []
	self.m_styles = []
	self.m_albums = []
	self.m_review = ''
	self.m_release = ''
	self.m_thumb = ''
	self.m_tracks = []

    def __str__(self):
	x = [u'id: %s'%self.m_id,
	     u'title: %s'%self.m_title,
	     u'artists: %s'%'|'.join(self.m_artists),
	     u'genres: %s'%'|'.join(self.m_genres),
	     u'styles: %s'%'|'.join(self.m_styles),
	    ]
	x.append( u'release: %s'%self.m_release )
	x.append( u'review: %s'%self.m_review )
	x.append( u'track:' )
	for pos,title in self.m_tracks:
	    x.append(u'  %02d: %s'%(pos,title))
	x.append( u'thumb: %s'%self.m_thumb )
	return '\n'.join(x)

    #---------------------------------
    # XBMC .nfo file
    def SaveNFO(self, filename): 
	lines = []
	lines.append( u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>' )
	lines.append( u"<album>" )
	lines.append( u"  <title>%s</title>" % self.m_title )
	lines.append( u"  <releasedate>%s</releasedate>" % self.m_release )
	lines.append( u"  <thumb>%s</thumb>" % self.m_thumb )
        # artist
	for artist in self.m_artists:
	    if artist == self.m_artists[0]:
		lines.append( u"  <artist clear=true>%s</artist>" % artist)
	    else:
		lines.append( u"  <artist>%s</artist>" % artist)
        # genre
	for genre in self.m_genres:
	    if genre == self.m_genres[0]:
		lines.append( u"  <genre clear=true>%s</genre>" % genre)
	    else:
		lines.append( u"  <genre>%s</genre>" % genre)
        # style
	for style in self.m_styles:
	    if style == self.m_styles[0]:
		lines.append( u"  <style clear=true>%s</style>" % style)
	    else:
		lines.append( u"  <style>%s</style>" % style)
        # review
	lines.append( u"  <review>%s</review>" % self.m_review )
        # track
        for pos,title in self.m_tracks:
            lines.append( u"  <track>")
            lines.append( u"    <position>%d</position>" % pos)
            lines.append( u"    <title>%s</title>" % title)
            lines.append( u"  </track>")
        lines.append( u"</album>")

        f = open(filename,'w')
        f.write( '\n'.join(lines).encode('utf-8') )
        f.close()

    def SavePoster(self, filepath): 
        f = open(filepath, "wb")
        f.write( urllib.urlopen(self.m_thumb).read() )
        f.close()

if __name__ == '__main__':
    meta = AlbumMetaData()
    meta.m_title = u"Blossom"
    meta.m_release = "2009/01/01"
    meta.m_artists = [u"빅마마"]
    meta.m_review = u"빅마마는"
    meta.m_genres = [u"가요"]
    meta.m_styles = [u"발라드", u"R&B"]
    meta.m_tracks = [(0,u"하나"), (1,u"둘")]
    import os
    testdir = os.path.join('d:'+os.sep,'Music','빅마마','4집 - Blossom')

    print meta.__str__()
    filename = unicode(os.path.join(testdir,'album.nfo'), 'utf-8')
    print "save nfo: %s" % filename
    meta.SaveNFO( filename )
    #print "save thumb"
    #meta.SavePoster( testdir+'folder.jpg' )
