# -*- coding: utf-8 -*-
"""
  Sohu
"""
import urllib, re
from extract_withflvcd import extract_withFLVCD

def extract_video(vid):
  return extract_video_from_url("http://my.tv.sohu.com/u/vw/"+vid)

def extract_video_from_url(main_url):
  vid_list = extract_withFLVCD(main_url)

  for vid in vid_list:
    url = vid['url']
    newpath = url[ url.rfind('&new=')+5 : ]

    resp = urllib.urlopen(url.replace('itc.cn','itc.cn/?prot=2&file='))
    link = resp.read()
    resp.close()
    fields = link.split('|')
    url = fields[0].rstrip('/') + newpath + '?key=' + fields[3]
    vid['url'] = url  # overwrite

  return vid_list

# vim:sts=2:sw=2:et
