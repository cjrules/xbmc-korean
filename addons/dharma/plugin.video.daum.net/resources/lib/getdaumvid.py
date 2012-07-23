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
        if url.startswith("http://movie") or url.startswith("http://tvnews"):     # trailer or news
            match=re.compile('''UI.[^\(]*SWF\("http://flvs.daum.net/flvPlayer.swf\?vid=(.+?)["\&]''').findall(link)
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
        # req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
        req = urllib2.Request("http://videofarm.daum.net/controller/api/open/v1_2/MovieLocation.apixml?trashData=sadjkfasdjkfafjahjfdhajfadjhdasjklfajkldfahjkfadhjkladsflhjkfad&vid="+vid+"&playLoc=tvpot&preset=main")
        req.add_header('Referer', referer)
        page = urllib2.urlopen(req);response=page.read();page.close()
        bs = BeautifulSoup.BeautifulSoup(response)
        urlnode = bs.find("url")
        if urlnode:
            url = re.sub('&amp;','&',urlnode.contents[0])
            query_match = re.search('''out_type=xml''', url)
            if query_match:
                return GetDaumVideo.DaumGetFLV(referer, url)
            return url
        xbmc.log( "Fail to find FLV reference with %s" % vid, xbmc.LOGERROR )
        return None

    @staticmethod
    def yk64_decode(s):
        ss = [s[i] for i in range(len(s))]
        bs = ''.join([BASE64_LIST[ BSFL64_LIST.index(c) ] for c in ss])
        import base64
        return base64.b64decode(bs)

    @staticmethod
    def DaumGetFLV(referer, url):
        #xbmc.log( "daum loc=%s" % url, xbmc.LOGINFO )
        req = urllib2.Request(url)
        req.add_header('Referer', referer)
        page = urllib2.urlopen(req);response=page.read();page.close()
        query_match = re.search('''<MovieLocation\s*movieURL="([^"]*)"\s*/>''', response)
        if query_match:
            return query_match.group(1)
        xbmc.log( "Fail to find FLV location from %s" % url, xbmc.LOGERROR )
        return None

if __name__ == "__main__":
    print '------ Trailer ---------------------'
    print GetDaumVideo.parse('http://movie.daum.net/moviedetail/moviedetailVideoView.do?movieId=50201&videoId=27664')
    print '------ News ---------------------'
    print GetDaumVideo.parse('http://tvnews.media.daum.net/cp/YTN/view.html?cateid=100000&cpid=24&newsid=20100508145507903&p=ytni')
    print '------ Best ---------------------'
    print GetDaumVideo.parse('http://tvpot.daum.net/clip/ClipView.do?clipid=23545528&focus=1&range=0&diff=0&ref=best&featureddate=20100508&weightposition=1&lu=b_today_01')
    print '------ Starcraft ---------------------'
    print GetDaumVideo.parse('http://tvpot.daum.net/clip/ClipView.do?clipid=23167202&lu=game_gamelist_play')

# vim:ts=4:sts=4:sw=4:et
