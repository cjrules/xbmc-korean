# -*- coding: utf-8 -*-
import urllib
import re
from BeautifulSoup import BeautifulSoup

root_url = "http://1qdisk.com"

# /vod/list.html?cate=
def parseList(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = {}
    # main body
    link = []
    for item in soup.findAll("div",{"class":"main_ztnr1"}):
        thumb = root_url + item.find('img')['src']
    	aa = item.find("div", {"class":"main_ztnr_right1"}).a
        title = aa.string.strip()
        url = root_url + aa['href']
        link.append( {'title':title,'url':url,'thumb':thumb} )
    result['link'] = link
    # page navigation
    sec = soup.find("div",{"class":"pagination"})
    prevpg = sec.find(text=u"이전")
    if prevpg:
        result['prevpage'] = root_url + prevpg.parent.get('href')
    nextpg = sec.find(text=u"다음")
    if nextpg:
        result['nextpage'] = root_url + nextpg.parent.get('href')
    return result

# /vod/view.html?idx=
def parseProg(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    playptn = re.compile(r"player\w*\('(.*?)','(\d+)'")
    sohu_idptn = re.compile("id=(\d+)")
    tudou_idptn = re.compile("/v/(\w*)")
    tudou_idptn2 = re.compile("iid=(\d*)")
    result = []
    for item in soup.find("table",{"id":"video_list"}).tbody.findChildren("tr")[1:]:
    	title = item.find("td",{"class":"vod_list"}).span.string
    	vsrc = []
        for aa in item.findAll(name=re.compile("(img|a)")):
            playcmd = aa.get('onclick')
            if playcmd is None:
            	continue
            match = playptn.search(playcmd)
            if match is None:
            	continue
            url = urllib.unquote( match.group(1) )
            # pretty formatting
            if url.find('sohu.com') >= 0:
                vid = sohu_idptn.search(url).group(1)
                vsrc.append( "http://my.tv.sohu.com/u/vw/"+vid )
            elif url.find('tudou.com') >= 0:
                match = tudou_idptn.search(url)
                if match:
                    vid = tudou_idptn.search(url).group(1)
                else:
                    iid = tudou_idptn2.search(url).group(1)
                    from extract_tudou import revert_icode
                    vid = revert_icode(iid)
                vsrc.append( "http://www.tudou.com/programs/view/"+vid )
            elif url.find('youku.com') >= 0:
                vsrc.append( url )
            else:
                print "Unknown format, "+url
        result.append( {'title':title,'list':vsrc} )
    return result

if __name__ == "__main__":
    result = parseList(root_url+"/vod/list.html?cate1=100000")
    print len(result['link'])
    print result['nextpage']
    result = parseProg(root_url+"/vod/view.html?idx=7126")
    print result[0]['title'].encode('utf-8')
    print len(result[0]['list'])

# vim:sw=4:sts=4:et
