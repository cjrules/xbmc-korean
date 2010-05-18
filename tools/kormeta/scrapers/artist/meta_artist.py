# -*- coding: utf-8 -*-
"""
  Music Artist Meta Data
"""

import urllib

class ArtistMetaData:
    def __init__(self):
	self.m_id = ''
	self.m_name = ''
	self.m_born = ''
	self.m_died = ''
	self.m_formed = ''
	self.m_disbanded = ''
	self.m_years = []
	self.m_genres = []
	self.m_styles = []
	self.m_albums = []
	self.m_biography = ''
	self.m_thumb = ''
	self.m_backdrop_list = []   # (thumb,url)

    def __str__(self):
	x = [u'id: %s'%self.m_id,
	     u'name: %s'%self.m_name,
	     u'genres: %s'%'|'.join(self.m_genres),
	     u'styles: %s'%'|'.join(self.m_styles),
	    ]
	x.append(u'born: %s'%self.m_born )
	x.append(u'died: %s'%self.m_died )
	x.append(u'formed: %s'%self.m_formed )
	x.append(u'disbanded: %s'%self.m_disbanded )
	x.append(u'biography: %s'%self.m_biography )
	for title,year in self.m_albums:
	    x.append(u'album: %s (%s)'%(title,year))
	x.append(u'thumb: %s'%self.m_thumb )
	for thumb,url in self.m_backdrop_list:
	    x.append(u'bdrop: %s'%url)
	return '\n'.join(x)

    #---------------------------------
    # XBMC .nfo file
    def SaveNFO(self, filename): 
	lines = []
	lines.append( u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>' )
	lines.append( u"<artist>" )
	lines.append( u"  <name>%s</name>" % self.m_name )
	lines.append( u"  <thumb>%s</thumb>" % self.m_thumb )
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
        # yearactive
	for year in self.m_years:
	    if year == self.m_years[0]:
		lines.append( u"  <yearactive clear=true>%s</yearactive>" % year)
	    else:
		lines.append( u"  <yearactive>%s</yearactive>" % year)
        # biography
	lines.append( u"  <biography>%s</biography>" % self.m_biography )
        # album
        for title,year in self.m_albums:
            lines.append( u"  <album>")
            lines.append( u"    <title>%s</title>" % title)
            lines.append( u"    <year>%s</year>" % year)
            lines.append( u"  </album>")
        # fanart
	lines.append( u"  <fanart>")
        for thumb,url in self.m_backdrop_list:
            lines.append( u'    <thumb preview="%s">%s</thumb>' % (thumb,url) )
	lines.append( u"  </fanart>")
	lines.append( u"</artist>")

        f = open(filename,'w')
        f.write( '\n'.join(lines).encode('utf-8') )
        f.close()

    def SavePoster(self, filepath): 
        f = open(filepath, "wb")
        f.write( urllib.urlopen(self.m_thumb).read() )
        f.close()

    def SaveBackdrops(self, path, sel_list): 
        import os
        # save the first photo as htbackdrop.jpg
        if len(sel_list) > 0 and len(self.m_backdrop_list) >= sel_list[0]:
            #  download
            f = open( os.path.join(path,'backdrop.jpg'), "wb")
            f.write( urllib.urlopen(self.m_backdrop_list[ sel_list[0] ][1]).read() )
            f.close()
        # save photo pages
        if len(sel_list) > 1:
            count = 0
            for i in sel_list:
                if self.m_backdrop_list[i]:
        	    count += 1
                    #  download
                    f = open( os.path.join(path,'backdrop%d.jpg' % count), "wb")
                    f.write( urllib.urlopen(self.m_backdrop_list[i][1]).read() )
                    f.close()

if __name__ == '__main__':
    meta = ArtistMetaData()
    meta.m_name = u'빅마마'
    meta.m_biography = u'빅마마는'
    meta.m_genres = [u'가요']
    meta.m_styles = [u'발라드',u'R&B']
    import os
    testdir = os.path.join('d:'+os.sep,'Music','빅마마')

    print meta.__str__()
    filename = unicode(os.path.join(testdir,'artist.nfo'), 'utf-8')
    print "save nfo: %s" % filename
    meta.SaveNFO( filename )
    #print "save thumb"
    #meta.SavePoster( testdir+'folder.jpg' )
    #print "save backdrop"
    #meta.SaveBackdrops( testdir, [0,1] )
