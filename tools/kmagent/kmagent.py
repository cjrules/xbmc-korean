# -*- coding: utf-8 -*-
#modified from simpleserver by Jon Berg

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

from os import curdir, sep
import sys
sys.path.append(curdir)
sys.path.append(curdir+sep+'lib')

fetcher = None
_ver = "$GlobalRev: 319 $"
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
            # parsing the first page
            if fetcher.meta is None or fetcher.meta.s_id != id:
                fetcher.EpisodeFound = False
                fetcher.max_epnum = 0
                fetcher.ParseEpisodePageByUrl(fetcher.episode_url % id)
            lines = []
            max_epnum = 25
            lines.append(u"<episodeguide>")
            if fetcher.EpisodeFound:
                max_epnum = fetcher.max_epnum
            for i in range(max_epnum):
                epnum = max_epnum-i
                lines.append(u"<episode>")
                lines.append(u"<season>%d</season>" % fetcher.Season)
                lines.append(u"<epnum>%d</epnum>" % epnum)
                lines.append(u"<url>http://127.0.0.1:%d/detail?type=daumtv&id=%s&season=%d&episode=%d</url>" % 
                                (self.server.server_port, id, fetcher.Season, epnum) )
                lines.append(u"</episode>")
            lines.append(u"</episodeguide>")
            xml = ''.join(lines).encode('utf-8')
            self.wfile.write(xml)
            # full scrapping afterward
            if fetcher.EpisodeFound and fetcher.meta.s_id != id:
                print "scrapping episode pages"
                fetcher.ParseEpisodePageList(id)
            fetcher.meta.s_id = id
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
            self.send_header('Content-Type', 'text/xml; charset=utf-8')
            self.end_headers()
            if fetcher.EpisodeFound:
                xml = fetcher.meta.GetEpisodeDetailXML( season, episode )
            else:
                xml = "<details><title>제%d회</title></details>" % episode
            self.wfile.write(xml)
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
            self.send_header('Content-Type', 'text/xml; charset=utf-8')
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
        if up.path == "/nulleplist":
            #type = param['type'][0]
            #if type == 'anime':
            epnum = int( param['epnum'][0] )
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml; charset=utf-8')
            self.end_headers()

            lines = []
            lines.append("<episodeguide>")
            for i in range(1,epnum+1):
                lines.append("<episode>")
                #lines.append("<title>제%d화</title>" % i)
                lines.append("<season>1</season>")
                lines.append("<epnum>%d</epnum>" % i)
                lines.append("<url>http://127.0.0.1:%d/nullep?ep=%d</url>" % (self.server.server_port,i))
                lines.append("</episode>")
            lines.append("</episodeguide>")
            xml = ''.join(lines)
            self.wfile.write(xml)
            print "done"
            return
        if up.path == "/nullep":
            #type = param['type'][0]
            #if type == 'anime':
            ep = int( param['ep'][0] )
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml; charset=utf-8')
            self.end_headers()
            self.wfile.write( "<details><title>제%d화</title></details>" % ep )
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

# vim: ts=4 sw=4 expandtab
