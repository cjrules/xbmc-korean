# -*- coding: utf-8 -*-
import urllib, urllib2
import cookielib
import os
import re

root_url = "http://dabdate.com"

BrowserAgent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)'
#BrowserAgent = 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0'
PlayerAgent  = 'Windows-Media-Player/12.0.7601.17514'

# http://dabdate.com
def parseTop( main_url, quality='1', localsrv='la'):
    result = {'video':[]}
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', BrowserAgent)
    psrc = urllib2.urlopen(req).read().decode('euc-kr')
    # item list
    items = re.split("<td colspan=\d+ height=\d+>", psrc)
    for item in items[:-1]:
        try:
            title = re.compile('''<a href[^>]*pr=[1|m]"><font [^>]*>(.*?)</font></a>''').search(item).group(1)
            title = re.compile("</?b>").sub("",title)
            if re.compile('<b>Free').search(item):
                title = "[B]"+title+"[/B]"
        except:
            continue

        img = ''
        match = re.compile('''<img src='([^']*)' ''').search(item)
        if match:
            img = match.group(1)

        vurl = None
        if quality == '1':
            match = re.compile("<a href='([^']*&pr={0:s}&local={1:s})'>".format(quality, localsrv)).search(item)
            if match:
                vurl = match.group(1)
        else:
            match = re.compile('<a href="([^"]*&pr={0:s})">'.format(quality)).search(item)
            if match:
                vurl = match.group(1)
        # fallback
        if vurl is None:
            #match = re.compile("<a href='([^']*&pr=1&local={0:s})'>".format(localsrv)).search(item)
            match = re.compile('<a href="([^"]*&pr=1)">').search(item)
            if match:
                vurl = match.group(1)
        if vurl is None:
            print "Video, {0:s}, doesn't exist on {1:s} server".format(title, quality)
        else:
            result['video'].append({'title':title, 'url':vurl, 'thumb':img})

    # navigation
    query = re.compile("<a href='([^']*)' class=navi>\[Prev\]</a>").search(psrc)
    if query:
        result['prevpage'] = query.group(1)
    query = re.compile("<a href='([^']*)' class=navi>\[Next\]</a>").search(psrc)
    if query:
        result['nextpage'] = query.group(1)
    return result

def getStreamUrl( main_url, userid='', passwd='', cookiefile='cookie.lwp'):
    # 1. load cookie
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    if os.path.isfile(cookiefile):
        cj.load(cookiefile)
        print "Cookie is loaded from "+cookiefile
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', BrowserAgent)
    resp = urllib2.urlopen(req)
    newurl = resp.geturl()
    # 2. login page
    if newurl.find('order.php') >= 0:
        resp.close()
        if userid == '' or passwd == '':
            raise LoginRequired(newurl)
        values = {
            'mode':'login',
            'url' :main_url,
            'id'  :userid,
            'pass':passwd
        }
        # login
        req = urllib2.Request( 'http://www.dabdate.com/login.php', urllib.urlencode(values) )
        req.add_header('User-Agent', BrowserAgent)
        req.add_header('Referer', newurl)
        resp = urllib2.urlopen(req)
        newurl = resp.geturl()
        cj.save(cookiefile)
        print "LOGIN to "+newurl
    # 3. accept payment
    if newurl.find('msg.php') >= 0:
        resp.close()
        values = {
            'mode':'auto',
            'mno' :'',
            'url' :main_url,
            'auto':'0'
        }
        req = urllib2.Request( 'http://www.dabdate.com/msg.php', urllib.urlencode(values) )
        req.add_header('User-Agent', BrowserAgent)
        req.add_header('Referer', newurl)
        resp = urllib2.urlopen(req)
        newurl = resp.geturl()
        cj.save(cookiefile)
        print "PAY to "+newurl
    # 4. video page
    psrc = resp.read().decode('euc-kr', 'ignore')
    resp.close()
    if not newurl.startswith(main_url):
        raise NotEnoughToken(newurl)
    if newurl.startswith("http://m.dabdate.com"):
        vurl = re.compile(r"location\.href\s*=\s*'([^']*)'").search( psrc ).group(1)
        vtitle = re.compile("<font class=big>(.*?)</font>", re.U).search( psrc ).group(1)
    else:
        vurl = re.compile("FileName='([^']*)'").search( psrc ).group(1)
        if not vurl.startswith("http://"):
            vurl = "http://dabdate.com/"+vurl
        vtitle = re.compile("<font class=big>(.*?)</font>", re.U).search( psrc ).group(1)
    cookies = []
    for cookie in cj:
        cookies.append( cookie.name+'='+cookie.value )
    ckStr = ';'.join(cookies)
    return {'title':vtitle, 'url':vurl, 'useragent':PlayerAgent, 'cookie':ckStr}

if __name__ == "__main__":
    #print parseTop( root_url )
    #print parseTop( root_url+"/index.php?page=2&lang=0" )
    print getStreamUrl( root_url+"/player.php?idx=29697&pr=1" )

# vim:sw=4:sts=4:et
