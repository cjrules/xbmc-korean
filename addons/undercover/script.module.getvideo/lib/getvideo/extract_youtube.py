# -*- coding: utf-8 -*-
"""
  Youtube
      13: 176x144
      17: 176x144
      36: 320x240
       5: 400\\327226
      34: 480x360 FLV (360p)
       6: 640\\327360 FLV
      35: 854\\327480 HD (480p)
      18: 480x360 MP4 (270p)
      22: 1280x720 MP4 (720p)
      37: 1920x1080 MP4 (1080p)
      38: 4096\\3272304 Epic MP4
      43: 4096\\3272304 WebM
      44: 4096\\3272304 WebM
      45: 4096\\3272304 WebM
"""
import urllib, urlparse, re

PTN_ID = re.compile("(?:watch\?v=|/embed/)(?P<id>[^&/]*)")

# refer plugin.video.youtube/YouTubePlayer/scrapeWebPageForVideoLinks
def extract_video(vid):
  url = "http://www.youtube.com/watch?v=%s&fmt=18" % vid

  html = urllib.urlopen(url).read()
  html = html.replace('\\u0026', '&')
  query = re.compile('"url_encoded_fmt_stream_map":\s*"(.+?)"').search(html)
  if query is None:
    raise FormatError

  vid_urls = {}
  for url_desc in query.group(1).split(','):
    url_desc_map = urlparse.parse_qs(url_desc)
    #print u"url_map: " + repr(url_desc_map)
    if not (url_desc_map.has_key(u"url") and url_desc_map.has_key(u"itag")):
      continue
    url = urllib.unquote(url_desc_map[u"url"][0])
    if url_desc_map.has_key(u"sig"):
      url += u"&signature=" + urllib.unquote(url_desc_map[u"sig"][0])
    itag = int(url_desc_map[u"itag"][0])
    vid_urls[itag] = url

  return vid_urls

def extract_video_from_url(url):
  vid = PTN_ID.search(url).group('id')
  return extract_video(vid)

if __name__ == "__main__":
  urls = extract_video('UslqIyPZsic')
  if urls.has_key(18):
    print urls[18]

# vim:sts=2:sw=2:et
