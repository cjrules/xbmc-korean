import urllib
import re
from BeautifulSoup import BeautifulSoup

def parse_search_result(page_url):
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    result = []
    for node in soup.findAll('h3', {'class':'posttitle posttitle-search'}):
        a_node = node.a
        result.append({'title':a_node.text, 'path':a_node['href']})
    return result

def extract_from_url(page_url):
    from xml.dom.minidom import parseString
    html = urllib.urlopen(page_url).read()
    vid_title = re.search('<meta property="og:title" content="([^"]*)"/>', html).group(1)
    new_url = re.search('flashvars="config=(.*?)"', html).group(1)
    xml = urllib.urlopen(new_url).read()
    dom = parseString(xml)
    protocol = dom.getElementsByTagName('type')[0].childNodes[0].data
    if protocol == 'rtmp':
    	return {'title':vid_title,
		'type':'rtmp',
    	        'app':'vod',
    	        'flashVer':'WIN 11,6,602,180',
    	        'swfUrl':'http://hentai.animestigma.com/player.swf',
    	        'tcUrl':dom.getElementsByTagName('streamer')[0].childNodes[0].data,
    	        'pageUrl':page_url,
    	        'play':'mp4:'+dom.getElementsByTagName('file')[0].childNodes[0].data,
                }
    elif protocol == 'video':
    	return {'title':vid_title, 'type':'mp4', 'path':dom.getElementsByTagName('file')[0].childNodes[0].data}
    return None

if __name__ == "__main__":
    print parse_search_result("http://hentai.animestigma.com/?s=Bible+Black&x=0&y=0")
    print extract_from_url("http://hentai.animestigma.com/bible-black-origins-episode-1/")
