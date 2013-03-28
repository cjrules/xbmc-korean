import urllib
import re

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    vtbl = dict()
    for key, val in re.compile('flashvars\.(video_title|video_url|image_url) = "([^"]*)";').findall(html):
    	vtbl[key] = val
    return {'title':vtbl['video_title'], 'url':urllib.unquote(vtbl['video_url']), 'thumbnail':vtbl['image_url']}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url("http://www.spankwire.com/aijou-kikan/video236824/")
