# -*- coding: utf-8 -*-
# DailyMotion
import urllib, re
import simplejson

def extract_id(url):
  try:
    return re.search('http://www.dailymotion.com/.*?/(.*)',url).group(1)
  except:
    return None

def extract_video(vid):
  jstr = urllib.urlopen("http://www.dailymotion.com/sequence/"+vid).read()
  json = simplejson.loads(jstr)
  vid_info = {'image':[], 'hd':[], 'sd':[]}
  if not 'sequence' in json:
    return vid_info
  for node1 in json['sequence']:
    for node2 in node1['layerList'][0]['sequenceList']:
      #print '-'+node2['name']
      if node2['name'] == 'main':
        for node3 in node2['layerList']:
          #print '--'+node3['name']
          if node3['name'] != 'video':
            continue
          node4 = node3['param']
          #json['customURL']
          #json['hd1080URL']
          #json['hd720URL']
          if 'hqURL' in node4:
            vid_info['hd'].append( node4['hqURL'] )
          if 'sdURL' in node4:
            vid_info['sd'].append( node4['sdURL'] )
          #json['video_url']
      elif node2['name'] == 'reporting':
        for node3 in node2['layerList']:
          node4 = node3['param']['extraParams']
          vid_info['image'].append( node4['videoPreviewURL'] )
  return vid_info

if __name__=="__main__":
  #print extract_video("xyt3vl")
  print extract_video("k73kkqGIaOfz2w3YEVU")

# vim:sts=2:sw=2:et
