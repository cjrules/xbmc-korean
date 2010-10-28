# -*- coding: utf-8 -*-
"""
    Return OGM url from gomtv.com

    systype: 10000
    subtype: 2
"""

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

class gomtv_downloader:
    txheaders = {
        'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
        'Cookie' : 'ptic=bfcbf4b805bc63344e200391d95069c7; GomVersion=5027; HQPlusVersion=0006'
    }        # full Cookie support is not required

    def getPlayUrl(self,info):
        self.referer = 'http://ch.gomtv.com/%s/%s/%s' \
              % (info['ch'], info['subch'], info['prog'])
        url = 'http://tv.gomtv.com/cgi-bin/gox/gox_channel.cgi?isweb=0&chid=%s&pid=%s&bid=%s&bjvid=%s' \
              % (info['chid'], info['subch'], info['prog'], info['id'])

        req = urllib2.Request(url, None, self.txheaders)
        try: resp=urllib2.urlopen(req)
        except: return None
            
        soup = BeautifulSoup( resp.read(), fromEncoding="euc-kr" )
        list = soup.findAll('ref')
        for ref in list:
            url = ref['href']
            if url[7:url.find('.',7)].isdigit():
                return url.replace('&amp;','&')
            elif url.startswith('gomp2p://'):
                pos1 = url.find('URLLIST=')+8
                pos2 = url.find('%2c&amp;HASHLIST=')
                import urllib
                return urllib.unquote( url[pos1:pos2] )
            elif url.startswith('goms://'):
                print "Unsupported format: "+url
        print "No video streaming comes from IP address?"
        for ref in list:
            print ref['href'].encode('euc-kr')
        return ''

if __name__ == "__main__":
    gom = gomtv_downloader()
    print gom.getPlayUrl( {'ch':'7727', 'chid':'17297', 'subch':'26958', 'prog':'363475', 'id':'279570'} )
# vim: softtabstop=4 shiftwidth=4 expandtab
