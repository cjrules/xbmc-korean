# -*- coding: utf-8 -*-
"""
  Daum Brand
"""
import urllib
import simplejson
from BeautifulSoup import BeautifulSoup
import re

class DaumBrand:
  root_url = "http://tvpot.daum.net"
  page_size = 15
  menu_list = []
  video_list = []
  prevpage = None
  nextpage = None
  ownerid = None

  def DaumBrand(self, pgsz=15):
    self.page_size = pgsz

  def parseList(self, page=1):
    self.menu_list = []
    self.prevpage = None
    self.nextpage = None

    main_url = self.root_url+"/mypot/json/GetAllPotList.do?page=%d&size=%d"
    jstr = urllib.urlopen(main_url % (page, self.page_size)).read()

    obj = simplejson.loads(jstr)
    #-- item list
    for pot in obj['pot_list']:
      self.menu_list.append( (pot['name'], pot['ownerid'], pot['profile_img_url']) )
    #-- navigation
    if page != 1:
      self.prevpage = main_url % (page-1, self.page_size)
    if obj['has_more']:
      self.nextpage = main_url % (page+1, self.page_size)

  def parseTop(self,ownerid):
    self.menu_list = []
    self.prevpage = None
    self.nextpage = None

    #main_url = self.root_url+"/mypot/json/GetPlaylistList.do?ownerid=%s"
    main_url = self.root_url+"/mypot/Top.do?ownerid=%s"
    self.ownerid = ownerid
    html = urllib.urlopen(main_url % ownerid).read()

    soup = BeautifulSoup( html, fromEncoding="utf-8" )
    #-- item list
    sec = soup.find("span", {"class":re.compile("txt_program")}).parent.parent
    for item in sec.findAll('a'):
      if item['data-type']=='group':
        self.menu_list.append( (item.span.string.strip(), None, '') )
      elif item['data-type']=='playlist':
        self.menu_list.append( (item.string.strip(), int(item['data-id']), '') )

  def parse(self,ownerid,playlistid,page=1):
    self.video_list = []
    self.prevpage = None
    self.nextpage = None

    main_url = self.root_url+"/mypot/json/GetClipInfo.do?ownerid=%s&playlistid=%d&page=%d&size=%d"
    jstr = urllib.urlopen(main_url % (ownerid, playlistid, page, self.page_size)).read()

    obj = simplejson.loads(jstr)
    #-- item list
    for clip in obj['clip_list']:
      title = clip['title'].replace('&lt;','<').replace('&gt;','>')
      self.video_list.append( (title, clip['vid'], clip['thumb_url']) )
    #-- navigation
    if page != 1:
      self.prevpage = main_url % (ownerid, playlistid, page-1, self.page_size)
    if obj['has_more']:
      self.nextpage = main_url % (ownerid, playlistid, page+1, self.page_size)

if __name__ == "__main__":
  site = DaumBrand()
  site.parseList(1)
  print len(site.menu_list)
  print site.menu_list[0]
  print site.prevpage
  print site.nextpage

  site.parseTop("O_5rgf7M1do0")
  print len(site.menu_list)
  print site.menu_list[0]
  print site.prevpage
  print site.nextpage

  site.parse("O_5rgf7M1do0", 2199214, 1)
  print len(site.video_list)
  print site.video_list[0]
  print site.prevpage
  print site.nextpage
# vim: softtabstop=2 shiftwidth=2 expandtab
