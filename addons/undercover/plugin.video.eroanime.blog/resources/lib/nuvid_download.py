import urllib, urllib2
import re

def extract_from_url(page_url):
    return extract_from_mobile(page_url)

def extract_from_mobile(page_url):
    new_url = page_url.replace('//www.', '//m.')
    html = urllib2.urlopen(new_url).read()
    vid_title = re.search('<p class="name2">([^<]*)</p>', html).group(1)
    wrap_url = "http://m.nuvid.com" + re.search('href="([^"]*)"[^>]*data-link_type="mp4"', html).group(1)
    html = urllib2.urlopen(wrap_url).read()
    vid_url = re.search('<p class="name2 download"><a href="([^"]*)"', html).group(1)
    return {'title':vid_title, 'url':vid_url}

def extract_from_flash(page_url):
    iid = re.search('/(\d+)[/$]', page_url).group(1)
    new_url = "http://www.nuvid.com/embed/"+iid
    req = urllib2.Request(new_url)
    req.add_header('Referer', page_url)
    html = urllib2.urlopen(req).read()
    cfg_url = "http://www.nuvid.com" + urllib.unquote(re.search('name="FlashVars" value="embed=1&config=(.*?)"', html).group(1))
    # pkey is needed
    print cfg_url
    req = urllib2.Request(cfg_url)
    req.add_header('Referer', new_url)
    print urllib2.urlopen(req).read()
    return None

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url("http://www.nuvid.com/video/22660/koihime-01-sub-espanol")
