import urllib
import re
from BeautifulSoup import BeautifulSoup

def parse_series_page(page_url):
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.ALL_ENTITIES)
    result = {'episode':[]}
    for node in soup.find('div', {'class':'category-text'}).findAll('p'):
    	if node.strong:
    	    if "Title" in node.strong.text:
    	    	result['title'] = node.text.replace(node.strong.text,'')
    	else:
	    result['summary'] = urllib.unquote(node.text)
    for node in soup.find('div', {'id':'category-post'}).findAll('a'):
	result['episode'].append({'title':node.text, 'path':node['href']})
    return result

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    emb_url = re.compile('<iframe src="([^"]*)"').findall(html)[1]
    title = re.compile('<title>Watch\s+(.*?\S)\s+Online</title>').search(html).group(1)
    print emb_url
    html = urllib.urlopen(emb_url).read()
    vid_url = re.compile('clip:\s*{\s*url:\s*"([^"]*)",', re.S).search(html).group(1)
    return {'title':title, 'url':vid_url}

if __name__ == "__main__":
    print parse_series_page("http://www.hentaicrunch.com/hentai/watch/genmukan-2-shinshou-genmukan/")
    print extract_from_url("http://www.hentaicrunch.com/shinshou-genmukan-episode-1/")
