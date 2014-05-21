# -*- coding: utf-8 -*-
"""
    BayKoreans - Korea Drama/TV Shows Streaming Service
"""
import urllib2
import urlparse
import re
from BeautifulSoup import BeautifulSoup

ROOT_URL = 'http://baykoreans.net'
UserAgent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"

def parseProgList(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', UserAgent)
    resp = urllib2.urlopen(req)
    doc = resp.read()
    resp.close()
    soup = BeautifulSoup(doc, fromEncoding='utf-8')

    result = {'link':[]}
    for item in soup.findAll("td", {"class":"title"}):
        thumb = ""
        if item.div:
            thumb = item.div.img['src']
        if item.p.a:
            if not item.p.a.string:
                continue
            title = item.p.a.string.replace('&amp;','&').encode('utf-8')
            date,title = re.compile('^(\d*)\s*(.*)').search(title).group(1,2)
            if date:
                title = date + " " + title
            url = item.p.a['href']
            if 'index.php' in url:
                qs = urlparse.parse_qs(url.split('?')[1])
                cate = qs['mid'][0]
                id = qs['document_srl'][0]
            else:
                token = url.split('/')
                cate, id = token[-2:-1]
            result['link'].append({'title':title.decode('utf-8'), 'cate':cate, 'id':id, 'thumbnail':thumb})

    cur = soup.find("div", {"class":"pagination"}).find("strong")
    p = cur.findPreviousSibling("a")
    if not p.has_key("class"):
        url = ROOT_URL+p['href']
        result['prevpage'] = url
    p = cur.findNextSibling("a")
    if not p.has_key("class"):
        url = ROOT_URL+p['href']
        result['nextpage'] = url
    return result

def parseMovieList(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', UserAgent)
    resp = urllib2.urlopen(req)
    doc = resp.read()
    resp.close()
    soup = BeautifulSoup(doc, fromEncoding='utf-8')

    result = {'link':[]}
    for item in soup.findAll("div", {"class":"title"}):
        title = item.a.string.replace('&amp;','&').encode('utf-8')
        url = item.a['href']
        if 'index.php' in url:
            qs = urlparse.parse_qs(url.split('?')[1])
            cate = qs['mid'][0]
            id = qs['document_srl'][0]
        else:
            token = url.split('/')
            cate, id = token[-2:-1]

        thumb = item.findNextSibling("div", {"class":"thumb"}).find('img')['src']
        result['link'].append({'title':title.decode('utf-8'), 'cate':cate, 'id':id, 'thumbnail':thumb})

    cur = soup.find("div",{"class":"pagination"}).find("strong")
    p = cur.findPreviousSibling("a")
    if not p.has_key("class"):
        url = ROOT_URL+p['href']
        result['prevpage'] = url
    p = cur.findNextSibling("a")
    if not p.has_key("class"):
        url = ROOT_URL+p['href']
        result['nextpage'] = url
    return result

def parseVideoList(main_url):
    req = urllib2.Request(main_url)
    req.add_header('User-Agent', UserAgent)
    doc = urllib2.urlopen(req).read().decode('string-escape')
    doc = re.compile(r'<script language="javascript">document\.write\(unescape\("(.*?)"\)\);</script>', re.S).sub(r"\g<1>", doc)
    soup = BeautifulSoup(doc)
    result = []
    for item in soup.find('div', {'class':re.compile('^document')}).findAll('a'):
        url = item['href']
        title = item.span.string.split('|')[0].strip()

        if not url.startswith('http://'):
            url = ROOT_URL + url
        base_url = url[ : url.find('/',7)] 
        if url.find('/?xink=') > 0:
            xink = re.search('xink=(.*)', url).group(1)
            vid_url = None
            if '/dmotion/' in url:
                vid_url = "http://www.dailymotion.com/video/"+xink
            elif '/tudou.y/' in url:
                vid_url = "http://www.tudou.com/programs/view/"+xink
            elif '/sohu/' in url:
                vid_url = "http://my.tv.sohu.com/u/vw/"+xink
            else:
                print "Unsupported URL, "+url
            if vid_url:
                result.append({'title':title, 'url':vid_url})
        elif url.find('/?link=') > 0:
            req = urllib2.Request(url)
            req.add_header('User-Agent', UserAgent)
            doc = urllib2.urlopen(req).read()
            xink = re.search(r'\)\);</script>([^>]*)">', doc).group(1)
            vid_url = base_url+"/linkout/getfile/"+xink
            result.append({'title':title, 'url':vid_url})
        else:
            result.append({'title':title, 'url':url})
    return result

if __name__ == "__main__":
    print parseProgList(ROOT_URL+'/index.php?mid=entertain&page=1')
    print parseMovieList(ROOT_URL+'/index.php?mid=animation&page=1')
    print parseVideoList(ROOT_URL+'/index.php?mid=entertain&document_srl=2020832')

# vim:sts=4:sw=4:et
