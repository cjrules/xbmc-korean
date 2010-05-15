# coding=utf-8
"""
  Best video clip
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class DaumBrand:
    video_list = []
    nextpage = None
    def DaumBrand(self):
        pass
    def parse(self,url):
        link = urllib.urlopen(url)
        soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
        self.video_list = []
        self.nextpage = None
        #-- item list
        strain = SoupStrainer( "div", { "class" : re.compile("^listBody") } )
        items = soup.find(strain).findAll('dl')
        for item in items:
            ddimg = item.find('dd',{'class' : 'image'})
            vid_url = ddimg.find('a')['href'].replace("&amp;","&")
            vid_url = vid_url.replace("&amp;","&").replace(" ","")
            if vid_url[0] == '/':
                vid_url = "http://tvpot.daum.net"+vid_url
            imgpt = ddimg.find('img')
            thumb = imgpt['src']
            title = imgpt['title']
            query = re.compile(u"동영상 '(.*?)'의 미리보기 이미지").match(title)
	    if query:
		title = query.group(1)
            self.video_list.append( (title,vid_url,thumb) )
        #-- next page
        pages = soup.find("table", {"class" : "pageNav2"}).findAll( ('td','th') )
        found = False
        for page in pages:
            if found:
            	url = page.find('a')['href'].replace("&amp;","&")
            	if url.startswith("/"):
                    url = "http://tvpot.daum.net"+url
            	self.nextpage = url
            	break
            if page.find('span', {"class" : "sel"}):
            	found = True

if __name__ == "__main__":
    #import sys,os
    #LIB_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..'))
    #if not LIB_DIR in sys.path:
    #    sys.path.append (LIB_DIR)

    site = DaumBrand()
    site.parse("http://tvpot.daum.net/brand/ProgramView.do?ownerid=O_5rgf7M1do0&playlistid=1101578&lu=b_c_main_programlist_cate_2")
    print len(site.video_list)
    print site.video_list[0]
    print site.nextpage
