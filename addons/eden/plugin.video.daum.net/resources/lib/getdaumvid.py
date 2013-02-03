# coding=utf-8
"""
  Get real media stream from Daum
"""
import urllib2
import re

def parse(url):
    response = urllib2.urlopen(url)
    link=response.read()
    response.close()
    match=re.compile('''Video\.html\?vid=(.+?)["\&]''').findall(link)
    if not match:
        match=re.compile('''{\s*vid:\s*"(.*?)",''').findall(link)
    flv_url = []
    for vid in match:
        flv = DaumGetFlvByVid2(url,vid)
        if flv is not None:
            flv_url.append( flv )
    return flv_url

def DaumGetClipInfo(clipid):
    url = "http://tvpot.daum.net/mypot/json/GetClipInfo.do?clipid=%d" % clipid
    jstr = urllib2.urlopen(url).read()
    import simplejson
    obj = simplejson.loads(jstr)
    clip = obj['clip_bean'];
    return (clip['title'], clip['vid'], clip['thumb_url'])

def DaumGetFlvByVid(referer, vid):
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
        url = yk64_decode(url)
    url = re.sub('&amp;','&',url)
    return DaumGetFLV(referer, url)

def DaumGetFlvByVid2(referer, vid):
    url = "http://videofarm.daum.net/controller/api/open/v1_2/MovieLocation.apixml?preset=main"
    if referer and referer.find("movie.daum.net") >= 0:
        url += "&playLoc=daum_movie"
    else:
        url += "&playLoc=tvpot"
    url += "&vid="+vid

    req = urllib2.Request(url)
    if referer:
        req.add_header('Referer', referer)
    resp = urllib2.urlopen(req); xml = resp.read(); resp.close()
    query_match = re.search(r"!\[CDATA\[(http.*?)\]\]", xml)
    if query_match is None:
        print "Fail to find FLV reference with %s" % vid
        print xml
        return None
    return query_match.group(1)

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

BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
BSFL64_CHARS = "abcdeWXYZMNOPQRSTUVEFGHIJKLmnopqrstuvwxyzfghijkABCDl0123456789-_$"
BASE64_LIST = [BASE64_CHARS[i] for i in range(len(BASE64_CHARS))]
BSFL64_LIST = [BSFL64_CHARS[i] for i in range(len(BSFL64_CHARS))]

def yk64_decode(s):
    ss = [s[i] for i in range(len(s))]
    bs = ''.join([BASE64_LIST[ BSFL64_LIST.index(c) ] for c in ss])
    import base64
    return base64.b64decode(bs)

if __name__ == "__main__":
    print '------ Trailer ---------------------'
    print parse('http://movie.daum.net/moviedetail/moviedetailVideoView.do?movieId=50201&videoId=27664')
    print '------ Best ---------------------'
    print parse('http://tvpot.daum.net/clip/ClipView.do?clipid=23545528&focus=1&range=0&diff=0&ref=best&featureddate=20100508&weightposition=1&lu=b_today_01')
    print '------ Starcraft ---------------------'
    print parse('http://tvpot.daum.net/clip/ClipView.do?clipid=23167202&lu=game_gamelist_play')

# vim:ts=4:sts=4:sw=4:et
