# coding=utf-8
"""
  Media News
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer

class DaumNews:
    menu_list = []
    video_list = []
    nextpage = None
    prevday = None
    def DaumNews(self):
        pass

    def parseTop(self,url):
        link = urllib.urlopen(url)
        soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
        self.menu_list = []
        #-- item list
        strain = SoupStrainer( "li", { "class" : "M" } )
        items = soup.findAll(strain)
        for item in items:
            ref = item.find('a')
            vid_url = ref['href']
            title   = ref.contents[0]
            self.menu_list.append( (title,vid_url) )

    def parse(self,url):
        link = urllib.urlopen(url)
        soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
        self.video_list = []
        self.nextpage = None
        self.prevday = None
        base_url = url[:url.rfind('/')+1]
        #-- item list
        strain = SoupStrainer( "dl", { "class" : "TV_RL" } )
        items = soup.findAll(strain)
        for item in items:
            refs = item.findAll('a')
            vid_url = base_url + refs[0]['href']
            thumb   = refs[0].find('img')['src']
            title   = refs[1].contents[0]
            self.video_list.append( (title,vid_url,thumb) )
        #-- next page
        psec = soup.find("div", {"class" : "paging"})
        curpg = psec.find('b')
        nextpg = curpg.findNextSibling('a')
        if nextpg:
            pg_url  = base_url + nextpg['href']
            pg_name = nextpg.contents[0].strip()
            self.nextpage = (pg_name,pg_url)
        #-- prev day
        psec = soup.find("p", {"class" : "pagingDay"})
        curday = psec.find('a', {"class" : "on"})
        if curday is None:
            curday = psec.find('a')
        prevday = curday.findNextSibling('a')
        if prevday:
            day_url  = base_url + prevday['href']
            day_name = prevday.contents[0].strip()
            self.prevday = (day_name,day_url)

if __name__ == "__main__":
    #import sys,os
    #LIB_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..'))
    #if not LIB_DIR in sys.path:
    #    sys.path.append (LIB_DIR)

    site = DaumNews()
    site.parseTop("http://tvnews.media.daum.net/")
    print "--- Top -----------------------------"
    print site.menu_list[0]
    print len(site.menu_list)

    site.parse("http://tvnews.media.daum.net/cp/YTN/")
    print "--- News -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.nextpage
    print site.prevday
