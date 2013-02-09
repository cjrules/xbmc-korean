# -*- coding: utf-8 -*-
"""
  Parse GomTV Movie page

      movie.gomtv.com/000
          000 : movie id
"""

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class gommovie_site:
    def __init__(self):
        self.prevpage = None
        self.nextpage = None

    def parseMoviePage(self,main_url):
        try: tDoc=urllib.urlopen(main_url).read()
        except: return None
        query = re.compile("http://movie.gomtv.com/sub/detailAjax.\gom\?misid=(\d+)&dispid=(\d+)&vodid=(\d+)&mtype=5").search(tDoc)
        if query is None:
            return {}
        return {'misid':query.group(1), 'dispid':query.group(2), 'vodid':query.group(3)}

    def parseMovieHotClipPage(self, main_url):
        try: tDoc=urllib.urlopen(main_url).read()
        except: return []

        strain = SoupStrainer('div', {"class" : "widgetMinMax"})
        soup = BeautifulSoup( tDoc, strain, fromEncoding="euc-kr" )
        out_list = []
        for item in soup.contents[1].findAll("dl", {"class" : "list_join_small2"}):
            ta = item.find('dd', {"class":"title"}).find('a')
            clipid = re.compile("clipid:'(\d+)'").search( ta['onclick'] ).group(1)
            title = ta.string.replace('&quot;','"')
            thumb = item.find('img', {"class":"thum"})['src']
            out_list.append( {'clipid':clipid, 'name':title, 'thumb':thumb} )
        return out_list

    def parseMovieChartPage(self,main_url):
        resp=urllib.urlopen(main_url)
        strain = SoupStrainer( "div", { "id" : "sub_center" } )
        soup = BeautifulSoup( resp.read(), strain, fromEncoding="euc-kr" )
        #-- item list
        found = []
        strain = SoupStrainer( "div", { "id" : "program_poster" } )
        for item in soup.find(strain).findAll("div", {"class" : "poster"}):
            refs = item.findAll('a')
            thumb = refs[0].find('img')['src']
            url = refs[1]['href']
            if url.startswith('/'):
                url="http://movie.gomtv.com"+url
            found.append( {'name':refs[1].string, 'url':url, 'thumb':thumb} )
        #-- next page
        strain = SoupStrainer( "div", { "id" : "page" } )
        curpage = soup.find(strain).find('span')
        nextpage = curpage.findNextSibling('a')
        if nextpage:
            self.nextpage = "http://movie.gomtv.com"+nextpage['href']
        else:
            self.nextpage = None
        prevpage = curpage.findPreviousSibling('a')
        if prevpage:
            self.prevpage = "http://movie.gomtv.com"+prevpage['href']
        else:
            self.prevpage = None
        return found
      
    def parsePremierPage(self,main_url):
        resp=urllib.urlopen(main_url)
        strain = SoupStrainer( "div", { "id" : "sub_center2" } )
        soup = BeautifulSoup( resp.read(), strain, fromEncoding="euc-kr" )
        #-- item list
        found = []
        strain = SoupStrainer( "div", { "id" : "theater_poster" } )
        for item in soup.find(strain).findAll("div", {"class" : "poster"}):
            refs = item.findAll('a')
            thumb = refs[0].find('img')['src']
            found.append( {'name':refs[1].string, 'url':refs[1]['href'], 'thumb':thumb} )
        #-- next page
        strain = SoupStrainer( "div", { "id" : "page" } )
        nextpage = soup.find(strain).find('span').findNextSibling('a')['href']
        self.nextpage = "http://movie.gomtv.com"+nextpage
        return found

    def parseHotClipPage(self,main_url):
        link=urllib.urlopen(main_url)
        strain = SoupStrainer( "div", { "id" : "sub_center2" } )
        soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
        #-- item list
        found = []
        strain = SoupStrainer( "div", { "id" : "hotClip_list" } )
        for item in soup.find(strain).findAll('dl'):
            refs = item.findAll('a')
            thumb = refs[0].find('img')['src']
            url = "http://tv.gomtv.com/cgi-bin/gox/gox_clip.cgi?dispid=%s&clipid=%s" % re.compile('/(\d*)/\d+/\d+/(\d+)').search( refs[1]['onclick'] ).group(1,2)
            found.append( {'name':refs[0]['title'], 'url':url, 'thumb':thumb} )
        self.nextpage = None
        return found
      
    def parseBoxOfficePage(self,main_url):
        link=urllib.urlopen(main_url)
        strain = SoupStrainer( "div", { "id" : "boxOffice_poster" } )
        soup = BeautifulSoup( link.read(), strain, fromEncoding="euc-kr" )
        #-- item list
        found = []
        strain = SoupStrainer( "div", { "class" : "poster" } )
        for item in soup.findAll(strain):
            refs = item.findAll('a')
            thumb = refs[0].find('img')['src']
            found.append( {'name':refs[1].string, 'url':refs[0]['href'], 'thumb':thumb} )
        self.nextpage = None
        return found

if __name__ == "__main__":
    site = gommovie_site()
    print site.parseMoviePage( 'http://movie.gomtv.com/14025' )
    print site.parseMovieHotClipPage( 'http://movie.gomtv.com/sub/detailAjax.gom?misid=15814&dispid=14025&vodid=27354&mtype=5' )
    print site.parseMovieChartPage( 'http://movie.gomtv.com/list.gom?cateid=4' )
    print site.parsePremierPage( 'http://movie.gomtv.com/list.gom?cateid=65' )
    print site.parseHotClipPage( 'http://movie.gomtv.com/release/hotclip.gom' )
    print site.parseBoxOfficePage( 'http://movie.gomtv.com/release/boxoffice.gom' )
# vim: softtabstop=4 shiftwidth=4 expandtab
