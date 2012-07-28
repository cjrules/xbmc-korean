# -*- coding: utf-8 -*-
"""
  Tudou
"""
import urllib
import xml.dom.minidom
from extract_withflvcd import extract_withFLVCD
from random import randint

def extract_video(vid):
  return extract_video_from_url("http://www.tudou.com/programs/view/"+vid)

def extract_video_from_url(main_url):
  result = extract_withFLVCD(main_url)
  for i in range(len(result)):
    result[i]['url'] = result[i]['url'].replace("&amp;","&")
    result[i]['url'] = result[i]['url'].replace("?1","?8")  # trick to make streaming easier
  return result

def extract_video_from_iid(iid):
  values = {
    "st" : "2",
    "vn" : "02",
    "si" : "11000",
    "sid": "10000",
    'it' : iid,
  }
  url = "http://v2.tudou.com/v.action?"+urllib.urlencode(values)
  doc = urllib.urlopen(url).read()
  dom = xml.dom.minidom.parseString(doc)
  items = dom.getElementsByTagName('f')
  url = items[ randint(0,len(items)-1) ].firstChild.nodeValue.replace('&amp;','&')
  url = url.replace("f4v?", "f4v?80000&")
  return [{'title':'','url':url}]

def revert_icode(iid):
  values = {
    'it' : iid,
    "hd" : "1",
    "mt" : "0",
  }
  url = "http://v2.tudou.com/v.action?"+urllib.urlencode(values)
  doc = urllib.urlopen(url).read()
  dom = xml.dom.minidom.parseString(doc)
  return dom.getElementsByTagName('v')[0].getAttribute('code')

if __name__ == "__main__":
  print extract_video("ubrrVcYGweA")
  print extract_video_from_iid("31252809")
  #print revert_icode("31252809")

# vim:sts=2:sw=2:et
