# -*- coding: utf-8 -*-
"""
  m.gomtv.com
"""
import urllib, urllib2
import cookielib
import re
from random import randrange
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as etree

BrowserAgent = "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) Mobile"
cookie_jar = None

root_url = "http://m.gomtv.com"

def setCookieFile(fpath):
    import os
    global cookie_jar
    cookie_jar = cookielib.LWPCookieJar(fpath)
    if os.path.isfile(fpath):
        cookie_jar.load(ignore_discard=True, ignore_expires=True)

def login(userid, password):
    global cookie_jar
    if cookie_jar is None:
    	return False
    # prepare login form
    import hashlib
    m = hashlib.md5()
    m.update(password)
    paras = {'userid':userid,
             'passwd':m.hexdigest(),
             'passwdtmp':'',
             'savedIdCheck':'1',
             'from':'m',
             'adultcheck':'Y',
             'adult':'2',
             'returl':root_url+'/'
            }
    referer = "http://private.gomtv.com/login/loginMobile.gom?adult=2&returl="+urllib.quote(paras['returl'])
    # login and save cookie
    opener = setCookieOpener()
    opener.addheaders = [('User-Agent', BrowserAgent), ('Referer', referer)]
    f = opener.open('https://private.gomtv.com/gomtv20/member/loginProcess.gom', urllib.urlencode(paras))
    print f.geturl()
    login_status = f.geturl() == paras['returl']
    f.close()
    for cj in cookie_jar:
    	print cj
    cookie_jar.save(ignore_discard=True, ignore_expires=True)
    return login_status

def parseMenu(main_url):
    vid_info = {'tab':[], 'subtab':[]}

    opener = setCookieOpener()
    html = opener.open(main_url).read()
    if html.startswith('<script>'):
    	return None     # redirected to login page
    soup = BeautifulSoup(html)

    # tab menu
    for node in soup.find("nav", {"class":re.compile("^top_menu")}).findAll('a'):
        vid_info['tab'].append( {'title':node.string, 'url':root_url+node['href']} )
    # subtab menu
    ptn_para = re.compile("'listtype'\s*:\s*'([^']*)'[^}]*'listseq'\s*:\s*'([^']*)'")
    for node in soup.find("ul", {"class":"list_tab"}).findAll('a'):
        cmd = node['onclick']
        service, listseq = ptn_para.search(cmd).group(1,2)
        vid_info['subtab'].append( {'title':node.string, 'service':service, 'listseq':listseq} )
    return vid_info

# http://m.gomtv.com/js/m.js?<date>
def parseList(service, listseq, offset, limit):
    page_url = root_url + "/ajaxInclude.gom?lib=gomclass&src=%2FindexList.gom&offset={0:d}&limit={1:d}&listseq={2:s}&service={3:s}".format(offset, limit, listseq, service)
    req = urllib2.Request(page_url)
    req.add_header('User-Agent', BrowserAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, fromEncoding='UTF-8')
    items = []
    for node in soup.findChildren('a'):
        items.append( {'title':node.span.string, 'url':root_url+node['href'], 'thumbnail':node.img['src']} )
    return items

def parseProg(main_url, proxy=None):
    opener = setCookieOpener()
    resp = opener.open(main_url)
    if 'loginMobile' in resp.geturl():
    	#raise LoginRequired
    	return None

    html = resp.read()
    btns = BeautifulSoup(html).findAll('dd', {'class':'btn'})
    if not btns:
    	#raise UnknownFormat
    	return None
    soup = btns[-1]
    ptn_play = re.compile("setPlayVideo\('([^']*)'\)")
    result = {'link':[]}
    for item in soup.findAll('a', {'onclick':ptn_play}):
    	arg = ptn_play.search(item['onclick']).group(1)
        result['link'].append( getPlayUrl(arg, main_url, proxy) )
    return result

def setCookieOpener():
    global cookie_jar
    ck_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(ck_handler)
    opener.addheaders = [('User-Agent', BrowserAgent)]
    return opener

def getPlayUrl(arg, referer, proxy=None):
    global cookie_jar
    ck_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    if proxy:
        px_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(px_handler, ck_handler)
    else:
        opener = urllib2.build_opener(ck_handler)

    down_url = root_url+"/ajax/getPlayUrl.gom"
    opener.addheaders = [("User-Agent", BrowserAgent),
                         ("Referer", referer),
                         ("Accept", "text/html")]
    paras = '&authmodel=ipad&systemversion=6&arg=%s&rand=%d' %(urllib.quote(arg), randrange(0, 1000))
    print paras
    xml = opener.open(down_url, paras).read()
    markup = etree.fromstring(xml)
    title = markup.find('.//TITLE').text
    vid_url = markup.find('.//REF').attrib['href']
    return {'title':title, 'url':vid_url}

if __name__ == "__main__":
    proxy = "http://175.209.211.180:8888/"
    ### regular contents
    """
    print parseMenu(root_url)
    print parseList('game', '142', 0, 25)
    info = parseProg(root_url+"/view.gom?contentsid=3013576&service=game", proxy=proxy)
    print "%s %s" % (info['contentsid'], info['seriesid'])
    print info['title'] + " : " + info['url']
    """
    # adult contents
    setCookieFile('temp.txt')
    print login('test', 'temp')
    print parseMenu(root_url+"/?service=adult")
    #info = parseProg(root_url+"/view.gom?contentsid=19961&service=movie", proxy=proxy)
    #print "%s %s" % (info['contentsid'], info['seriesid'])

# vim:sts=4:et
