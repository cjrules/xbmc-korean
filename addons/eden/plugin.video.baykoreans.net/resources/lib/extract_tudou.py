# -*- coding: utf-8 -*-
"""
  Tudou
"""
import urllib
import xml.dom.minidom

def revert_icode(iid):
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
  return dom.getElementsByTagName('v')[0].getAttribute('code')

# vim:sts=2:sw=2:et
