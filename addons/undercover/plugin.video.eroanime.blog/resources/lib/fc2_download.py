from hashlib import md5
import urllib, urllib2
import cookielib
from urlparse import parse_qs
from BeautifulSoup import BeautifulSoup

UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.9"

def parse_search_result(page_url):
    req = urllib2.Request(page_url)
    req.add_header('User-Agent', UserAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    result = []
    for node in soup.findAll('div', {'class':'video_list_thumb'}):
    	a_node = node.find('a')
    	thumb = a_node.find('img')['src']
    	if a_node.has_key('title'):
	    result.append({'title':a_node['title'], 'path':a_node['href'], 'thumbnail':thumb})
    return result

# refer github.com/binzume/fc2-video-downloader
def extract_from_url(page_url):
    # get cookie
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    r = opener.open(page_url)
    r.read()
    ck_list = []
    for index, cookie in enumerate(cj):
	ck_list.append(cookie.name+"="+cookie.value)
    ck_str = '; '.join(ck_list)

    # upid from url
    if page_url[-1] == '/':
	upid = page_url.rsplit('/',2)[1]
    else:
	upid = page_url.rsplit('/',1)[1]

    # internal info
    m = md5()
    m.update(upid+'_gGddgPfeaf_gzyr')
    mimi = m.hexdigest()
    refer = "http://video.fc2.com/en/a/content/%s/" %upid
    url = "http://video.fc2.com/ginfo.php?mimi={1:s}&href={2:s}&v={0:s}&fversion=WIN%2011%2C6%2C602%2C180&from=2&otag=0&upid={0:s}&tk=null&".format(upid, mimi, urllib.quote(refer, safe='').replace('.','%2E'))
    try:
	req = urllib2.Request(url)
	req.add_header('User-Agent', UserAgent)
	qstr = urllib2.urlopen(req).read()
	ll = parse_qs(qstr)
	print ll['title'][0]
	return {'title':ll['title'][0], 'url':ll['filepath'][0]+'?mid='+ll['mid'][0], 'cookie':ck_str}
    except:
	return None

# Read command line arguments.
if __name__ == "__main__":
    print parse_search_result('http://video.fc2.com/a/movie_search.php?keyword=%E3%81%9D%E3%82%89%E3%81%AE%E3%81%84%E3%82%8D%E3%80%81%E3%81%BF%E3%81%9A%E3%81%AE%E3%81%84%E3%82%8D&sobj_keyword=%E3%81%9D%E3%82%89%E3%81%AE%E3%81%84%E3%82%8D%E3%80%81%E3%81%BF%E3%81%9A%E3%81%AE%E3%81%84%E3%82%8D&m=scont')
    print extract_from_url('http://video.fc2.com/a/content/20130319dfpT4Pqp/')
