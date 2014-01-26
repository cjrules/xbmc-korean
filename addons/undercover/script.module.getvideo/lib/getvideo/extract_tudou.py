# -*- coding: utf-8 -*-
"""
  Extract Video with Tudou
"""
import urllib2
import re
import json

from extract_withflvcd import UserAgentStr

PTN_TITLE = re.compile(",kw: *'(.*?)'")
PTN_THUMB = re.compile(",pic: *'(.*?)'")
PTN_SEGS  = re.compile(",segs: *'(.*?)'")

def extract_video(vid):
  return extract_video_from_url("http://www.tudou.com/programs/view/"+vid)

def extract_video_from_url(main_url):
  req = urllib2.Request(main_url)
  req.add_header('User-Agent', UserAgentStr)
  doc = urllib2.urlopen(req).read().decode('utf-8')
  title = PTN_TITLE.search(doc).group(1)
  jstr = PTN_SEGS.search(doc).group(1)
  data = json.loads(jstr)

  if '2' in data:
    quality = '2'
  else:
    quality = data.keys()[0]
  print "quality: "+quality

  vid_list = list()
  for part in data[quality]:
    part_id = part['k']
    part_no = int(part['no'])
    vid_title = u"%s - %d" % (title, part_no+1)
    vid_url = _url_for_id(part_id, part['pt'])
    vid_list.append({'title':vid_title, 'url':vid_url, 'useragent':UserAgentStr})
  return vid_list

def _url_for_id(iid, quality=None):
  info_url = "http://v2.tudou.com/f?id="+str(iid)
  if quality:
    info_url += "&hd" + str(quality)
  req = urllib2.Request(info_url)
  req.add_header('User-Agent', UserAgentStr)
  xml = urllib2.urlopen(req).read()
  vid_url = re.compile('>(.+?)</f>').search(xml).group(1)
  return vid_url.replace('&amp;','&')

if __name__ == "__main__":
  print extract_video("9uC6orp2AEQ")

# vim:sts=2:sw=2:et
