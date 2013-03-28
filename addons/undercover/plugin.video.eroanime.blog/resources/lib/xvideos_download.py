import urllib
import urlparse
import re

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    vid_title = re.search('<meta name="description" content="XVIDEOS\s*([^"]*\S)\s+free"\s*/?>', html).group(1)
    qstr = re.search('flashvars\s*=\s*"(.*?)"', html).group(1)
    qq = urlparse.parse_qs(qstr)
    return {'title':vid_title, 'url':qq['flv_url'][0], 'thumbnail':qq['url_bigthumb'][0]}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://www.xvideos.com/video3004304/family_of_debauchery')
