# http://www.pornhub.com/view_video.php?viewkey=1586570949
# var flashvars =
# json
#   video_title
#   image_url
#   encrypted=true
#   video_url -> base64 decode
import urllib
import re
import simplejson
import base64

def extract_from_url(page_url):
    html = urllib.urlopen(page_url).read()
    jstr = re.compile('var flashvars\s*=\s*({.*?});', re.S).search(html).group(1)
    json = simplejson.loads(jstr)
    vid_title = json['video_title']
    vid_thumb = urllib.unquote(json['image_url'])
    ### dont't know encryption method yet
    #vid_url = base64.b64decode(json['video_url'])
    ### via mobile page
    vkey = re.search('viewkey=(\d+)', page_url).group(1)
    m_url = "http://m.pornhub.com/video/show/title/"+vid_title+"/vkey/"+vkey
    html = urllib.urlopen(m_url).read()
    vid_url = re.search('href="([^"]*\.mp4[^"]*)"', html).group(1)
    return {'title':vid_title, 'url':vid_url, 'thumbnail':vid_thumb}

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://www.pornhub.com/view_video.php?viewkey=652793009#!')
