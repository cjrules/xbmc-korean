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
        flv = DaumGetFlvByVid(url,vid)
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

# vim:ts=4:sts=4:sw=4:et
