# -*- coding: utf-8 -*-
# DailyMotion
import urllib, re

def extract_id(url):
  try:
    return re.search('http://www.dailymotion.com/.*?/(.*)',url).group(1)
  except:
    return None

def extract_video(vid):
  resp = urllib.urlopen("http://www.dailymotion.com/video/"+vid)
  html = resp.read()
  resp.close()

  sequence = re.compile('"sequence",  "(.+?)"').findall(html)
  newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/', '/')

  vid_info = {}

  imgSrc = re.compile('og:image" content="(.+?)"').findall(html)
  if len(imgSrc) == 0:
      imgSrc = re.compile('/jpeg" href="(.+?)"').findall(html)
  vid_info['image'] = imgSrc

  vid_info['sd'] = re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
  vid_info['hd'] = re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
  return vid_info

if __name__=="__main__":
  print extract_video("xsb5oi")

# vim:sts=2:sw=2:et
