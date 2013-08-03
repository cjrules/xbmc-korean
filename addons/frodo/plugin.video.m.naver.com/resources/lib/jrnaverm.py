# -*- coding: utf-8 -*-
"""
  m.jr.naver.com
"""
import urllib, urllib2
import re
import simplejson

BrowserAgent = "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) Mobile"

root_url = "http://m.jr.naver.com"

def parseMenu(menuName):
    page_url = root_url + "/%s/list.nhn" %menuName
    req = urllib2.Request(page_url)
    req.add_header("User-Agent", BrowserAgent)
    html = urllib2.urlopen(req).read()

    items = []
    for serviceId, title in re.compile('''<a name="(\d+)" onclick="getContentsList.*, \\\.tvt.*class="tit">(.*)</span>''', re.U).findall(html):
        items.append({"name":title.decode('utf-8'), "serviceId":serviceId, "thumb":""})
    return items

def getContentsCount(menuName, serviceId):
    url = root_url + "/vod/ajaxGetContentsListCount.nhn?serviceId=%s&recommendAge=all&menuName=%s" %(serviceId, menuName)
    req = urllib2.Request(url)
    req.add_header("User-Agent", BrowserAgent)
    count = urllib2.urlopen(req).read()
    return count

def parseVideoList(menuName, serviceId, pageOffset, dispCount):
    values = {
        "menuName" : menuName,
        "serviceId" : serviceId,
        "sort" : "update",
        "recommendAge" : "all",
        "reqType" : "ajax",
        "pageOffset" : pageOffset,
        "display" : dispCount,
    }
    page_url = root_url + "/vod/ajaxGetContentsList.nhn"
    req = urllib2.Request(page_url, urllib.urlencode(values))
    req.add_header("User-Agent", BrowserAgent)
    html = urllib2.urlopen(req).read()

    items = []
    ptn_clean = re.compile(r"[\\\n\r\t]*")
    for link, thumb, title in re.compile('<a href="(/[^"]*)">[^<]*<span class="thm"><img src="([^"]*)".*?<span class="tit">(.*?)</span>', re.U|re.S).findall(html):
    	title = title.decode('utf-8')
    	title = ptn_clean.sub('', title)
    	items.append({'title':title, 'link':link, 'thumb':thumb})

    return items

def parseVideoPage(page_url):
    req = urllib2.Request(page_url)
    req.add_header("User-Agent", BrowserAgent)
    html = urllib2.urlopen(req).read()

    title = re.search('title\s*:\s*"(.*?)"', html).group(1).decode('utf-8')

    # video
    vid, key = re.compile("RMCVideoPlayer\('([^']*)', *'([^']*)',").search(html).group(1,2)
    new_url = "http://serviceapi.rmcnmv.naver.com/ui/getVideoInfoRMC.nhn?videoId="+vid+"&inKey="+key+"&jsonp=vodPlayer.evaluateJSONP&protocol=http"
    req = urllib2.Request(new_url)
    req.add_header("User-Agent", BrowserAgent)
    req.add_header("Referer", page_url)
    jstr = urllib2.urlopen(req).read()
    json = simplejson.loads( jstr[jstr.find('{') : jstr.rfind('}')+1] )
    return {"title":title, "path":json['playUrl'], "thumbnail":json['coverImage']}

if __name__ == "__main__":
    print parseMenu("tv")

    print getContentsCount("tv", "75")

    result = parseVideoList("tv", "75", 0, 10)
    print len(result)
    print result[0]

    url = root_url+result[0]['link']
    print url
    print parseVideoPage(root_url+result[0]['link'])

# vim:sts=4:et
