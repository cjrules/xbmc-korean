# -*- coding: utf-8 -*-
"""
    ondemandkorea.com
"""
import urllib
import re
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as etree

root_url = "http://www.ondemandkorea.com"

def parseTop():
    html = urllib.urlopen(root_url).read()
    soup = BeautifulSoup(html)
    items = []
    for node in soup.find('span', {'class':'menu'}).findAll(lambda tag: tag.name=='a' and tag['href'].endswith('html')):
    	items.append(node['href'])
    return items

def parseGenrePage(page_url):
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    # soup.findAll('div', {'class':'genreSub'})
    items = []
    for node in soup.findAll('div', {'class':'ep_box'}):
    	items.append({'title':node.b.string, 'url':root_url+'/'+node.a['href'], 'thumbnail':node.img['src']})
    return items

def parseEpisodePage(page_url):
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    # soup.findAll('div', {'class':'genreSub'})
    result = {'episode':[]}
    for node in soup.findAll('div', {'class':re.compile('^(?:ep|ep_last)$')}):
    	title = node.b.string.replace('&amp;','&')
    	bdate = node.b.findNextSibling(text=True).string.split(':',1)[1].strip()
    	result['episode'].append({'title':title, 'broad_date':bdate, 'url':root_url+node.a['href'], 'thumbnail':node.img['src']})
    pgnav = soup.find('div', {'id':'pg'})
    if pgnav:
    	curpg = pgnav.find('a', {'class':'current'})
    	prevpg = curpg.findPreviousSibling('a')
    	if prevpg:
    	    result['prevpage'] = root_url+'/'+prevpg['href']
    	nextpg = curpg.findNextSibling('a')
    	if nextpg:
    	    result['nextpage'] = root_url+'/'+nextpg['href']
    return result

def extractStreamUrl(page_url):
    # loadPlayer()
    html = urllib.urlopen(page_url).read()
    vid_title = re.compile('<div id="title">(.*?)</div>', re.S).search(html).group(1).strip()
    info_url = root_url + re.compile('"(/includes/playlist.php\?token=\d+\|[^"]*)').search(html).group(1)
    print info_url
    xml = urllib.urlopen(info_url).read()
    root_node = etree.fromstring(xml)
    tcUrl = root_node.find('.//meta').attrib['base']
    app = tcUrl.rsplit('/',1)[1]
    videos = dict()
    paras = {'app':app, 'tcUrl':tcUrl}
    for item in root_node.findall('.//video'):
    	videos[ item.attrib['system-bitrate'] ] = {'tcUrl':tcUrl, 'app':app, 'playpath':item.attrib['src']}
    return {'title':vid_title, 'bitrate':videos}

if __name__ == "__main__":
    #print parseGenrePage( root_url+"/variety" )
    #print parseEpisodePage( root_url+"/infinite-challenge-e324.html" )
    print extractStreamUrl( root_url+"/infinite-challenge-e324.html" )

# vim:sw=4:sts=4:et
