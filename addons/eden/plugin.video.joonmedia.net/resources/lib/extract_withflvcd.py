# -*- coding: utf-8 -*-
"""
  Extract Video with FLVCD.com
"""
import urllib, re

def extract_withFLVCD(main_url):
  vid_list = []

  url = "http://www.flvcd.com/parse.php?kw="+main_url
  hdl = urllib.urlopen(url)
  doc = hdl.read().decode('gb2312')
  hdl.close()

  match = re.compile('<input[^>]*name="inf" value="(.*?)">', re.S).search(doc)
  if not match:
    return []
  for item in match.group(1).split('<$>'):
    try:
      title = re.compile(r"<N>(.*)", re.U).search(item).group(1).encode('utf-8')
      url = re.compile(r"<U>(.*)").search(item).group(1)
      vid_list.append( {"title":title, "url":url} )
    except:
      pass
  return vid_list

if __name__ == "__main__":
  print extract_withFLVCD("http://v.youku.com/v_show/id_cc00XNzQ3ODcyMA==.html")

# vim:sts=2:sw=2:et
