# coding=utf-8
"""
  Kids JJang
"""
import urllib,re

class DaumKids:
    root_url = "http://infant.kids.daum.net"
    countPerPage = 40
    menu_list = []
    video_list = []
    nextpage = None
    prevpage = None
    def DaumKids(self):
        pass

    def parseTop(self,main_url):
        html = urllib.urlopen(main_url).read()

        #-- menu list
        secstr = re.compile('<ul +id="listContent"(.*?)</ul>',re.S).search(html).group(1)

        match = re.compile('<a href="(.*?)" title="(.*?)">\s*<img src="(.*?)"',re.S).findall(secstr)
        self.menu_list = []
        for url,title,thumb in match:
            fullurl = self.root_url+url
            self.menu_list.append( (title.decode('utf-8'), fullurl, thumb) )

    def parseSeries(self,main_url):
        html = urllib.urlopen(main_url).read()
        match = re.compile('<a href="(.*?)" class="link_vodtop.*?" title="(.*?)"').findall(html)
        self.menu_list = []
        for url,title in match:
            fullurl = self.root_url+url
            self.menu_list.append( (title.decode('utf-8'), fullurl, '') )

    def parse(self,main_url):
        baseurl = main_url[:main_url.rfind('/')+1]
        html = urllib.urlopen(main_url).read()

        #-- video list
        self.video_list = []
        query = re.compile('<ul +id="contentsList"(.*?)</ul>',re.S).search(html)
        if query:
            secstr = query.group(1)
            match = re.compile('<a href="(.*?)" class="link_thumb".*?>\s*<img src="(.*?)".*?alt="(.*?)"',re.S).findall(secstr)
            for url,thumb,title in match:
                fullurl = baseurl+url
                self.video_list.append( (title.decode('utf-8'), fullurl, thumb) )
            #-- page navigation
            secstr = re.compile('<div +class="paging_comm"(.*?)</div>',re.S).search(html).group(1)
            query = re.compile('<a href="(.*?)".*</a>\n\s*<span class="screen_out">').search(secstr)
            if query:
                self.prevpage = baseurl+query.group(1)
            else:
                self.prevpage = None
            query = re.compile('<span class="screen_out">.*</em>\n\s*<a href="(.*?)"').search(secstr)
            if query:
                self.nextpage = baseurl+query.group(1)
            else:
                self.nextpage = None

        #-- menu list
        self.menu_list = []
        query = re.compile('<ul +class="list_sub_tab"(.*?)</ul>',re.S).search(html)
        if query:
            secstr = query.group(1)
            match = re.compile('<li *>\s*\n\s*<a href="(.*?)" class="tit_tab.*?">(.*?)</a>').findall(secstr)
            for url,title in match:
                fullurl = self.root_url+url
                self.menu_list.append( (title.decode('utf-8'), fullurl, '') )

    def extract_video_id(self,main_url):
        html = urllib.urlopen(main_url).read()
        return re.compile('playFlashPlayerMovie\("(.*?)"').search(html).group(1)

if __name__ == "__main__":
    #import sys,os
    #LIB_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..'))
    #if not LIB_DIR in sys.path:
    #    sys.path.append (LIB_DIR)

    site = DaumKids()
    site.parseTop("http://infant.kids.daum.net/vod")
    print "--- Top -----------------------------"
    print len(site.menu_list)
    print site.menu_list[0]

    #site.parse(site.root_url+"/vod/pororo")
    site.parseSeries(site.menu_list[0][1])
    print "--- Series --------------------------"
    print len(site.menu_list)
    print site.menu_list[0]

    #site.parse(site.root_url+"/vod/list?categoryId=3025")
    site.parse(site.menu_list[0][1])
    print "--- List ----------------------------"
    print len(site.video_list)
    print site.video_list[0]
    print site.prevpage
    print site.nextpage
    print len(site.menu_list)
    print site.menu_list[0]

    print "--- ID ----------------------------"
    vid = site.extract_video_id(site.video_list[0][1])
    print vid
# vim:sts=4:et
