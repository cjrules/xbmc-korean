# coding=utf-8
"""
  Movie Trailer
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class DaumTrailer:
    video_list = []
    def DaumTrailer(self):
        pass
    def parse(self,url):
        link = urllib.urlopen(url)
        soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
        self.video_list = []
        #-- item list
        strain = SoupStrainer( "td", { "class" : re.compile("^td2") } )
        items = soup.findAll(strain)
        for item in items:
            refs = item.findAll('a')
            vid_url = refs[-1]['href'].replace("&amp;","&")
            title   = refs[-1].contents[0]
            if len(refs) > 1:
                thumb = refs[0].find('img')['src']
            self.video_list.append( (title,vid_url,thumb) )

if __name__ == "__main__":
    #import sys,os
    #LIB_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..'))
    #if not LIB_DIR in sys.path:
    #    sys.path.append (LIB_DIR)

    site = DaumTrailer()
    site.parse("http://movie.daum.net/ranking/movieclip_ranking/bestTrailer.do?datekey=3")
    print "--- Trailer 0 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)

    site.parse("http://movie.daum.net/ranking/movieclip_ranking/bestTrailer.do?datekey=2")
    print "--- Trailer 1 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)

    site.parse("http://movie.daum.net/ranking/movieclip_ranking/bestTrailer.do?datekey=1")
    print "--- Trailer 2 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
