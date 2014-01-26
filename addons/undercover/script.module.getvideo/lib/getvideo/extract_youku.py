# -*- coding: utf-8 -*-
"""
  Extract Video with Youku
"""
import urllib
import json
import math
import re

PTN_ID = re.compile("youku\.com/v_show/id_([^\.]+)")

# copied from plugin.video.youku
class youkuDecoder:
    def __init__( self ):
        return

    def getFileIDMixString(self,seed):  
        mixed = []  
        source = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\:._-1234567890")  
        seed = float(seed)  
        for i in range(len(source)):  
            seed = (seed * 211 + 30031 ) % 65536  
            index = math.floor(seed /65536 *len(source))  
            mixed.append(source[int(index)])  
            source.remove(source[int(index)])  
        return mixed  

    def getFileId(self,fileId,seed):  
        mixed = self.getFileIDMixString(seed)  
        ids = fileId.split('*')  
        realId = []  
        for i in range(0,len(ids)-1):
            realId.append(mixed[int(ids[i])])  
        return ''.join(realId)

def extract_video(vid):
  url = "http://v.youku.com/player/getPlayList/VideoIDS/"+vid
  jstr = urllib.urlopen(url).read()
  data = json.loads(jstr)

  title = data['data'][0]['title']

  # flv < mp4 < hd2 < hd3
  typename = None
  if 'mp4' in data['data'][0]['streamtypes']:
    typename = 'mp4'
  else:
    typename = data['data'][0]['streamtypes'][0]

  seed = data['data'][0]['seed']
  stfId = data['data'][0]['streamfileids'][typename].encode('utf-8')
  fileId = youkuDecoder().getFileId(stfId, seed)
  vid_list = []
  for tt in data['data'][0]['segs'][typename]:
    k = tt['k'].encode('utf-8')
    num = int(tt['no'])
    url = 'http://f.youku.com/player/getFlvPath/sid/00_00/st/%s/fileid/%s%02X%s?K=%s' % (typename, fileId[:8], num, fileId[10:], k)
    vid_list.append({'title':title, 'url':url})
  return vid_list

def extract_video_from_url(url):
  vid = PTN_ID.search(url).group(1)
  return extract_video(vid)

if __name__ == "__main__":
  print extract_video("XNjY1ODE4NTI4")

# vim:sts=2:sw=2:et
