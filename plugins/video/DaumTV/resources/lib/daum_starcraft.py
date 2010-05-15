# coding=utf-8
"""
  Movie Trailer
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer

class DaumStarcraft:
    menu_list = []
    video_list = []
    nextpage = None
    def DaumStarcraft(self):
        pass

    def parseTop(self,url):
        link = urllib.urlopen(url)
        soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
        self.menu_list = []
        base_url = url[:url.rfind('/')+1]
        #-- item list
        strain = SoupStrainer( "div", { "class" : "schedule" } )
        items = soup.find("div", {"class" : "schedule"}).find("ul", {"class" : "pulldownList hidden"}).findAll('a')
        for item in items:
            vid_url = base_url + item['href'].replace("&amp;","&")
            title   = item.contents[0]
            self.menu_list.append( (title,vid_url) )

    def parse(self,main_url):
        link = urllib.urlopen(main_url)
        soup = BeautifulSoup( link.read(), fromEncoding="utf-8" )
        self.video_list = []
        self.nextpage = None
        base_url = main_url[:main_url.rfind('/')+1]
        #-- item list
        strain1 = SoupStrainer( "div", { "class" : "schedule" } )
        strain2 = SoupStrainer( "div", { "class" : "matchGroup" } )
        mgrp = soup.find(strain1).findAll(strain2)
        for match in mgrp:
            # match info
            hdr = match.find('h5')
            date = hdr.find('strong').contents[0]
            cable = hdr.contents[1]
            if "league=pro" in main_url:
                teamrefs = match.find('span').findAll('a')
                mtitle = "%s vs %s" % (teamrefs[0].contents[0], teamrefs[1].contents[0])
            elif "league=osl" in main_url:
                mtitle = match.find('p').contents[0].strip()
            else:
                mtitle = ''
            # set
            set_list = []
            for set in match.find("div", {"class" : "pastGame"}).findAll('li'):
            	setName = set.find("strong", {"class" : "set"}).contents[0]
            	refs = set.findAll('a')
            	if len(refs) == 3:
                    stitle = "%s vs %s" % (refs[0].contents[0], refs[1].contents[0])
                    url = refs[2]['href'].replace("&amp;","&")
		    if url.startswith("http"):
			vid_url = url
		    elif url.startswith("/"):
			vid_url = "http://tvpot.daum.net"+url
		    else:
			vid_url = base_url + url
                elif len(refs) == 1:
                    stitle = set.find('dd').contents[0]
                    url = refs[0]['href'].replace("&amp;","&")
		    if url.startswith("http"):
			vid_url = url
		    elif url.startswith("/"):
			vid_url = "http://tvpot.daum.net"+url
		    else:
			vid_url = base_url + url
                else:
                    stitle = ''
                    vid_url = ''
            	set_list.append( (setName, stitle, vid_url) )
            self.video_list.append( (date,cable,mtitle,set_list) )
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

    site = DaumStarcraft()
    site.parseTop("http://tvpot.daum.net/game/sl/LeagueList.do?league=pro&type=list&lu=game_pro_closegame")
    print "--- Proleague Menu ------------------------"
    print site.menu_list[0]
    print len(site.menu_list)

    site.parse("http://tvpot.daum.net/game/sl/LeagueList.do?league=pro&type=list&lu=game_pro_closegame")
    print "--- Proleague -----------------------------"
    print site.video_list[0]
    print "#match: %d" % len(site.video_list)
    print "#set[0]: %d" % len(site.video_list[0][3])
    print site.nextpage

    site.parseTop("http://tvpot.daum.net/game/sl/LeagueList.do?league=osl&type=list&lu=game_osl_closegame")
    print "--- Starleague Menu ------------------------"
    print site.menu_list[0]
    print len(site.menu_list)

    site.parse("http://tvpot.daum.net/game/sl/LeagueList.do?league=osl&type=list&lu=game_osl_closegame")
    print "--- Starleague -----------------------------"
    print site.video_list[0]
    print "#match: %d" % len(site.video_list)
    print "#set[0]: %d" % len(site.video_list[0][3])
    print site.nextpage
