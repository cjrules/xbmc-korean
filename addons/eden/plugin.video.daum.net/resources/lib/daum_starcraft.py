# coding=utf-8
"""
  Movie Trailer
"""
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer

class DaumStarcraft:
    root_url = "http://tvpot.daum.net"
    menu_list = []
    video_list = []
    prevpage = None
    nextpage = None
    def DaumStarcraft(self):
        pass

    def parseTop(self,url):
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup( html, fromEncoding="utf-8" )
        self.menu_list = []
        base_url = url[:url.rfind('/')+1]
        #-- item list
        strain = SoupStrainer( "div", { "class" : "schedule" } )
        items = soup.find("div", {"class" : "schedule"}).find("ul", {"class" : "pulldownList hidden"}).findAll('a')
        for item in items:
	    vid_url = self.translate_url(item['href'], base_url)
            title   = item.contents[0]
            self.menu_list.append( (title,vid_url) )

    def parse(self,main_url):
        html = urllib.urlopen(main_url).read()
        soup = BeautifulSoup( html, fromEncoding="utf-8" )
        self.video_list = []
        self.prevpage = None
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
		    vid_url = self.translate_url(refs[2]['href'], base_url)
                elif len(refs) == 1:
                    stitle = set.find('dd').contents[0]
		    vid_url = self.translate_url(refs[0]['href'], base_url)
                else:
                    stitle = ''
                    vid_url = ''
            	set_list.append( (setName, stitle, vid_url) )
            self.video_list.append( (date,cable,mtitle,set_list) )
	#-- page navigation
	sect = soup.find("table", {"class" : "pageNav2"})
	if sect:
	    curpg = sect.find('span', {"class" : "sel"}).parent
	    prevpg = curpg.findPreviousSibling('td')
	    if prevpg:
		self.prevpage = self.translate_url(prevpg.a['href'], base_url)
	    nextpg = curpg.findNextSibling('td')
	    if nextpg:
		self.nextpage = self.translate_url(nextpg.a['href'], base_url)

    def translate_url(self,url,base_url):
	url = url.replace('&amp;','&')
	if url.startswith("http"):
	  pass
	elif url.startswith("/"):
	  url = self.root_url + url
	else:
	  url = base_url + url
        return url

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
