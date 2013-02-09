# -*- coding: utf-8 -*-
"""
  gomtv.com
"""

import urllib, urllib2, re
import simplejson

root_url = "http://www.gomtv.com"

BrowserAgent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
GompAgent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ;  Embedded Web Browser from: http://bsalsa.com/; .NET4.0C)'

def parseProg(main_url):
    vid_info = {}
    html = urllib2.urlopen(main_url).read()

    # node id
    match = re.search(r"this\.arrCommonMid\s*=\s*\[(.*?)\];", html)
    if match is None:
    	return None
    ndstr = match.group(1)
    if len(ndstr):
        nodelist = ndstr.split(',')
    else:
        nodelist = []

    # title
    titlist = re.compile('<li class="pbtn">.*?<span>(.*?)</span></a></li>',re.S).findall(html)
    if len(nodelist) == 1 and len(titlist) == 0:
    	titlist = [ re.compile('<h1[^>]*><a[^>]*>(.*?)</a>',re.U).search(html).group(1) ]

    # output combine
    vid_info['playlist'] = []
    if len(nodelist) <= len(titlist):
        for i in range(len(nodelist)):
            vid_info['playlist'].append( {'title':titlist[i].decode('euc-kr'), 'nodeid':nodelist[i]} )
    else:
    	print "ERROR: #node(%d) > #title(%d)" % (len(nodelist), len(titlist))

    return vid_info

def getPlayUrl(contentsid):
    values = { "arrContentsid":[contentsid],
               "platform_flag":1,  # 1:GomPlayer, 16:HTML5, 32:FLV
               "machine":1,
               "level_flag":4,      # 1:일반화질, 4:고화질, 256:HD, 4096:FullHD
               "attr1":10004,
               "option":1,
               #"pgtype1":urllib.quote("영상상세뷰"),
               #"pgtype2":urllib.quote("게임"),
               "pgtype1":"",
               "pgtype2":"",
               "startPos":1,
               "preview":0,
               "returnPaymentCode":1,
               "playertype":"webPlayer",    # gomPlayer/webPlayer
             }
    jstr = simplejson.dumps(values)
    #print jstr
    req = urllib2.Request(root_url+"/ajaxController.gom")
    req.add_header("User-Agent", BrowserAgent)
    resp = urllib2.urlopen(req, "src=streamingGomGetJs&params="+jstr)
    jstr2 = resp.read()
    resp.close()
    #print jstr2
    json = simplejson.loads(jstr2)
    if json['errorcode'] & 256:
    	print "not allowed outside Korea"
    if json['errorcode'] & 512:
    	print "no playable environment"
    jstr3 = re.search("({.*})", json['playscript']).group(1).replace("'",'"')
    #print jstr3.encode('utf-8')
    # GomtvPlay (defined in img.gomtv.com/js_utf8/common/util-1.0.doc.js?20120809_1)
    json = simplejson.loads(jstr3)
    values2 = []
    for k,v in json.iteritems():
    	if isinstance(v,list):
            v = ','.join(map(str,v))
        else:
            v = urllib.quote(v.encode('utf-8'))
        if k != "playerType" and k != "navurl":
            values2.append(u"%s=%s" % (k,v))
    if json['playerType'] == 'webPlayer':
        values2.append("isweb=1")
        values2.append("onlyIE=n")
        values2.append("os=Windows")
        values2.append("browser=MSIE9.0")
        values2.append("isMultiPlay=false")
        values2.append("player=ax")
        param2 = "|||||".join(values2)
        # webPlayer request
        down_url = root_url+"/ajaxController.gom?src=getCmsGoxUrlToJsonUtf8"
        req = urllib2.Request(down_url)
        req.add_header("User-Agent", BrowserAgent)
        resp = urllib2.urlopen(req, "param=|||||"+param2+"&property=channel")
        jstr4 = resp.read()
        resp.close()
    else:
        param2 = "|||".join(values2)
        # gomPlayer request
        down_url = root_url+"/ajaxController.gom?src=getGoxUrl"
        req = urllib2.Request(down_url)
        req.add_header("User-Agent", BrowserAgent)
        resp = urllib2.urlopen(req, "param="+param2+"&property=")
        jstr4 = resp.read()
        resp.close()
    #print jstr4.encode('utf-8')
    json = simplejson.loads(jstr4)
    print json['gox']['url'][0]
    req = urllib2.Request(json['gox']['url'][0])
    req.add_header("User-Agent", BrowserAgent)
    resp = urllib2.urlopen(req)
    print resp.read()
    return [{"title":json['gox']['title'][i],"url":json['gox']['url'][i]} for i in range(len(json['gox']['title']))]

def getNodeIds(contentsid, seriesid):
    referer = "http://expmini.gomtv.com/view.gom?contentsid=%d&seriesid=%d&seq=&seriesSort=desc&seriesPage=1" % (contentsid, seriesid)
    url = 'http://expmini.gomtv.com/ajaxController.gom?src=getCheckedPlaylist&arrcontents={"0":%d}&arrpromotionid={"0":0}&navurl={"0":"http://expmini.gomtv.com/view.gom?contentsid=%d"}&arrlevelflag={"0":"4"}&arrautolevel={"0":"1"}&notplay=0&onlydown=0&startPos=1&playerType=&arrpgtype1=undefined&arrpgtype2=undefined&arrpgtype3=undefined&arrsource={"0":"0"}' % (contentsid, contentsid)
    cookie = 'GomVersion=5119'
    req = urllib2.Request(url)
    hdrs = {"x-requested-with":"XMLHttpRequest",
            "Referer":referer,
            "User-Agent":GompAgent,
            "Cookie":cookie,
           }
    #resp = urllib2.urlopen(req, "", hdrs)
    for k,v in hdrs.iteritems():
    	req.add_header(k,v)
    resp = urllib2.urlopen(req)
    jstr = resp.read()
    resp.close()
    json = simplejson.loads(jstr)
    nidlist = [item["nodeid"] for item in json["errordomesticlist"]]
    return nidlist

if __name__ == "__main__":
    print getNodeIds(555443, 1029262)
    #print getPlayUrl(555443)
    #info = parseProg("http://ch.gomtv.com/427/28099/393618")
    #for item in info['playlist']:
    #    print item['title'] + " : " + item['nodeid']

# vim:sts=4:et
