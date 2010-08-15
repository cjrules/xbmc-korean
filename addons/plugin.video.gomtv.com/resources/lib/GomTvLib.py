# -*- coding: utf-8 -*-
"""
  GomTV - Parse GomTV pages
"""

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

txheaders = {
  'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
  'Cookie' : 'ptic=bfcbf4b805bc63344e200391d95069c7; GomVersion=5027; HQPlusVersion=0006'
}    # full Cookie support is not required

gom_errors = {
  "1000" : "영상 재생에 문제가 발생했습니다. 잠시 후 다시 이용해 주세요.",
  "1001" : "영상 재생에 문제가 발생했습니다.",
  "1010" : "선택하신 화질의 영상은 현재 서비스 되고 있지 않습니다.",
  "1020" : "해당 영상은 대한민국 내에서만 시청하실 수 있습니다.",
  "1030" : "19세 미만은 본 영상을 시청하실 수 없습니다.",
  "1040" : "결제?",
  "1041" : "결제 해야되서 로그인",
  "1050" : "해당 영상을 재생하는데 일시적인 오류가 발생하였습니다. 잠시 후 다시 이용 부탁드립니다.",
  "1051" : "해당 영상은 현재 서비스 일시 중단한 영상입니다.",
  "1060" : "영상 재생에 문제가 발생했습니다. - parameter error - ",
  "1070" : "결제 필요",
  "1071" : "패키지 구매가 필요한 영상입니다.",
  "1080" : "보다 좋은 서비스를 위해 현재 시스템을 점검중에 있습니다. \n이용에 불편을 드려 죄송합니다.",
  "1500" : "해당 생중계는 현재 방송중이 아닙니다.",
  "1510" : "사용량 초과.",
  "1520" : "해당 생중계는 현재 방송중이 아닙니다.\n(이미 해당 생중계를 보고 있습니다.)",
  "1700" : "해당 영상에 시청 권한이 없습니다."
}
  
class GomTvLib:
  hq_first = False
  chid = 0
  pid = 0
  bid = 0
  sub_list = []
  dispid = 0
  vodid = 0
  mis_id = 0
  liveid = 0
  live_level = 0
  req_ip = "147.46.100.100"        # any IP in Korea

  def GomTvLib(self):
    import random
    self.req_ip = "147.46.%d.%d" % (random.randint(0,255), random.randint(1,255))

  def useHQFirst(self,value):
    self.hq_first = value

  def GetVideoUrl(self,main_url):
    txhdr = txheaders
    txhdr['User-Agent'] = 'HttpGetFile'
    req = urllib2.Request(main_url, None, txhdr)
    try: resp=urllib2.urlopen(req)
    except: return None
      
    soup = BeautifulSoup( resp.read(), fromEncoding="euc-kr" )
    list = soup.findAll('ref')
    for ref in list:
      url = ref['href']
      if url[7:url.find('.',7)].isdigit():
        return url.replace('&amp;','&')
      elif url.startswith('goms://'):
        print "Unsupported format: "+url
    return ''

  def GetMovieUrls(self,dispid,vodid):
    req_url = 'http://movie.gomtv.com/common/ajax/getGoxUrlToJson.gom'
    param_templ = ['param=', 'dsi=null', 'onlyIE=n',
                   'uip=%s', 'dispid=%s', 'vodid=%s',
                   'part=1', 'level=2',
                   'isMultiPlay=false', 'isPlay=true',
                   'async=false', 'serv=100', 'adult=F',
                   'isweb=1', 'isnav=1', 'navurl=', 'source=',
                   'os=Windows', 'browser=MSIE8.0',
                   '&property=movie']

    txdenc = '|||||'.join(param_templ) % (self.req_ip, dispid, vodid)

    req = urllib2.Request(req_url, txdenc, txheaders)
    urls = []
    try:
      resp = urllib2.urlopen(req)
      data = resp.read()
      code = re.compile('"error":"?(\d+)').search(data).group(1)
      if code == "0":
        titles = re.compile('"title":\[(.*)\],"url"').search(data).group(1)[1:-1].split('","')
        urls = re.compile('"url":\[(.*)\],"error"').search(data).group(1)[1:-1].replace("\\/","/").split('","')
      else:
        print gom_errors[code]
      resp.close
    except IOError, e:
      print "ERROR with movie (ajax)"
      if hasattr(e,'code'):
        print "Failed with code - %s" % e.code
    mov_urls = []
    for i in range(0,len(urls)):
      mov_urls.append( (titles[i].decode("unicode_escape"), urls[i]) )
    return mov_urls

  def ParseMoviePage(self,main_url):
    (self.misid, self.dispid, self.vodid) = (0,0,0)
    req = urllib2.Request(main_url, None, txheaders)
    try: tDoc=urllib2.urlopen(req).read()
    except: return
    query = re.compile("http://movie.gomtv.com/sub/detailAjax.\gom\?misid=(\d+)&dispid=(\d+)&vodid=(\d+)&mtype=5").search(tDoc)
    if query:
      (self.misid, self.dispid, self.vodid) = query.group(1,2,3)

  def GetHotclipIds(self):
    if self.dispid==0: return []
    hotclip_url = "http://movie.gomtv.com/sub/detailAjax.gom?misid=%s&dispid=%s&vodid=%s&mtype=5" % (self.misid,self.dispid,self.vodid)
    req = urllib2.Request(hotclip_url, None, txheaders)
    try: tDoc=urllib2.urlopen(req).read()
    except: return []

    soup = BeautifulSoup( tDoc, fromEncoding="euc-kr" )
    out_list = []
    strain = SoupStrainer('div', {"class" : "widgetMinMax"})
    sec = soup.find(strain)
    if sec is None: return []
    for item in sec.findAll("dl", {"class" : "list_join_small2"}):
      ta = item.find('dd', {"class":"title"}).find('a')
      clipid = re.compile("clipid:'(\d+)'").search( ta['onclick'] ).group(1)
      title = ta.string.replace('&quot;','"')
      thumb = item.find('img', {"class":"thum"})['src']
      out_list.append( (clipid,title,thumb) )
    return out_list

  def ParseChVideoPage(self,main_url):
    req = urllib2.Request(main_url, None, txheaders)
    try: tDoc=urllib2.urlopen(req).read()
    except: return None

    #-- chid/pid/bid & default bjvid
    query = re.compile('obj\.useNoneImg(.*?)if\(isFirst\)',re.S).search(tDoc)
    if query is None:
      print "%s is not compatible" % main_url
      return None
    self.chid,self.pid,bjvid,self.bid = re.compile("'(\d+)'").findall(query.group(1))

    #-- check playlist table
    self.sub_list = []
    soup = BeautifulSoup( tDoc, fromEncoding="euc-kr" )
    if self.hq_first:
      plist = soup.find("ul", {"id" : "widgetTabs1"})   # HQ first
      if plist is None:
        plist = soup.find("ul", {"id" : "widgetTabs2"})
    else:
      plist = soup.find("ul", {"id" : "widgetTabs2"})   # Std first
      if plist is None:
        plist = soup.find("ul", {"id" : "widgetTabs1"})
    if plist:
      #-- bjvid from table
      for item in plist.findAll('a'):
        ref = item['href']
        id = ref[ref.rfind('(')+1:ref.rfind(',')]
        title = item['title']
        title = title[:title.find('\n')]
        self.sub_list.append( (id, title) )
    else:
      #-- bjvid for single
      match = re.compile('this\.arr(?:High|Low)Bjoinv\s*=\s*\[(\d+)\];').findall(tDoc)
      if len(match) == 2:
        if self.hq_first: bjvid = match[0]
        else:             bjvid = match[1]
      self.sub_list.append( (bjvid,"PLAY") )    # single video

  def GetLiveUrl(self,main_url):
    txhdr = txheaders
    txhdr['User-Agent'] = 'HttpGetFile'
    req = urllib2.Request(main_url, None, txhdr)
    try: resp=urllib2.urlopen(req)
    except: return None
      
    soup = BeautifulSoup( resp.read(), fromEncoding="euc-kr" )
    list = soup.findAll('ref')
    for ref in list:
      url = ref['href']
      if url.startswith('gomp2p://'):
        url2 = url[ url.rfind("&quot;http")+6 : url.rfind("&quot;") ]
        return url2.replace("&amp;","&")
    return ''

  def ParseLivePage(self,main_url):
    req = urllib2.Request(main_url, None, txheaders)
    try: tDoc=urllib2.urlopen(req).read()
    except: return None

    query = re.compile('var typeObj(.*?)}\s*}',re.S).search(tDoc)
    if query is None:
      print "%s is not compatible" % main_url
      return None
    grpid,self.liveid,self.live_level = re.compile("'(\d+)'").findall(query.group(1))

if __name__ == "__main__":
  gom = GomTvLib()
  # hotclip parse
  gom.misid = '42929'
  gom.dispid = '23850'
  gom.vodid = '0'
  print gom.GetHotclipIds()
  # unsupported movie page
  print gom.GetMovieUrls('11099','34678')
  # unsupported video format
  for title,url in gom.GetMovieUrls('17917','19822'):
    print "%s: %s" % (title,url)
    print gom.GetVideoUrl(url)
# vim: softtabstop=2 shiftwidth=2 expandtab
