import urllib
import re

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    vid_title = re.search('<meta name="description" content="([^"]*)"\s*/?>', html).group(1)
    vid_url = urllib.unquote(re.search(",flv:\s*'([^']*)'", html).group(1))
    return {'title':vid_title, 'url':vid_url}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://www.slutload.com/watch/tVNE7qD58nD/BibleBlack-1-EroParadise-com-br.html')
