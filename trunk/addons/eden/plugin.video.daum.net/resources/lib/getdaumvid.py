# coding=utf-8
"""
  Get real media stream from Daum
"""
import urllib2
import re

BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
BSFL64_CHARS = "abcdeWXYZMNOPQRSTUVEFGHIJKLmnopqrstuvwxyzfghijkABCDl0123456789-_$"
BASE64_LIST = [BASE64_CHARS[i] for i in range(len(BASE64_CHARS))]
BSFL64_LIST = [BSFL64_CHARS[i] for i in range(len(BSFL64_CHARS))]

class GetDaumVideo:
    @staticmethod
    def parse(url):
        response = urllib2.urlopen(url)
        link=response.read()
        response.close()
        if url.startswith("http://movie"):  # trailer
            match=re.compile('''VideoView\.html\?vid=(.+?)["\&]''').findall(link)
        else:
            # daumEmbed_jingle2 had 3 arguments, but daumEmbed_standard had 4
            match=re.compile('''daumEmbed_.+?\('.+?','(.+?)','.+?'[,\)]''').findall(link)
        flv_url = []
        for vid in match:
                flv = GetDaumVideo.DaumGetFlvByVid(url,vid)
                if flv is not None:
                    flv_url.append( flv )
        return flv_url

    @staticmethod
    def DaumGetFlvByVid(referer, vid):
        print "daum vid=%s" % vid
        req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
        if referer:
            req.add_header('Referer', referer)
        response = urllib2.urlopen(req);xml=response.read();response.close()
        query_match = re.search('''<MovieLocation [^>]*url="([^"]*)"[^>]*/>''', xml)
        if query_match is None:
            print "Fail to find FLV reference with %s" % vid
            print xml
            return None
        url = query_match.group(1)
        if not url.startswith("http"):
            url = GetDaumVideo.yk64_decode(url)
        url = re.sub('&amp;','&',url)
        return GetDaumVideo.DaumGetFLV(referer, url)

    @staticmethod
    def yk64_decode(s):
        ss = [s[i] for i in range(len(s))]
        bs = ''.join([BASE64_LIST[ BSFL64_LIST.index(c) ] for c in ss])
        import base64
        return base64.b64decode(bs)

    @staticmethod
    def DaumGetFLV(referer, url):
        print "daum loc=%s" % url
        req = urllib2.Request(url)
        if referer:
            req.add_header('Referer', referer)
        response = urllib2.urlopen(req);xml=response.read();response.close()
        query_match = re.search('''<MovieLocation\s*[^>]*movieURL="([^"]*)"\s*/>''', xml)
        if query_match:
            return query_match.group(1)
        print "Fail to find FLV location from %s" % url
        print xml
        return None

if __name__ == "__main__":
    print '------ Trailer ---------------------'
    print GetDaumVideo.parse('http://movie.daum.net/moviedetail/moviedetailVideoView.do?movieId=50201&videoId=27664')
    print '------ Best ---------------------'
    print GetDaumVideo.parse('http://tvpot.daum.net/clip/ClipView.do?clipid=23545528&focus=1&range=0&diff=0&ref=best&featureddate=20100508&weightposition=1&lu=b_today_01')
    print '------ Starcraft ---------------------'
    print GetDaumVideo.parse('http://tvpot.daum.net/clip/ClipView.do?clipid=23167202&lu=game_gamelist_play')

# vim:ts=4:sts=4:sw=4:et