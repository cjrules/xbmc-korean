# -*- coding: utf-8 -*-
import urllib
import re
from BeautifulSoup import BeautifulSoup
from extract_tudou import revert_icode

root_url = "http://www.133133.com"

# /ucc/list.php?cate1=
def parseList(main_url):
    base_url = root_url+"/ucc/"
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = {}
    # main body
    link = []
    for item in soup.find("ul",{"class":"ucc-list"}).findAll("li"):
    	aa = item.div.h4.a
        title = aa.string
        url = base_url + aa['href']
        thumb = base_url + item.find('img')['src']
        link.append( {'title':title,'url':url,'thumb':thumb} )
    result['link'] = link
    # page navigation
    sec = soup.find("div",{"class":"page"})
    prevpg = sec.find(text=lambda(x) : x == u"이전")
    if prevpg:
        result['prevpage'] = prevpg.parent.get('href')
    nextpg = sec.find(text=lambda(x) : x == u"다음")
    if nextpg:
        result['nextpage'] = nextpg.parent.get('href')
    return result

# /ucc/new_list.php
def parseNewList(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    result = []
    # main body
    link = []
    sec = soup.table.findChildren("tr")[1].td.findChildren("tr")
    ssname = [item.strong.string for item in sec[0].findAll("td")]
    subsec = sec[1].findAll("td")
    for i in range(len(subsec)):
        plist = []
        for aa in subsec[i].findAll("a"):
            plist.append( (aa.string, root_url+"/ucc/"+aa['href']) )
        result.append( {'name':ssname[i], 'list':plist} )
    return result

# /ucc/view.php?id=
def parseProg(main_url):
    resp = urllib.urlopen(main_url)
    html = resp.read()
    resp.close()
    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    playptn = re.compile("new_play_(\d)\('(.+?)',(\d+)\)")
    allnum_ptn = re.compile("^\d+$")
    sohu_idptn = re.compile("id=(\d+)")
    tudou_idptn = re.compile("/v/(\w*)")
    youku_idptn = re.compile("/([^/]*)/v.swf")
    result = []
    for item in soup.find("ul",{"class":"menu-item"}).findAll("li"):
    	title = item.find(text=True).strip()
    	vsrc = []
        for aa in item.findAll("a"):
            tt, url = playptn.search(aa['href']).group(1,2)
            if tt == '1':
                if allnum_ptn.match(url):
                    #icode = int(url)+133122
                    #vsrc.append( "http://www.tudou.com/programs/view/"+revert_icode(str(icode)) )
                    pass
                else:
                    vsrc.append( "http://v.youku.com/v_show/id_"+url )
            elif tt == '2':
                # pretty formatting
                if url.find('sohu.com') >= 0:
                    vid = sohu_idptn.search(url).group(1)
                    vsrc.append( "http://my.tv.sohu.com/u/vw/"+vid )
                elif url.find('tudou.com') >= 0:
                    vid = tudou_idptn.search(url).group(1)
                    vsrc.append( "http://www.tudou.com/programs/view/"+vid )
                elif url.find('youku.com') >= 0:
                    vid = youku_idptn.search(url).group(1)
                    vsrc.append( "http://v.youku.com/v_show/id_"+vid )
                elif url.find('yinyuetai.com') >= 0:
                    vid = re.search('videoId=(\d+)', url).group(1)
                    vsrc.append( "http://www.yinyuetai.com/video/"+vid )
                else:
                    print "Unknown format, "+aa['href']
            else:
                print "Unknown script, "+aa['href']
        result.append( {'title':title,'list':vsrc} )
    return result

if __name__ == "__main__":
    result = parseNewList(root_url+"/ucc/new_list.php")
    print len(result)
    result = parseList(root_url+"/ucc/list.php?cate1=오락프로")
    print len(result['link'])
    print result['nextpage']
    result = parseProg(root_url+"/ucc/view.php?id=2044")
    print result[0]['title'].encode('utf-8')
    print len(result[0]['list'])

# vim:sw=4:sts=4:et
