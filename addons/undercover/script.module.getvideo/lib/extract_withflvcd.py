# -*- coding: utf-8 -*-
"""
  Extract Video with FLVCD.com
"""
import urllib, urllib2, re

UserAgentStr = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"

def extract_withFLVCD(main_url):
  vid_list = []

  url = "http://www.flvcd.com/parse.php?kw="+main_url
  req = urllib2.Request(url)
  req.add_header("User-Agent", UserAgentStr)
  doc = urllib2.urlopen(req).read().decode('gb2312','ignore')

  try:
    title = re.compile(' name="name" value="(.*?)"').search(doc).group(1)
  except:
    title = ""
  query = re.compile(' name="inf" value="(.*?)"',re.S).search(doc)
  if query:
    ptcnt = 1
    for url in re.compile('(\S+)').findall(query.group(1)):
      vid_list.append( {"title":u"%s - %d" %(title,ptcnt), "url":url} )
      ptcnt += 1
  else:
    try:
      url = re.compile('clipurl *= *"(.*?)"').search(doc).group(1)
      vid_list.append( {"title":title, "url":url.replace('&amp;','&')} )
    except:
      pass
  return vid_list

if __name__ == "__main__":
  print extract_withFLVCD("http://www.tudou.com/programs/view/ubrrVcYGweA/")
  print extract_withFLVCD("http://v.youku.com/v_show/id_cc00XNzQ3ODcyMA==.html")
  print extract_withFLVCD("http://my.tv.sohu.com/u/vw/1882940")

# vim:sts=2:sw=2:et
