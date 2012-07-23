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
import urllib, re

def extract_video(vid):
  url = "http://www.youtube.com/watch?v=%s&fmt=18" % vid

  html = urllib.urlopen(url).read()
  html = html.replace('\\u0026', '&')
  match = re.compile('url_encoded_fmt_stream_map=(.+?)&').findall(html)
  if len(match) == 0:
    stream_map = (re.compile('url_encoded_fmt_stream_map": "(.+?)"').findall(html)[0]).replace('\\/', '/').split('url=')
  else:
    stream_map = urllib.unquote(match[0]).decode('utf8').split('url=')

  if re.search('status=fail', html):
    return None

  vid_urls = {}
  for attr in stream_map:
    if attr == '':
        continue
    parts = urllib.unquote(attr).decode('utf8').split('&qual')
    qual = int(re.compile('&itag=(\d*)').findall(parts[1])[0])
    vid_urls[qual] = parts[0]

  return vid_urls

if __name__ == "__main__":
  urls = extract_video('UslqIyPZsic')
  if urls.has_key(18):
    print urls[18]

# vim:sts=2:sw=2:et
