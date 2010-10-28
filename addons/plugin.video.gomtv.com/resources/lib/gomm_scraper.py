# -*- coding: utf-8 -*-
"""
  Parse GomTV Mobile page

      ch.gomtv.com/000/111/222
          000 : channel
          111 : sub-channel
          222 : program
"""

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class gomm_scraper:
    agent_str = 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

    # return: array of {name,url}
    def parseProgramPage(self,main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', self.agent_str)
        try: tDoc=urllib2.urlopen(req).read()
        except: return None

        found = []
        strain = SoupStrainer('ul', {'class':'playlist_btn'})
        soup = BeautifulSoup( tDoc, strain, fromEncoding="utf-8" )
        for item in soup.findAll('a', {'onclick':re.compile('setPlay')}):
            idlist = re.compile("'(\d*)'").findall(item['onclick'])
            found.append( {'systype':idlist[0],
                           'chid':idlist[1],
                           'subch':idlist[2],
                           'prog':idlist[3],
                           'id':idlist[5],
                           'title':item.string} )
        if len(found) == 0: # no playlist -> single play button
            strain = SoupStrainer('dd', {'id':'zzimInfo'})
            soup = BeautifulSoup( tDoc, strain, fromEncoding="utf-8" )
            item = soup.find('a', {'onclick':re.compile('setPlay')})
            idlist = re.compile("'(\d*)'").findall(item['onclick'])
            found.append( {'systype':idlist[0],
                           'chid':idlist[1],
                           'subch':idlist[2],
                           'prog':idlist[3],
                           'id':'0',
                           'title':item.string} )
        return found

if __name__ == "__main__":
    scraper = gomm_scraper()
    for vidinfo in scraper.parseProgramPage( 'http://ch.gomtv.com/427/28099/388308' ):
    	print "%s: %s" % (vidinfo['title'], vidinfo['id'])
# vim: softtabstop=4 shiftwidth=4 expandtab
