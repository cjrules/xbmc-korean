# -*- coding: utf-8 -*-
"""
    JoonMedia - Korea Drama/TV Shows Streaming Service
"""
import re
from BeautifulSoup import BeautifulSoup

def parseProgList(html):
    result = []
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    for item in soup.findAll("div", { "class" : "column" } ):
        ref = item.find('a')
        tlist = []
        for s in ref.contents:
            if s.string: tlist.append( s.string )
        title = " / ".join( tlist )
        url = ref['href']
        log( u"TV program: %s" % title )

        thumb = item.find('img')['src']
        if thumb.endswith("/utils/icons/"):
            thumb = ""    # fix site bug

        result.append({'title':title, 'id':url.rsplit('/')[-1], 'thumb':thumb})
    return result

def parseRecentList(html):
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    cols = []
    for colnum, item in enumerate(soup.findAll( "div", { "class" : "column" } )):
        category = item.find('h2').contents[0]
        log(u"%s: %d" % (category, colnum))
        result = []
        for ref in item.findAll('a'):
            if str(ref.contents[0]).startswith('<strong>'):
                continue    # skip
            tlist = []
            for s in ref.contents:
                if s.string: tlist.append( s.string )
            title = " / ".join( tlist )
            url = ref['href']
            log( "TV program: %s" % title.encode('utf-8') )

            result.append({'title': title, 'id':url.rsplit('/')[-1]})

        cols.append(result)
    return cols

def parseEpisodeList(html, colsel=2):
    result = []

    soup = BeautifulSoup( html )
    cols = soup("div", {"class" : "column"})
    thumb = cols[0].find('img')['src']
    for episode in cols[colsel-1].findAll('li'):
        title = u""
        for node in episode.contents:
            if node.string:
                title += node.string
            if getattr(node, 'name', None) == 'br':
                break
        title = title.strip()

        for ref in episode.findAll('a'):
            url = ref['href']
            suppl = ''.join(ref.findAll(text=True)).strip()
            title2 = u"{0:s} ({1:s})".format(title,suppl)
            log( u"Found page: %s" % title2 )

            ids = url.rsplit('/', 2)
            result.append({'title':title2, 'id':ids[-2], 'server':ids[-1]})

    return result

def extract_video_link(html):
    return re.compile('<a class="player_link" href="([^"]*)"').findall(html.decode('string-escape'))

def log(msg):
    #print msg.encode('utf-8')
    pass

#-----------------------------------                
if __name__ == "__main__":
    import urllib
    base_url = 'http://joonmedia3.com'
    print parseProgList( urllib.urlopen(base_url+'/vids/list/drama').read() )
    print parseRecentList( urllib.urlopen(base_url+'/').read() )
    print parseEpisodeList( urllib.urlopen(base_url+'/series/718').read() )
    print extract_video_link( urllib.urlopen(base_url+'/vids/play/29577/dmotion1').read() )

# vim:sts=4:sw=4:et
