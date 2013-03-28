import urllib
import re
import simplejson

def extract_from_url(page_url):
    new_url = page_url.replace('videobam.com/', 'videobam.com/widget/')
    html = urllib.urlopen(new_url).read()
    vid_title = re.search('<title>(.*?)</title>', html).group(1)
    jstr = re.compile('var player_config = ({.*?});',re.S).search(html).group(1)
    json = simplejson.loads(jstr)
    vid_thumb = json['playlist'][0]['url']
    vid_url = json['playlist'][1]['url']
    return {'title':vid_title, 'url':vid_url, 'thumbnail':vid_thumb}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://videobam.com/TRWfc')
