import urllib
import re

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    vartbl = {}
    for key, val in re.compile("so.addVariable\('([^']*)','([^']*)'\);").findall(html):
    	vartbl[key] = val
    title = re.search('<h2 class="titles">(.*?)</h2>', html).group(1).decode('utf-8')
    return {'title':title, 'url':vartbl['file'], 'thumbnail':vartbl['image']}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://toukoucity.to/video/YGADvN5597/')
