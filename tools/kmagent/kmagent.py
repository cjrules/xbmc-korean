#modified from simpleserver by Jon Berg

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

from os import curdir, sep
import sys
sys.path.append(curdir)
sys.path.append(curdir+sep+'lib')

fetcher = None
last_id = 0

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global fetcher,last_id
        up = urlparse.urlparse(self.path)
        param = urlparse.parse_qs(up.query)
        print "cmd: "+up.path
        if up.path == "/fetch":
            id = param['id'][0]
            print "id: "+id
            self.send_response(200)
            self.send_header('Content-type', 'text/xml')
            self.end_headers()

            if last_id != id:
                fetcher.ParseEpisodePageList(id)
                last_id = id
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
            if last_id != param['id'][0]:
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
    from scrapers.series.daum import SeriesFetcher
    fetcher = SeriesFetcher()
    main()

