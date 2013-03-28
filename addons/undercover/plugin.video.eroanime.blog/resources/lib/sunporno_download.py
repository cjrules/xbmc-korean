import urllib
import re

def extract_from_url(page_url):
    new_url = page_url.replace('www.','embeds.').replace('/videos/','/embed/')
    html = urllib.urlopen(new_url).read()
    vid_url, thumb = re.search('<video src="([^"]*)"[^>]*poster="([^"]*)"', html).group(1,2)
    return {'title':'Sunporno Video', 'url':vid_url, 'thumbnail':thumb}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://www.sunporno.com/videos/333902/')
