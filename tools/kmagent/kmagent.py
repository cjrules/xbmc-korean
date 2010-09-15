# -*- coding: utf-8 -*-
#modified from simpleserver by Jon Berg

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

from os import curdir, sep
import sys
sys.path.append(curdir)
sys.path.append(curdir+sep+'lib')

fetcher = None
_ver = "$GlobalRev: 313 $"
_portnum = 8081

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global fetcher
        up = urlparse.urlparse(self.path)
        param = urlparse.parse_qs(up.query)
        print "cmd: "+up.path
        if up.path == "/fetch":
            #type = param['type'][0]
            #if type == 'daumtv':
            id = param['id'][0]
            print "id: "+id

            if fetcher is None or fetcher.type != "series":
                from scrapers.series.daum import SeriesFetcher
                fetcher = SeriesFetcher()
	    self.send_response(200)
	    self.send_header('Content-Type', 'text/xml; charset=utf-8')
	    self.end_headers()
	    self.wfile.write('<episodeguide><url>http://127.0.0.1:%d%s</url></episodeguide>' % (self.server.server_port, self.path.replace('fetch','retrieve')))
            if fetcher.meta is None or fetcher.meta.s_id != id:
                fetcher.ParseEpisodePageList(id)
                fetcher.meta.s_id = id
            print "done"
            return
        if up.path == "/retrieve":
            #type = param['type'][0]
            #if type == 'daumtv':
            if fetcher is None or fetcher.type != "series" or fetcher.meta is None:
                self.send_error(404,'File Not Found: %s' % self.path)
                return
            if fetcher.meta.s_id != param['id'][0]:
                self.send_error(404,'File Not Found: %s' % self.path)
                return
	    self.send_response(200)
	    self.send_header('Content-Type', 'text/xml; charset=utf-8')
	    if fetcher.EpisodeFound:
		xml = "<episodeguide>%s</episodeguide>" % fetcher.meta.GetEpisodeListXML(
		  "http://127.0.0.1:"+str(self.server.server_port)+"/detail2?type=daumtv&id="+fetcher.meta.s_id+"&season=%d&ep=%d" )
	    else:
		# dummy info for non-existing episode
		lines = []
		lines.append("<episodeguide>")
		for i in range(1,25):
		    lines.append("<episode>")
		    #lines.append("<title>제%d회</title>" % i)
		    lines.append("<url>http://127.0.0.1:%d/dummyep?type=daumtv&ep=%d</url>" % (self.server.server_port,i))
		    #lines.append("<url>http://127.0.0.1:%d/detail?type=daumtv&id=%s&season=1&episode=%d</url>" % (self.server.server_port,fetcher.meta.s_id,i))
		    lines.append("<season>1</season>")
		    lines.append("<epnum>%d</epnum>" % i)
		    lines.append("</episode>")
		lines.append("</episodeguide>")
		xml = ''.join(lines)
	    self.send_header('Content-Length', len(xml))
	    self.end_headers()
	    self.wfile.write(xml)
            print "done"
            return
        if up.path == "/detail":
            #type = param['type'][0]
            #if type == 'daumtv':
            if fetcher is None or fetcher.type != "series":
                self.send_error(404,'File Not Found: %s' % self.path)
                return
            if fetcher.meta.s_id != param['id'][0]:
                self.send_error(404,'File Not Found: %s' % self.path)
                return
            season = int( param['season'][0] )
            episode = int( param['episode'][0] )
            print "season: %d, episode: %d" % (season,episode)

            self.send_response(200)
            self.send_header('Content-type', 'text/xml; charset=utf-8')
            self.end_headers()
            if fetcher.EpisodeFound:
                xml = fetcher.meta.GetEpisodeDetailXML( season, episode )
            else:
                xml = "<details><title>제%d회</title></details>" % episode
            self.wfile.write(xml)
            print "done"
            return
        if up.path == "/detail2":
            #type = param['type'][0]
            #if type == 'daumtv':
            if fetcher is None or fetcher.type != "series":
                self.send_error(404,'File Not Found: %s' % self.path)
                return
            if fetcher.meta.s_id != param['id'][0]:
                self.send_error(404,'File Not Found: %s' % self.path)
                return
            season = int( param['season'][0] )
            episode = int( param['ep'][0] )
            print "season: %d, episode: %d" % (season,episode)

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            if fetcher.EpisodeFound:
		vals = fetcher.meta.EpisodeInfo[ (season,episode) ]
                xml = u'''<h5 class="fs12 em">제%d회&nbsp;%s</h5><p class="txt"><strong class="epTit">%s</strong>%s</p>'''\
			% (episode,vals[1],vals[0],vals[2])
                xml = xml.encode('utf-8')
            else:
                xml = '''<h5 class="fs12 em">제%d회&nbsp;</h5><p class="txt"></p>''' % episode
            self.wfile.write(xml)
            print "done"
            return
        if up.path == "/dummyep":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            # mimic Daum page
            self.wfile.write( '''<h5 class="fs12 em">제%s회&nbsp;</h5><p class="txt"></p>''' % param['ep'][0] )
            print "done"
            return
        if up.path == "/fanart":
            #type = param['type'][0]
            #if type == 'daummusic':
            name = param['name'][0]
            #if param['coding']:
            #    name = name.decode(param['coding'][0])
            print "name: "+name
            self.send_response(200)
            self.send_header('Content-type', 'text/xml; charset=utf-8')
            self.end_headers()

            if fetcher is None or fetcher.type != "artist":
                from scrapers.artist.daum import ArtistFetcher
                fetcher = ArtistFetcher()
            if fetcher.meta.m_name != name:
                srch_rslt = fetcher.Search(name)
                if srch_rslt is None: 
                    return
                print "found: %s, %s" % srch_rslt[0]
                fetcher.meta.m_id = srch_rslt[0][0]
                #fetcher.meta.m_name = srch_rslt[0][1]
                fetcher.meta.m_name = name
                fetcher.ParsePhotoPage(fetcher.meta.m_id)
                xml = "<details>%s</details>" % fetcher.meta.GetBackdropListXML()
                self.wfile.write(xml)
            print "done"
            return
        return
     
def main():
    try:
        server = HTTPServer(('', _portnum), MyHandler)
        print 'start kmagent web server, r%s...' % _ver[ _ver.find(':')+2 : _ver.rfind(' ') ]
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

# vim: ts=8 sw=4
