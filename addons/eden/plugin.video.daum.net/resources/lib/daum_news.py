# coding=utf-8
"""
  Media News
"""
import urllib,re
import simplejson

class DaumNews:
    root_url = "http://media.daum.net"
    countPerPage = 40
    menu_list = []
    video_list = []
    nextpage = None
    prevpage = None
    def DaumNews(self):
        pass

    def parseTop(self,main_url):
        html = urllib.urlopen(main_url).read()
        jstr = re.search('var originList = new Object\(({.*})\);', html).group(1)
        obj = simplejson.loads(jstr)
        self.menu_list = []
        #-- item list
	qstr = "page=1&countPerPage={0:d}&regdate=".format(self.countPerPage)
        for tv in obj['tvProgramList']:
	    title = "[COLOR FFFF0000]" + tv['title'] + "[/COLOR]"
	    url = self.root_url + "/api/service/tv" + tv['engIdPath'] + ".jsonp?" + qstr
	    self.menu_list.append( (title, url) )
	    for subtv in tv['subTv']:
		title = subtv['title']
		url = self.root_url + "/api/service/tv" + subtv['engIdPath'] + ".jsonp?" + qstr
		self.menu_list.append( (title, url) )

    def parse(self,main_url):
        jstr = urllib.urlopen(main_url).read()
        obj = simplejson.loads(jstr)
        #-- item list
	self.video_list = []
        for item in obj['tv']['newsList']['data']:
            vid_url = item['videoUrl']
            thumb   = item['imageUrl']
            title   = item['title']
            self.video_list.append( (title,vid_url,thumb) )
        #-- page navigation
        psec = obj['tv']['newsList']['pageNavigation']
        if psec['currentPageNo'] > 1:
	    url = re.sub('page=(\d+)', 'page=%d'%(psec['currentPageNo']-1), main_url)
	    self.prevpage = url
	else:
	    self.prevpage = None
        if psec['currentPageNo'] < psec['totalPageCount']:
	    url = re.sub('page=(\d+)', 'page=%d'%(psec['currentPageNo']+1), main_url)
	    self.nextpage = url
	else:
	    self.nextpage = None

if __name__ == "__main__":
    #import sys,os
    #LIB_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..'))
    #if not LIB_DIR in sys.path:
    #    sys.path.append (LIB_DIR)

    site = DaumNews()
    site.parseTop("http://media.daum.net/tv/")
    print "--- Top -----------------------------"
    print site.menu_list[0]
    print len(site.menu_list)

    site.parse("http://media.daum.net/api/service/tv/mbc.jsonp?page=1&countPerPage=8&regdate=")
    print "--- News -----------------------------"
    print site.video_list[0]
    print len(site.video_list)
    print site.prevpage
    print site.nextpage
