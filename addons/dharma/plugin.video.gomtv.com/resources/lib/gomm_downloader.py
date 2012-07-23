# -*- coding: utf-8 -*-
"""
  Download mp4 from m.gomtv.com
"""

import urllib2
import simplejson

class gomm_downloader:
    agent_str = 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

    def getPlayUrl(self,info):
        idpk = (info['systype'], info['chid'], info['subch'], info['prog'], info['id'])
        self.referer = 'http://m.gomtv.com/play.gom?systype=%s&id0s=%s&id1s=%s&id2s=%s&id3s=&nodeid=%s' % idpk

        url = 'http://m.gomtv.com/ajax/getPlayUrl.gom'
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.agent_str)
        req.add_header('Referer', self.referer)
        paras = '&systype=%s&id0s=%s&id1s=%s&id2s=%s&id3s=&nodeid=%s' % idpk
        jsonstr = urllib2.urlopen(req, paras).read()
        import simplejson
        markup = simplejson.loads(jsonstr)
        return markup['playUrl']

    def saveVideo(self,url,fname):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.agent_str)
        req.add_header('Referer', self.referer)
        resp = urllib2.urlopen(req)
        f = open(fname, 'wb')
        f.write( resp.read() )
        f.close()

if __name__ == "__main__":
    gom = GomMobile('http://ch.gomtv.com/427/28099/388308')
    idlist = [17693, 28099, 388308]
    # nodeid = 3219710/3219716/3219710
    url = gom.getPlayUrl(idlist)
    gom.saveVideo( url, idlist, 'a.mp4' )
# vim: softtabstop=4 shiftwidth=4 expandtab
