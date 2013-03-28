import urllib
from BeautifulSoup import BeautifulSoup
import re

def parse_search_result(page_url):
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    result = []
    for node in soup.find('div', {'class':'content itembox'}).findAll('div', {'class':'item'}):
    	a_node = node.find('a')
    	thumb = node.find('img')['src']
	result.append({'title':a_node.text, 'path':a_node['href'], 'thumbnail':thumb})
    return result

def extract_from_url(page_url):
    new_url = page_url.replace('/video/', '/embed/')
    html = urllib.urlopen(new_url).read()
    vartbl = {}
    for key, val in re.compile("so.addVariable\('([^']*)','([^']*)'\);").findall(html):
    	vartbl[key] = val
    title = re.search('<title>(.*?)</title>', html).group(1).decode('utf-8')
    return {'title':title, 'url':vartbl['file'], 'thumbnail':vartbl['image']}

# Read command line arguments.
if __name__ == "__main__":
    print parse_search_result('http://2anime.net/search/?keyword=%E5%AD%A6%E5%9C%92%EF%BC%92&x=0&y=0')
    print extract_from_url('http://2anime.net/video/xahA5LQUpx/')
