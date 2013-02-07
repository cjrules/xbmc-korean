# coding=utf-8
"""
  Best video clip
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class DaumBestClip:
    root_url = "http://tvpot.daum.net"
    video_list = []
    prevpage = None
    nextpage = None
    def DaumBestClip(self):
        pass
    def parse(self,url):
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup( html, fromEncoding="utf-8" )
        self.video_list = []
        self.prevpage = None
        self.nextpage = None
        #-- item list
        items = soup.findAll("dl",{"class":"bestclip"})
        for item in items:
            ddimg = item.find("dd",{"class":"image"})
            vid_url = ddimg.find('a')['href']
            if vid_url[0] == '/':
                vid_url = self.root_url + vid_url
            imgpt = ddimg.find('img')
            thumb = imgpt['src']
            title = imgpt['alt']
            self.video_list.append( (title,vid_url,thumb) )
        #-- page
	query = re.search('page=(\d+)',url)
	if query:
            pgnum = int(query.group(1))
            if pgnum > 1:
                self.prevpage = url.replace("page=%d"%pgnum, "page=%d"%(pgnum-1))
            self.nextpage = url.replace("page=%d"%pgnum, "page=%d"%(pgnum+1))
        else:
            self.nextpage = url+"&page=2"

if __name__ == "__main__":
    #import sys,os
    #LIB_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..'))
    #if not LIB_DIR in sys.path:
    #    sys.path.append (LIB_DIR)

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/TotalBest.do?dateterm=all&playterm=all&sort=play")
    print "--- BEST 0 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/TotalBest.do?dateterm=week&playterm=all&sort=play")
    print "--- BEST 1 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/TotalBest.do?dateterm=all&playterm=50M&sort=play")
    print "--- BEST 2 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/TotalBest.do?dateterm=all&playterm=all&sort=wtime")
    print "--- BEST 3 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage
# vim:ts=8:sts=4:sw=4:et
