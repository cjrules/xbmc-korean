# -*- coding: utf-8 -*-
"""
  FLV from various URL
"""
import urllib2
import re

import sys
__settings__ = sys.modules[ "__main__" ].__settings__
youtube_fmt = {"270p":18, "360p":34, "480p":35, "720p":22}

class GetFLV:
  @staticmethod
  def flv(url):
    if url.find('tudou')>0:
      req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+url)
      response=urllib2.urlopen(req);link=response.read();response.close()
      match=re.search('<a href\s*=\s*"(.+?)" target="_blank" ', link)
      if match:
        flv=match.group(1).replace('&amp;','&')
        flv=flv.replace('?1','?8')        #trick to enable on-the-fly streaming
        return [flv]
      return []
    elif url.find('56.com')>0:
      if url.find('vid=')<0:
        #obtain redirected url
        req = urllib2.Request(url)
        response=urllib2.urlopen(req);url=response.geturl();response.close()
      req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+url)
      response=urllib2.urlopen(req);link=response.read();response.close()
      match=re.search('<a href\s*=\s*"(.+?)" target="_blank" ', link)
      if match:
        #obtain redirected url
        req = urllib2.Request(match.group(1))
        response=urllib2.urlopen(req);re_url=response.geturl();response.close()
        return [re_url]
      return []
    elif url.find('youku')>0:
      req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+url)
      response=urllib2.urlopen(req);link=response.read();response.close()
      return re.compile('<a href\s*=\s*"(.+?)" target="_blank" ').findall(link)
    elif url.find('veoh')>0:
      #match=re.search(r'http://www.veoh.com/videos/(.+)',url)
      match=re.search('permalinkId=(\w+)&',url)
      req = urllib2.Request('http://www.veoh.com/rest/videos/'+match.group(1)+'/details')
      response=urllib2.urlopen(req);link=response.read();response.close()

      #preview has 5min play time limitation
      veoh=re.search('fullPreviewHashPath="(.+?)"',link).group(1)
      thumb=re.search('fullHighResImagePath="(.+?)"',link).group(1)
      if veoh.find("content.veoh.com")>0:
        #obtain redirected url
        req = urllib2.Request(veoh)
        response=urllib2.urlopen(req);re_url=response.geturl();response.close()
        return [re_url]
      return [veoh]
    elif url.find('youtube')>0:
      id = re.search('http://www.youtube.com/watch\?v=(.+)',url)
      if id is None:
        id = re.search('http://www.youtube.com/v/(.+)',url)
        url = "http://www.youtube.com/watch?v=%s"%id.group(1)
      print "youtube ID: "+id.group(1)
      req = urllib2.Request(url)
      response=urllib2.urlopen(req);link=response.read();response.close()
      key = re.search('&t=(.+?)&',link)
      if key:
        url = "http://www.youtube.com/get_video.php?video_id="+id.group(1)+"&t="+key.group(1)
        fmt = __settings__.getSetting('YouTubeFmt')
        return [ url+"&fmt=%d"%youtube_fmt[ fmt ] ]
      return []
    elif url.find('4shared')>0:
      req = urllib2.Request(url)
      response=urllib2.urlopen(req);re_url=response.geturl();response.close()
      query = re.compile("streamer=(.*?)&").search(re_url)
      if match:
        return [match.group(1)]
      return []
    elif url.find('dailymotion')>0:
      id = re.search('http://www.dailymotion.com/.*?/(.*)',url).group(1)
      print "dailymotion ID: "+id

      req = urllib2.Request("http://www.dailymotion.com/video/"+id)
      response=urllib2.urlopen(req);link=response.read();response.close()
      match=re.search('''addVariable\("video", "(.*?)"\);''', link)
      if match:
        print "dailymotion wrapper: "+match.group(1)
        #obtain redirected url
        req = urllib2.Request(match.group(1))
        response=urllib2.urlopen(req);re_url=response.geturl();response.close()
        return [re_url]
      return []
    #not supported format
    return []

  @staticmethod
  def img(url):
    if url.find('tudou')>=0:
      return "http://www.video-download-capture.com/wp-content/uploads/2010/01/tudou_logo.jpg"
    elif url.find('56.com')>=0:
      return "http://mallow.wakcdn.com/avatars/000/060/094/normal.png"
    elif url.find('youku')>=0:
      return "http://static.youku.com/v1.0.0541/index/img/youkulogo.gif"
    elif url.find('veoh')>=0:
      return "http://ll-appserver.veoh.com/images/veoh.gif"
    elif url.find('youtube')>=0:
      #return "http://s.ytimg.com/yt/img/logos/youtube_logo_standard_againstwhite-vfl95119.png"
      return "http://s.ytimg.com/yt/img/logos/youtube_logo_standard_againstblack-vfl95119.png"
    elif url.find('4shared')>=0:
      return "http://userlogos.org/files/logos/veinedstorm/4shared.png"
    elif url.find('dailymotion')>=0:
      return "http://www.iconspedia.com/uploads/1687271053.png"
    else:
      return ''
# vim: softtabstop=2 shiftwidth=2 expandtab
