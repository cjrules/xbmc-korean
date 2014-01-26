# -*- coding: utf-8 -*-
"""
  Sohu
"""
import urllib
import json
import re

PTN_ID = re.compile("tv\.sohu\.com/.*?/(?P<id>\d+)\.shtml")
# ID to URL: http://my.tv.sohu.com/u/vw/<id>

def _fetch_data(vid):
  url = "http://my.tv.sohu.com/play/videonew.do?vid="+str(vid)
  jstr = urllib.urlopen(url).read()
  return json.loads(jstr)

def extract_video(vid):
  data = _fetch_data(vid)

  title = data['data']['tvName']

  vid_list = []
  # quality: nor < high < super < ori
  vid_id = data['data']['norVid']

  if vid_id != vid:
    data = _fetch_data(vid_id)

  part_count = data['data']['totalBlocks']
  allot = data['allot']
  prot = data['prot']
  clipsURL = data['data']['clipsURL']
  su = data['data']['su']

  vid_list = []
  for i in range(part_count):
    part_url = "http://%s/?prot=%s&file=%s&new=%s" % (allot, prot, clipsURL[i], su[i])
    doc = urllib.urlopen(part_url).read()
    part_info = doc.split('|')
    vid_url = "%s%s?key=%s" % (part_info[0], su[i], part_info[3])
    vid_list.append({'title':title, 'url':vid_url})

  return vid_list

def extract_video_from_url(url):
  vid = PTN_ID.search(url).group('id')
  return extract_video(vid)

if __name__=="__main__":
  print extract_video("63960984")

# vim:sts=2:sw=2:et
