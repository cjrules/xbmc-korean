import urllib
import re
from BeautifulSoup import BeautifulSoup

def parse_search_result(page_url):
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    result = []
    for node in soup.findAll('div', {'class':re.compile('^post(?: last|)$')}):
        a_nodes = node.findAll('a')
        title = a_nodes[1].text
        url = a_nodes[0]['href']
        thumb = a_nodes[0].find('img')['src']
        result.append({'title':title, 'path':url, 'thumbnail':thumb})
    return result

def extract_from_url(page_url):
    from xml.dom.minidom import parseString

    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    vid_title = soup.find('div', {'class':'videotitle'}).text.replace('&#164;','')
    result = []
    for sec in soup.find('div', {'id':'tabs-1-1'}).findAll('script'):
    	jstr = re.search('var flashvars = {(.*?)};', sec.text).group(1)
    	jj = dict()
    	for key, val in re.compile('''(\w+):\s*["']([^"']*)["']''').findall(jstr):
    	    jj[key] = val
	xml = urllib.urlopen(jj['file']).read()
	dom = parseString(xml)
	vid_url = dom.getElementsByTagName('location')[0].childNodes[0].data
	#vid_thumb = jj['image']
	vid_thumb = dom.getElementsByTagName('image')[0].childNodes[0].data
	result.append({'title':vid_title, 'path':vid_url, 'thumbnail':vid_thumb})
    return result

if __name__ == "__main__":
    print parse_search_result("http://hentaistream.com/?s=Ane+Haramix")
    print extract_from_url("http://hentaistream.com/watch/ane-haramix-episode-04")
