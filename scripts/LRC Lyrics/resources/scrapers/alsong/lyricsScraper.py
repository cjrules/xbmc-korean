# -*- Mode: python; coding: utf-8; tab-width: 8; indent-tabs-mode: t; -*-
"""
Scraper for http://lyrics.alsong.co.kr/

edge
"""

import struct,string,md5
import urllib2
import xbmc
import xml.dom.minidom as xml

__title__ = "alsong.co.kr"
__allow_exceptions__ = False


ALSONG_URL = "http://lyrics.alsong.net/alsongwebservice/service1.asmx"

ALSONG_TMPL = '''\
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns2="ALSongWebServer/Service1Soap" xmlns:ns1="ALSongWebServer" xmlns:ns3="ALSongWebServer/Service1Soap12">
<SOAP-ENV:Body>
<ns1:GetLyric5>
    <ns1:stQuery>
	<ns1:strChecksum>%s</ns1:strChecksum>
	<ns1:strVersion>2.2</ns1:strVersion>
	<ns1:strMACAddress />
	<ns1:strIPAddress />
    </ns1:stQuery>
</ns1:GetLyric5>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''

class alsongClient(object):
    '''
    privide alsong specific function, such as key from mp3
    '''
    @staticmethod
    def GetKeyFromFile(file):
	f = open(file,'rb')
	# Searching ID tag
	while True:
	    buf = f.read(3)
	    if len(buf) < 3 or f.tell() > 50000:
		# no ID tag
		f.seek(0,0)
		break
	    if buf == 'ID3':
		f.seek(3,1)     # skip version/flag
		# ID length (synchsafe integer)
		tl = struct.unpack('bbbb', f.read(4))
		taglen = (tl[0]<<21)|(tl[1]<<14)|(tl[2]<<7)|tl[3]
		f.seek(taglen,1)
		break
	    else:
		f.seek(-2,1)
	# Searching MPEG SOF
	while True:
	    buf = f.read(1)
	    if len(buf) < 1 or f.tell() > 100000:
		key = ''
		break
	    if buf == '\xff':
		rbit = struct.unpack('B',f.read(1))[0] >> 5
		if rbit == 7:
		    f.seek(-2,1)
		    buf = f.read(160*1024)
		    # calculate hashkey
		    m = md5.new(); m.update(buf); key = m.hexdigest()
		    break
	f.close()
	return key


class LyricsFetcher:
    def __init__( self ):
        self.base_url = "http://lyrics.alsong.co.kr/"

    def get_lyrics(self, artist, song):
	musicFullPath = xbmc.Player().getPlayingFile()
	print musicFullPath
	key = alsongClient.GetKeyFromFile( musicFullPath )
	if not key:
	    return ''

	title = artist+' - '+song
	lyrics = self.get_lyrics_from_list( (title,key,artist,song) )
	return lyrics

    def get_lyrics_from_list(self, link):
        title,key,artist,song = link
        print key, artist, song

	headers = { 'Content-Type' : 'text/xml; charset=utf-8' }
	request = urllib2.Request(ALSONG_URL, ALSONG_TMPL % key, headers)
	try:
	    response = urllib2.urlopen(request)
	    Page = response.read()
	except Exception, e:
	    print e

	tree = xml.parseString( Page )
	if tree.getElementsByTagName("strInfoID")[0].childNodes[0].data == '-1':
	    return ''
	lyric = string.replace( tree.getElementsByTagName("strLyric")[0].childNodes[0].data, '<br>', '\n' )
	return lyric.encode('utf-8')

if ( __name__ == '__main__' ):
    # used to test get_lyrics() 
    artist = u"소녀시대"
    song = u"Gee"

    lyrics = LyricsFetcher().get_lyrics( artist, song )
    if ( isinstance( lyrics, list ) ):
        for song in lyrics:
            print song
    else:
        print lyrics

    LyricsFetcher().get_lyrics_from_list(lyrics[0])
