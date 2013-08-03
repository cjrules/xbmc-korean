# -*- coding: utf-8 -*-
"""
    tving Air
"""
from xbmcswift2 import Plugin
import urllib, urllib2
import simplejson
import xml.etree.ElementTree as etree

plugin = Plugin()
_L = plugin.get_string

tPrevPage = u"[B]<<%s[/B]" % _L(30100)
tNextPage = u"[B]%s>>[/B]" % _L(30101)
itemPerPage = 15

root_url = "http://www.tving.com"
api_root = "http://air.tving.com"
img_root = "http://image.tving.com"

@plugin.route('/')
def main_menu():
    items = [
        {'label':u'무료 방송다시보기', 'path':plugin.url_for('category_view', cate_cd='free')},
        {'label':u'무료 영화', 'path':plugin.url_for('movie_list', cate_cd='10', page_no='-')},
    ]
    return items

#--------------------------------------------------------------
# Channel
@plugin.route('/category/<cate_cd>/')
def category_view(cate_cd):
    url = root_url + "/vod/categoryAllChListA.do"
    values = {
    	"key"    :"CATE_CH00",
    	"deploy" :"0",
    	"cache"  :"N",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/vod/genre.do?cate_cd="+cate_cd)
    jstr = urllib2.urlopen(req, urllib.urlencode(values)).read()
    json = simplejson.loads(jstr)

    cate_tpl = u"[COLOR FFFF0000]%s[/COLOR]"
    items = [{'label':u"[B]전체[/B]", 'path':plugin.url_for('channel_view', cate_cd=cate_cd, ch_cd='-', offset='-')}]
    for item in json['RESULT_DATA']:
    	if len(item['CH_CD']) == 2:
            name = cate_tpl% item['CH_NM']
    	else:
            name = item['CH_NM']
        items.append({'label':name, 'path':plugin.url_for('channel_view', cate_cd=cate_cd, ch_cd=item['CH_CD'], offset='-')})
    return items

@plugin.route('/channel/<cate_cd>/<ch_cd>/<offset>')
def channel_view(cate_cd, ch_cd, offset):
    offset2 = 0 if offset=='-' else int(offset)
    if ch_cd=='-':
        ch_cd = ''
    start_num = offset2+1
    end_num = offset2+itemPerPage

    url = root_url + "/vod/vodListA.do"
    values = {
    	"key"    :"vodList",
    	"cate_cd":cate_cd,
    	"ch_cd"  :ch_cd,
    	"sort_type":"NEW",
    	"start_num":start_num,
    	"end_num":end_num,
    	"payfree_yn":"Y",
    	"initial_keyword":"",
    	"adult_yn":"N",
    	"deploy" :"0",
    	"cache"  :"N",
    	"package_id":"",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/vod/genre.do?cate_cd=free")
    jstr = urllib2.urlopen(req, urllib.urlencode(values)).read()
    json = simplejson.loads(jstr)

    items = []
    for item in json['RESULT_DATA']['RESULT_DATA']:
        #items.append({'label':item['PGM_NM'], 'path':plugin.url_for('play_vod', file_cd=str(item['DRM_VOD_FILE_CD'])), 'thumbnail':img_root+item['IMG_URL'], 'is_playable':True})
        items.append({'label':item['PGM_NM'], 'path':plugin.url_for('program_view', pgm_cd=str(item['PGM_CD']), offset='-'), 'thumbnail':img_root+item['IMG_URL']})
    # navigation
    if offset2 >= itemPerPage:
        new_offset = offset2 - itemPerPage
        items.append({'label':tPrevPage, 'path':plugin.url_for('channel_view', cate_cd=cate_cd, ch_cd=ch_cd, offset=new_offset)})
    if int(json['RESULT_DATA']['RESULT_COUNT']) == itemPerPage:
        new_offset = offset2 + itemPerPage
        items.append({'label':tNextPage, 'path':plugin.url_for('channel_view', cate_cd=cate_cd, ch_cd=ch_cd, offset=new_offset)})
    morepage = False if offset=='-' else True
    return plugin.finish(items, update_listing=morepage)

@plugin.route('/program/<pgm_cd>/<offset>')
def program_view(pgm_cd, offset):
    offset2 = 0 if offset=='-' else int(offset)
    start_num = offset2+1
    end_num = offset2+itemPerPage

    # /scripts/web/tving.vod.program.js -> episodePayfreeSearch('Y')
    url = root_url + "/vod/episodeListA.do"
    values = {
    	"key"   :"episodeListA",
    	"pgm_cd":pgm_cd,
    	"sort_type":"FREQUENCY_DESC",
    	"start_num":start_num,
    	"end_num":end_num,
    	"payfree_yn":"Y",
    	"adult_yn":"N",
    	"deploy" :"0",
    	"cache"  :"N",
    	"package_id":"",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/vod/program.do?pgm_cd="+pgm_cd)
    jstr = urllib2.urlopen(req, urllib.urlencode(values)).read()
    json = simplejson.loads(jstr)

    items = []
    for item in json['RESULT_DATA']['RESULT_DATA']:
        title = u"%s [%s]" %(item['EPI_NM'], item['BROAD_DT'])
        items.append({'label':title, 'path':plugin.url_for('play_vod', file_cd=(item['DRM_VOD_FILE_CD'])), 'thumbnail':img_root+item['IMG_URL'], 'is_playable':True})
    # navigation
    if offset2 >= itemPerPage:
        new_offset = offset2 - itemPerPage
        items.append({'label':tPrevPage, 'path':plugin.url_for('program_view', pgm_cd=pgm_cd, offset=new_offset)})
    if int(json['RESULT_DATA']['RESULT_COUNT']) >= itemPerPage:
        new_offset = offset2 + itemPerPage
        items.append({'label':tNextPage, 'path':plugin.url_for('program_view', pgm_cd=pgm_cd, offset=new_offset)})
    morepage = False if offset=='-' else True
    return plugin.finish(items, update_listing=morepage)

#--------------------------------------------------------------
# Movie
@plugin.route('/movie/<cate_cd>/<page_no>')
def movie_list(cate_cd, page_no):
    pgnum = 1 if page_no=='-' else int(page_no)
    url = root_url + "/sm/ms/SMMS401A.do"
    values = {
    	"CATE_CD":cate_cd,
    	"sortType":"NEW",
    	"pageNo":str(pgnum),
    	"grade":"ALL",
    	"runtime":"ALL",
    	"year":"ALL",
    }
    req = urllib2.Request(url)
    req.add_header('Referer', root_url+"/sm/ms/SMMS401Q.do?CATE_CD="+str(cate_cd))
    jstr = urllib2.urlopen(req, urllib.urlencode(values)).read()
    json = simplejson.loads(jstr)

    items = []
    for item in json['data']:
        items.append({'label':item['MAST_NM'], 'path':plugin.url_for('play_vod', file_cd=item['DRM_VOD_FILE_CD']), 'thumbnail':img_root+item['POSTER_IMG_URL'], 'is_playable':True})
    # navigation
    if pgnum > 1:
        new_pgnum = pgnum - 1
        items.append({'label':tPrevPage, 'path':plugin.url_for('movie_list', cate_cd=cate_cd, page_no=str(new_pgnum))})
    if len(json['data']) > 0:
        new_pgnum = pgnum + 1
        items.append({'label':tNextPage, 'path':plugin.url_for('movie_list', cate_cd=cate_cd, page_no=str(new_pgnum))})
    morepage = False if page_no=='-' else True
    return plugin.finish(items, update_listing=morepage)

# vodInfo/[TYPE]/[DRM_VOD_FILE_CD]/[PROTOCOL]?out=jsonp
#   TYPE: clip / vod
#   PROTOCOL: HLS / RTSP / HTTP
@plugin.route('/vod/<file_cd>')
def play_vod(file_cd):
    if plugin.get_setting('useProxy', bool):
    	proxy = plugin.get_setting('proxyServer', unicode)
    	print "Proxy="+proxy
        handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(handler)
    else:
        opener = urllib2.build_opener()

    url = root_url + "/sm/fh/FHViewControl.do?VOD_CD=%s&VIEW_GUBUN=VOD" %file_cd
    xml = opener.open(url).read().strip()
    root = etree.fromstring(xml)
    node = root.find('.//content_info')
    try:
        vid_title = node.find('./vod_nm').text
        #vid_url = node.find('./broad_url_org').text
        vid_url = node.find('./broad_url').text
        vid_thumb = "DefaultVideo.png"
    except:
        plugin.notify('login required')
        return plugin.finish(None, succeeded=False)
    if vid_url is None:
        xbmcgui.Dialog().ok(_L(30010), _L(30011))
        return plugin.finish(None, succeeded=False)
    plugin.set_resolved_url(vid_url)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
