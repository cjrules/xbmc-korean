# -*- coding: utf-8 -*-
#modified from simpleserver by Jon Berg

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

from os import curdir, sep
import sys
sys.path.append(curdir)
sys.path.append(curdir+sep+'lib')

fetcher = None

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
            self.send_response(200)
            self.send_header('Content-type', 'text/xml')
            self.end_headers()

            if fetcher is None or fetcher.type != "series":
                from scrapers.series.daum import SeriesFetcher
                fetcher = SeriesFetcher()
            if fetcher.meta is None or fetcher.meta.s_id != id:
                fetcher.ParseEpisodePageList(id)
                fetcher.meta.s_id = id
            if fetcher.EpisodeFound:
                xml = "<episodeguide>%s</episodeguide>" % fetcher.meta.GetEpisodeListXML(
                  "http://127.0.0.1:8081/detail?type=daumtv&id="+ id + "&season=%d&episode=%d" )
            else:
                lines = []
                lines.append("<episodeguide>")
                for i in range(1,25):
                    lines.append("<episode>")
                    #lines.append("<title>제%d회</title>" % i)
                    lines.append("<url>http://127.0.0.1:8081/detail?type=daumtv&id=%s&season=1&episode=%d</url>" % (id,i))
                    lines.append("<season>1</season>")
                    lines.append("<epnum>%d</epnum>" % i)
                    lines.append("</episode>")
                lines.append("</episodeguide>")
                xml = ''.join(lines)

            self.wfile.write(xml)
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
            self.send_header('Content-type', 'text/xml')
            self.end_headers()
            if fetcher.EpisodeFound:
                xml = fetcher.meta.GetEpisodeDetailXML( season, episode )
            else:
                xml = "<details><title>제%d회</title></details>" % episode
            self.wfile.write(xml)
            return
        if up.path == "/fanart":
            #type = param['type'][0]
            #if type == 'daummusic':
            name = param['name'][0]
            #if param['coding']:
            #    name = name.decode(param['coding'][0])
            print "name: "+name
            self.send_response(200)
            self.send_header('Content-type', 'text/xml')
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
            return
        return
     
def main():
    try:
        server = HTTPServer(('', 8081), MyHandler)
        print 'started kmagent web server...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

