# -*- coding: utf-8 -*-
"""
  gomtv.com
"""

import urllib2
import re
from BeautifulSoup import BeautifulSoup

# 무료영화: /video/cate.gom?seq=8&subseq=30
# 무료드라마: /video/cate.gom?seq=6&subseq=42
# 무료연예오락: /video/cate.gom?seq=7&subseq=50
# 뮤직/전체/종합: /video/cate.gom?seq=12&subseq=12&attr=-1
# 뮤직/전체/가요: /video/cate.gom?seq=12&subseq=12&attr=4039
# 게임,스포츠: /video/cate.gom?seq=13
# /view.gom?contentsid=<contentsid>

root_url = "http://www.gomtv.com"

def parseSubCateList(cate):
    page_url = root_url + "/video/cate.gom?seq=%d" %cate
    html = urllib2.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    items = []
    ptn_subcate = re.compile("title:'([^']*)',url:'[^']*subseq=(\d+)'")
    for node in soup.find('ul', {'class':'cate_smenu'}).findAll('a'):
    	title, subcate = ptn_subcate.search(node['onclick']).group(1,2)
    	items.append({'title':title, 'subcate':int(subcate)})
    return items

def parseBoard(cate, subcate, page):
    page_url = root_url + "/video/cate.gom?seq=%d&subseq=%d&page=%d&isseries=0" %(cate, subcate, page)
    html = urllib2.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    result = {'video':[]}
    ptn_contentsid = re.compile("contentsid=(\d+)")
    for node in soup.findAll('dl', {'class':'dl_type_join2'}):
    	a_node = node.find('a')
    	title = a_node.img['alt']
    	thumb = a_node.img['src']
    	contentsid = int(ptn_contentsid.search(a_node['href']).group(1))
    	result['video'].append({'title':title, 'contentsid':contentsid, 'thumbnail':thumb})
    # page navigation
    curpg = soup.find('div', {'class':re.compile('^page_index')}).find('a', {'class':'on'})
    if curpg:
        prevpg = curpg.findPreviousSibling('a')
        if prevpg:
            result['prevpage'] = int(prevpg['href'])
        nextpg = curpg.findNextSibling('a')
        if nextpg:
            result['nextpage'] = int(nextpg['href'])
    return result

if __name__ == "__main__":
    #print parseSubCateList(13)
    print parseBoard(13, 61, 2)

# vim:sts=4:et
