import urllib
import urlparse
import re

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    vid_title = re.search("<title>([^|]*)", html).group(1).strip()
    qstr = re.search('"flashvars",\s*"(.*?)"', html).group(1)
    qq = urlparse.parse_qs(qstr)
    #vid_url = qq['flv_h264_url'][0]
    vid_url = qq['mp4_url'][0]
    #vid_url = qq['mp4_url'][0]+qq['hash_mp4'][0]
    return {'title':vid_title, 'url':vid_url}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://www.redtube.com/287973')
