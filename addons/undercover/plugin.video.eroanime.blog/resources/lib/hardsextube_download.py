import urllib

def extract_from_url(page_url):
    return extract_from_mobile(page_url.replace('//www.', '//m.'))

def extract_from_mobile(page_url):
    from BeautifulSoup import BeautifulSoup
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    vid_title = soup.find('h2').text
    a_node = soup.find('div', {'id':'playVideoBtnWrap'}).find('a')
    vid_url = a_node['href']
    vid_thumb = a_node.find('img')['src']
    return {'title':vid_title, 'url':vid_url, 'thumbnail':vid_thumb}

def extract_from_flash_page(page_url):
    import re
    import base64

    html = urllib.urlopen(page_url).read()
    vid_title = re.search('<h1[^>]*>([^<]*)</h1>', html).group(1)
    jstr = re.compile('var flashvars\s*=\s*{(.*?)};', re.S).search(html).group(1)
    vtbl = dict()
    for key, val in re.compile('^\s*(.*?):\s"(.*?)",\s*$', re.M).findall(jstr):
    	vtbl[key] = val
    print vtbl['flv']
    vid_url = base64.b64decode(vtbl['flv'])
    vid_thumb = vtbl['startimg']
    return {'title':vid_title, 'url':vid_url, 'thumbnail':vid_thumb}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://www.hardsextube.com/video/948208/')
