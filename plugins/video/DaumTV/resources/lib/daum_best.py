# coding=utf-8
"""
  Best video clip
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class DaumBestClip:
    video_list = []
    nextpage = None
    def DaumBestClip(self):
        pass
    def parse(self,url):
        link = urllib.urlopen(url)
        soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
        self.video_list = []
        self.nextpage = None
        #-- item list
        strain = SoupStrainer( "div", { "id" : "thumbList" } )
        items = soup.find(strain).findAll('dl')
        for item in items:
            ddimg = item.find('dd',{'class' : 'img'})
            vid_url = ddimg.find('a')['href'].replace("&amp;","&")
            if vid_url[0] == '/':
                vid_url = "http://tvpot.daum.net"+vid_url
            imgpt = ddimg.find('img')
            thumb = imgpt['src']
            title = imgpt['title']
            self.video_list.append( (title,vid_url,thumb) )
        #-- page
        strain = SoupStrainer( "li", { "class" : re.compile('^bar11c') } )
        items = soup.findAll(strain)
        found = False;
        for item in items:
            if (found):
            	temp = item.find('a')
            	url = temp['href'].replace("&amp;","&")
            	if url[0] == '?':
                    url = "http://tvpot.daum.net/best/BestToday.do"+url
                self.nextpage = (temp['title'], url)
                break
            if item['class'].startswith("bar11c  selected"):
            	found = True;

if __name__ == "__main__":
    #import sys,os
    #LIB_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..'))
    #if not LIB_DIR in sys.path:
    #    sys.path.append (LIB_DIR)

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/BestToday.do?svctab=best&range=0")
    print "--- BEST 0 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/BestToday.do?svctab=best&range=1")
    print "--- BEST 1 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/BestToday.do?svctab=best&range=2")
    print "--- BEST 2 -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage

    site = DaumBestClip()
    site.parse("http://tvpot.daum.net/best/BestToday.do?svctab=10m")
    print "--- 10m -------------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage
