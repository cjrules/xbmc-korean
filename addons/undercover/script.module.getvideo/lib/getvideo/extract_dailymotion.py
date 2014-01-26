# -*- coding: utf-8 -*-
# DailyMotion
import urllib, re

PTN_ID = re.compile("dailymotion.com/.*?/(.*)")

def extract_id(url):
  try:
    return PTN_ID.search(url).group(1)
  except:
    return None

def extract_video(vid):
  jstr = urllib.urlopen("http://www.dailymotion.com/sequence/"+vid).read()
  vid_info = {'image':[], 'hd':[], 'sd':[]}
  if not '"statusCode":410' in jstr and not '"statusCode":403' in jstr:
    #vid_info['hd'] = [urllib.unquote_plus(url) for url in re.compile('"hd1080URL":"(.+?)"', re.DOTALL).findall(jstr)]
    #vid_info['hd'] = [urllib.unquote_plus(url) for url in re.compile('"hd720URL":"(.+?)"', re.DOTALL).findall(jstr)]
    vid_info['hd'] = [urllib.unquote_plus(url) for url in re.compile('"hqURL":"(.+?)"', re.DOTALL).findall(jstr)]
    vid_info['sd'] = [urllib.unquote_plus(url) for url in re.compile('"sdURL":"(.+?)"', re.DOTALL).findall(jstr)]
    if not vid_info['sd']:
      vid_info['sd'] = [urllib.unquote_plus(url) for url in re.compile('"video_url":"(.+?)"', re.DOTALL).findall(jstr)]
    vid_info['image'] = [urllib.unquote_plus(url.replace('\\/','/')) for url in re.compile('"videoPreviewURL":"(.+?)"', re.DOTALL).findall(jstr)]
  return vid_info

def extract_video_from_url(url):
  vid = extract_id(url)
  return extract_video(vid)

if __name__=="__main__":
  #print extract_video("xyt3vl")
  #print extract_video("k73kkqGIaOfz2w3YEVU")
  #print extract_video("x11kxil")
  print extract_video_from_url("http://www.dailymotion.com/embed/video/k7scJiabg1V2RW51fGo")

# vim:sts=2:sw=2:et
