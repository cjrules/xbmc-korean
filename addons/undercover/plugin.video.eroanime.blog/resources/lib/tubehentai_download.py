import urllib
import re

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    emb_url = re.search('<div class="video-wrap"><iframe[^>]*src="([^"]*)"', html).group(1)
    html = urllib.urlopen(emb_url).read()
    vid_title = re.search('<title>(.*?)</title>', html).group(1)
    for key, val in re.compile("var (hq_video_file|normal_video_file|preview_img) = '([^']*)';").findall(html):
    	if key == 'hq_video_file':
    	    vid_url = val
	elif key == 'preview_img':
    	    vid_thumb = val
    return {'title':vid_title, 'url':vid_url, 'thumbnail':vid_thumb}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url("http://www.tubehentai.me/harem-time-the-animation-episode-1/")
