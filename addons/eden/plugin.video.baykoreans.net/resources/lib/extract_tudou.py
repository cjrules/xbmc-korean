# -*- coding: utf-8 -*-
"""
  Tudou
"""
import urllib, re
import xml.dom.minidom
from random import randint

def extract_video(iid):
  values = {
    'it' : iid,
    "hd" : "1",
    "mt" : "0",
  }
  url = "http://v2.tudou.com/v.action?"+urllib.urlencode(values)
  hdl = urllib.urlopen(url)
  doc = hdl.read()
  hdl.close()
  dom = xml.dom.minidom.parseString(doc)
  icode = dom.getElementsByTagName('v')[0].getAttribute('code')

  url = "http://www.flvcd.com/parse.php?kw=http://www.tudou.com/programs/view/{0:s}/".format(icode)
  hdl = urllib.urlopen(url)
  doc = hdl.read().decode('gb2312')
  hdl.close()
  vid_url = re.search('<a href\s*=\s*"(http://\d.+?)" target="_blank"', doc).group(1)
  vid_url = urllib.unquote(vid_url)

  return vid_url

# vim:sts=2:sw=2:et
