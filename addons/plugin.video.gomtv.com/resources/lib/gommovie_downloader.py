# -*- coding: utf-8 -*-
"""
    Return OGM url from movie.gomtv.com

    systype: 10000
    subtype: 2
"""

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class gommovie_downloader:
    txheaders = {
        'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
        'Cookie' : 'ptic=bfcbf4b805bc63344e200391d95069c7; GomVersion=5027; HQPlusVersion=0006'
    }        # full Cookie support is not required
    gom_errors = {
        "1000" : "영상 재생에 문제가 발생했습니다. 잠시 후 다시 이용해 주세요.",
        "1001" : "영상 재생에 문제가 발생했습니다.",
        "1010" : "선택하신 화질의 영상은 현재 서비스 되고 있지 않습니다.",
        "1020" : "해당 영상은 대한민국 내에서만 시청하실 수 있습니다.",
        "1030" : "19세 미만은 본 영상을 시청하실 수 없습니다.",
        "1040" : "결제?",
        "1041" : "결제 해야되서 로그인",
        "1050" : "해당 영상을 재생하는데 일시적인 오류가 발생하였습니다. 잠시 후 다시 이용 부탁드립니다.",
        "1051" : "해당 영상은 현재 서비스 일시 중단한 영상입니다.",
        "1060" : "영상 재생에 문제가 발생했습니다. - parameter error - ",
        "1070" : "결제 필요",
        "1071" : "패키지 구매가 필요한 영상입니다.",
        "1080" : "보다 좋은 서비스를 위해 현재 시스템을 점검중에 있습니다. \n이용에 불편을 드려 죄송합니다.",
        "1500" : "해당 생중계는 현재 방송중이 아닙니다.",
        "1510" : "사용량 초과.",
        "1520" : "해당 생중계는 현재 방송중이 아닙니다.\n(이미 해당 생중계를 보고 있습니다.)",
        "1700" : "해당 영상에 시청 권한이 없습니다."
    }

    def __init__(self):
        import random
        self.req_ip = "147.46.%d.%d" % (random.randint(0,255), random.randint(1,255))

    def getMovieUrls(self,info):
        req_url = 'http://movie.gomtv.com/common/ajax/getGoxUrlToJson.gom'
        param_templ = ['param=', 'dsi=null', 'onlyIE=n',
                       'uip=%s', 'dispid=%s', 'vodid=%s',
                       'part=1', 'level=2',
                       'isMultiPlay=false', 'isPlay=true',
                       'async=false', 'serv=100', 'adult=F',
                       'isweb=1', 'isnav=1', 'navurl=', 'source=',
                       'os=Windows', 'browser=MSIE8.0',
                       '&property=movie']

        txdenc = '|||||'.join(param_templ) % (self.req_ip, info['dispid'], info['vodid'])

        req = urllib2.Request(req_url, txdenc, self.txheaders)
        urls = []
        try:
            resp = urllib2.urlopen(req)
            data = resp.read()
            code = re.compile('"error":"?(\d+)').search(data).group(1)
            if code == "0":
                titles = re.compile('"title":\[(.*)\],"url"').search(data).group(1)[1:-1].split('","')
                urls = re.compile('"url":\[(.*)\],"error"').search(data).group(1)[1:-1].replace("\\/","/").split('","')
            else:
                print self.gom_errors[code]
            resp.close
        except IOError, e:
            print "ERROR with movie (ajax)"
            if hasattr(e,'code'):
                print "Failed with code - %s" % e.code
        mov_urls = []
        for i in range(0,len(urls)):
            mov_urls.append( (titles[i].decode("unicode_escape"), urls[i]) )
        return mov_urls

if __name__ == "__main__":
    downloader = gommovie_downloader()
    print downloader.getMovieUrls( {'dispid':'14025', 'vodid':'27354'} )
# vim: softtabstop=4 shiftwidth=4 expandtab
