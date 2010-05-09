# coding=utf-8
"""
  Get real media stream from Daum
"""
import urllib2
import re

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
        req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
        req.add_header('Referer', referer)
        page = urllib2.urlopen(req);response=page.read();page.close()
        query_match = re.search('''<MovieLocation regdate="\d+" url="([^"]*)" storage="[^"]*"\s*/>''', response)
        if query_match:
            url = re.sub('&amp;','&',query_match.group(1))
            return GetDaumVideo.DaumGetFLV(referer, url)
        xbmc.log( "Fail to find FLV reference with %s" % vid, xbmc.LOGERROR )
        return None

    @staticmethod
    def DaumGetFLV(referer, url):
        #xbmc.log( "daum loc=%s" % url, xbmc.LOGINFO )
        req = urllib2.Request(url)
        req.add_header('Referer', referer)
        page = urllib2.urlopen(req);response=page.read();page.close()
        query_match = re.search('''<MovieLocation movieURL="(.+?)"\s*/>''', response)
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
