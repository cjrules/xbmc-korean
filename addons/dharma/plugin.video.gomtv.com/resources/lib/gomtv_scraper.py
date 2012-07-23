# -*- coding: utf-8 -*-
"""
  Parse GomTV web page

      ch.gomtv.com/000/111/222
          000 : channel
          111 : sub-channel
          222 : program
"""

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

txheaders = {
    'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
    'Cookie' : 'ptic=bfcbf4b805bc63344e200391d95069c7; GomVersion=5027; HQPlusVersion=0006'
} # full Cookie support is not necessary

class gomtv_scraper:
    def __init__(self, hq=False):
        self.prevpage = None
        self.nextpage = None
        self.hq_first = hq

    #----------------------------------------------
    # return: array of {name, url, thumb}
    def parseChPage(self,main_url):
        link=urllib2.urlopen(main_url)
        strain = SoupStrainer( "div", { "id" : "ch_menu" } )
        soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
        #-- channel menu
        found = []
        for item in soup.findAll('p'):
            if item['class'] == 'mbin_tit':
                if item.span and item.span.string:
                    found.append( {'name':item.span.string, 'url':'', 'thumb':''} )
            elif item['class'] == 'mbin_list_s':
                url = ''
                for key,value in item.a.attrs:
                    if key == 'href':
                        url = value
                        break
                if re.compile('http://ch.gomtv.com/\d+/\d+').match(url):
                    found.append( {'name':item.a.span.string, 'url':url, 'thumb':''} )
        self.prevpage = None
        self.nextpage = None
        return found

    # return: array of {name, url, thumb}
    def parseSubChPage(self,main_url):
        link=urllib2.urlopen(main_url)
        soup = BeautifulSoup( link.read(), fromEncoding="euc-kr" )
        #-- item list
        strain1 = SoupStrainer( "table", { "id" : "program_text_list" } )
        strain2 = SoupStrainer( "dl", { "class" : "text_list" } )
        list1 = soup.find(strain1).findAll(strain2)
        found = []
        for item in list1:
            refs = item.findAll('a')
            url = refs[0]['href']
            thumb = refs[0].find('img')['src']
            title = refs[1].contents[0].replace('&amp;','&')
            found.append( {'name':title, 'url':url, 'thumb':thumb} )
        #-- next page
        strain = SoupStrainer( "table", { "class" : "page" } )
        curpg = soup.find(strain).find("td", {"class" : re.compile("^on")})
        if curpg and curpg['class'] != "on last":
            url = curpg.findNextSibling('td').find('a')['href']
            self.nextpage = url
        else:
            self.nextpage = None
        self.prevpage = None
        return found

    def parseProgramPage(self,main_url):
        req = urllib2.Request(main_url, None, txheaders)
        try: tDoc=urllib2.urlopen(req).read()
        except: return None

        #-- ch/chid/pid/bid & default bjvid
        query1 = re.search("'ch' : '(\d+)'", tDoc)
        query2 = re.compile('obj\.useNoneImg(.*?)if\(isFirst\)',re.S).search(tDoc)
        if query1 is None or query2 is None:
            print "%s is not compatible" % main_url
            return None
        ch = query1.group(1)
        chid,pid,bjvid,bid = re.compile("'(\d+)'").findall( query2.group(1) )

        #-- check playlist table
        found = []
        soup = BeautifulSoup( tDoc, fromEncoding="euc-kr" )
        if self.hq_first:
            plist = soup.find("ul", {"id" : "widgetTabs1"})     # HQ first
            if plist is None:
                plist = soup.find("ul", {"id" : "widgetTabs2"})
        else:
            plist = soup.find("ul", {"id" : "widgetTabs2"})     # Std first
            if plist is None:
                plist = soup.find("ul", {"id" : "widgetTabs1"})
        if plist:
            #-- bjvid from table
            for item in plist.findAll('a'):
                ref = item['href']
                id = ref[ref.rfind('(')+1:ref.rfind(',')]
                title = item['title']
                title = title[:title.find('\n')]
                found.append( {'title':title, 'ch':ch, 'chid':chid, 'subch':pid, 'prog':bid, 'id':id} )
        else:
            #-- bjvid for single
            match = re.compile('this\.arr(?:High|Low)Bjoinv\s*=\s*\[(\d+)\];').findall(tDoc)
            if len(match) == 2:
                if self.hq_first: bjvid = match[0]
                else:             bjvid = match[1]
            found.append( {'title':'PLAY', 'ch':ch, 'chid':chid, 'subch':pid, 'prog':bid, 'id':bjvid} )    # single video
        self.prevpage = None
        self.nextpage = None
        return found

    #------------------------------------
    # return: array of {name, url, thumb}
    def parseMusicChartPage(self,main_url):
        link=urllib2.urlopen(main_url)
        soup = BeautifulSoup( link.read(), fromEncoding="euc-kr" )
        #-- item list
        found = []
        strain = SoupStrainer( "table", { "id" : "neo_wchart_list" } )
        for item in soup.find(strain).findAll('td', {'class':'left'}):
            url = item.find('a')['href']
            thumb = item.find('img',{'width':'72','height':'52'})['src']
            title = item.find('dd',{'class':'wchart_tit'}).a.string
            title = title.replace('&amp;','&')
            found.append( {'name':title, 'url':url, 'thumb':thumb} )
        #-- next page
        self.prevpage = None
        self.nextpage = None
        strain = SoupStrainer( "div", { "class" : "neo_wchart_index" } )
        thispage = soup.find(strain).find('a', {"class" : "cho_on"})
        if thispage:
            nextpage = thispage.findNextSibling('a')
            if nextpage:
                self.nextpage = "http://www.gomtv.com"+nextpage['href']
        return found

    #------------------------------------
    # return: array of {name, url, thumb}
    def parseHotListPage(self,url):
        link=urllib2.urlopen( url )
        strain = SoupStrainer('ul', {"class" : "lnb_list"})
        soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
        found = []
        for item in soup.findAll('li', {"class" : "mbin_list_1"}):
            ref = item.find('a')
            found.append( {'name':ref.contents[0], 'url':"http://www.gomtv.com"+ref['href'], 'thumb':''} )
        self.prevpage = None
        self.nextpage = None
        return found

    # return: array of {name, url, thumb}
    def parseHotSubListPage(self,url):
        link=urllib2.urlopen( url )
        strain = SoupStrainer('ul', {"id" : "tab_menu"})
        soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
        found = []
        for item in soup.findAll('li'):
            ref = item.find('a')
            found.append( {'name':ref.contents[0], 'url':"http://www.gomtv.com"+ref['href'], 'thumb':''} )
        self.prevpage = None
        self.nextpage = None
        return found

    # return: array of {name, url, thumb}
    def parseMostWatchedPage(self,main_url):
        link=urllib2.urlopen(main_url)
        soup = BeautifulSoup( link.read(), fromEncoding="euc-kr" )
        #-- item list
        found = []
        for item in soup.findAll('dl', {"id" : "ranking_set"}):
            #title/url
            titblk = item.find('h6').find('a')
            title = titblk.string
            if title:
                title = title.replace('&amp;','&')
            url = titblk['href']
            #thumb
            thumb = ''
            img = item.find('a',{"href" : url}).find('img')
            if img: thumb = img['src']
            found.append( {'name':title, 'url':url, 'thumb':thumb} )
        #-- next page
        strain1 = SoupStrainer( "table", { "class" : "down_page" } )
        strain2 = SoupStrainer( "td", { "class" : "on" } )
        nextpage = soup.find(strain1).find(strain2).findNextSibling('td')
        if nextpage is None: return
        for attr,value in nextpage.attrs:
            if attr == 'class' and value.endswith("nv"):
                return
        self.nextpage = "http://www.gomtv.com"+nextpage.find('a')['href']
        self.prevpage = None
        return found

if __name__ == "__main__":
    scraper = gomtv_scraper()
    print scraper.parseChPage('http://ch.gomtv.com/206')
    print scraper.parseSubChPage('http://ch.gomtv.com/206/27879')
    print scraper.parseProgramPage('http://ch.gomtv.com/206/27879/385692')
    print scraper.parseProgramPage('http://ch.gomtv.com/427/28099/389172')
# vim: softtabstop=4 shiftwidth=4 expandtab
