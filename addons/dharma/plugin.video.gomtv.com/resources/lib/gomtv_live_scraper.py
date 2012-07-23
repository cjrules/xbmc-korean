# -*- coding: utf-8 -*-
"""
  Parse GomTV web page

       Live (experimental)
"""

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

txheaders = {
    'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
    'Cookie' : 'ptic=bfcbf4b805bc63344e200391d95069c7; GomVersion=5027; HQPlusVersion=0006'
} # full Cookie support is not necessary

class gomtv_live_scraper:
    hq_first = False
    chid = 0
    pid = 0
    bid = 0
    sub_list = []
    dispid = 0
    vodid = 0
    mis_id = 0
    liveid = 0
    live_level = 0

    def __init__(self):
        self.prevpage = None
        self.nextpage = None

    def parseLivePage(self,main_url):
        doc=urllib.urlopen( main_url ).read()
        for ch,title in re.compile(r'<a href="/(\d+)">(.*?)</a>').findall(doc):
            title = re.sub(r'<img class="vs".*?/>'," vs ",title)
            addDir(title.decode("euc-kr"),"http://live.gomtv.com/"+ch,22,"")

    def getLiveUrl(self,main_url):
        txhdr = txheaders
        txhdr['User-Agent'] = 'HttpGetFile'
        req = urllib2.Request(main_url, None, txhdr)
        try: resp=urllib2.urlopen(req)
        except: return None
            
        soup = BeautifulSoup( resp.read(), fromEncoding="euc-kr" )
        list = soup.findAll('ref')
        for ref in list:
            url = ref['href']
            if url.startswith('gomp2p://'):
                url2 = url[ url.rfind("&quot;http")+6 : url.rfind("&quot;") ]
                return url2.replace("&amp;","&")
        return ''

    def parseLivePage(self,main_url):
        req = urllib2.Request(main_url, None, txheaders)
        try: tDoc=urllib2.urlopen(req).read()
        except: return None

        query = re.compile('var typeObj(.*?)}\s*}',re.S).search(tDoc)
        if query is None:
            print "%s is not compatible" % main_url
            return None
        grpid,self.liveid,self.live_level = re.compile("'(\d+)'").findall(query.group(1))

    def useHQFirst(self,value):
        self.hq_first = value

if __name__ == "__main__":
    gom = GomTvLib()
    # hotclip parse
    gom.misid = '42929'
    gom.dispid = '23850'
    gom.vodid = '0'
    print gom.getHotclipIds( '42929', '23850', '0' )
    # unsupported movie page
    print gom.getMovieUrls('11099','34678')
    # unsupported video format
    for title,url in gom.getMovieUrls('17917','19822'):
        print "%s: %s" % (title,url)
        print gom.getVideoUrl(url)
# vim: softtabstop=4 shiftwidth=4 expandtab
