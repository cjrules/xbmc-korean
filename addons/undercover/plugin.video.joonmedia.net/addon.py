# -*- coding: utf-8 -*-
"""
    JoonMedia
"""
from xbmcswift2 import Plugin, xbmcgui
import urllib, urllib2
import sys
import os
from YDStreamExtractor import getVideoInfo

plugin = Plugin()
_L = plugin.get_string

plugin_path = plugin.addon.getAddonInfo('path')
lib_path = os.path.join(plugin_path, 'resources', 'lib')
sys.path.append(lib_path)

import joonmedia

BaseURL = urllib2.urlopen('http://joonmedia.net').geturl()

@plugin.route('/')
def main_menu():
    items = [
        {'label':u"[최근] 드라마",    'path':plugin.url_for("recent_list", col='0')},
        {'label':u"[최근] 시사/교양", 'path':plugin.url_for("recent_list", col='1')},
        {'label':u"[최근] 예능",      'path':plugin.url_for("recent_list", col='2')},
        {'label':u"[최근] 영화",      'path':plugin.url_for("recent_list", col='4')},
        {'label':u"드라마",     'path':plugin.url_for("prog_list", cate='drama', page='-')},
        {'label':u"종영드라마", 'path':plugin.url_for("prog_list", cate='cdrama', page='-')},
        {'label':u"예능",       'path':plugin.url_for("prog_list", cate='show', page='-')},
        {'label':u"시사교양",   'path':plugin.url_for("prog_list", cate='edu', page='-')},
        {'label':u"한국영화",   'path':plugin.url_for("prog_list", cate='krmovie', page='-')},
        {'label':u"일본영화",   'path':plugin.url_for("prog_list", cate='jpmovie', page='-')},
        {'label':u"중국영화",   'path':plugin.url_for("prog_list", cate='chmovie', page='-')},
    ]
    return items

@plugin.route('/recent/<col>/')
def recent_list(col):
    html = fetch_html('/')
    items = joonmedia.parseRecentList(html)
    return [{'label':item['title'], 'path':plugin.url_for('video_list', sid=item['id'])} for item in items[int(col)]]

@plugin.route('/list/<cate>/')
def prog_list(cate):
    html = fetch_html('/vids/list/'+cate)
    items = joonmedia.parseProgList(html)
    return [{'label':item['title'],
             'path':plugin.url_for('video_list', sid=item['id']),
             'thumbnail':item['thumb'],
            } for item in items]

@plugin.route('/series/<sid>/')
def video_list(sid):
    html = fetch_html('/series/'+sid)
    items = joonmedia.parseEpisodeList(html, colsel=plugin.get_setting('VideoColumn', int))
    return [{'label':item['title'],
             'path':plugin.url_for('play_video', eid=item['id'], server=item['server']),
             #'thumbnail':thumb_by_server(item['server']),
             #'is_playable':True,
            } for item in items]

@plugin.route('/play/<eid>/<server>/')
def play_video(eid, server):
    html = fetch_html('/vids/play/%s/%s' % (eid, server))
    urls = joonmedia.extract_video_link(html)
    if len(urls) > 0:
        # select first video
        plugin.log.debug(urls[0])
        quality = plugin.get_setting('qualityPref', int)
        info = getVideoInfo(urls[0], quality=quality)
        if info is None:
            plugin.log.warning('Fail to extract')
            return None
        plugin.log.debug("num of streams: %d" % len(info.streams()))
        # select quality
        stream = info.selectedStream()
        li = xbmcgui.ListItem(stream['title'], iconImage="DefaultVideo.png")
        li.setInfo('video', {"Title": stream['title']})
        xbmc.Player().play(stream['xbmc_url'], li)
    else:
        plugin.log.warning('Unsupported')
    return plugin.finish(None, succeeded=False)

def fetch_html(rel):
    url = BaseURL + rel
    proxy = None
    if plugin.get_setting('useProxy', bool):
        proxy = plugin.get_setting('proxyServer', str)
        plugin.log.debug("Proxy="+proxy)
    if proxy:
        px_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(px_handler)
        resp = opener.open(url)
    else:
        resp = urllib.urlopen(url)
    return resp.read()

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
