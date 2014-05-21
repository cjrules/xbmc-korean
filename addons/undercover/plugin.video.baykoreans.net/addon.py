# -*- coding: utf-8 -*-
"""
    BayKoreans
"""
from xbmcswift2 import Plugin
import urllib
import sys
from YDStreamExtractor import getVideoInfo

plugin = Plugin()
_L = plugin.get_string

plugin_path = plugin.addon.getAddonInfo('path')
lib_path = os.path.join(plugin_path, 'resources', 'lib')
sys.path.append(lib_path)

import baykoreans

tPrevPage = u"[B]<%s[/B]" % _L(30100)
tNextPage = u"[B]%s>[/B]" % _L(30101)

@plugin.route('/')
def main_menu():
    items = [
        {'label':u"방영 드라마", 'path':plugin.url_for("prog_list", cate='drama', page='-')},
        {'label':u"종영 드라마", 'path':plugin.url_for("prog_list", cate='drama_fin', page='-')},
        {'label':u"예능 | 오락", 'path':plugin.url_for("prog_list", cate='entertain', page='-')},
        {'label':u"시사 | 교양", 'path':plugin.url_for("prog_list", cate='current', page='-')},
        {'label':u"영화",        'path':plugin.url_for("prog_list", cate='movie', page='-')},
        {'label':u"애니 극장판", 'path':plugin.url_for("prog_list", cate='animation', page='-')},
        {'label':u"스포츠",      'path':plugin.url_for("prog_list", cate='sports', page='-')},
        {'label':u"뮤직비디오",  'path':plugin.url_for("prog_list", cate='music', page='-')},
    ]
    return items

@plugin.route('/category/<cate>/<page>/')
def prog_list(cate, page):
    pageN = 1 if page == '-' else int(page)
    url = baykoreans.ROOT_URL+'/index.php?mid=%s&page=%d' % (cate, pageN)
    if cate in ['movie', 'animation']:
        result = baykoreans.parseMovieList(url)
    else:
        result = baykoreans.parseProgList(url)
    items = [{'label':item['title'],
             'path':plugin.url_for('video_list', cate=item['cate'], eid=item['id']),
             'thumbnail':item['thumbnail'],
            } for item in result['link']]
    if 'prevpage' in result:
        items.append({'label':tPrevPage, 'path':plugin.url_for('prog_list', cate=cate, page=pageN-1)})
    if 'nextpage' in result:
        items.append({'label':tNextPage, 'path':plugin.url_for('prog_list', cate=cate, page=pageN+1)})
    morepage = True if page != '-' else False
    return plugin.finish(items, update_listing=morepage)

@plugin.route('/episode/<cate>/<eid>/')
def video_list(cate, eid):
    items = baykoreans.parseVideoList(baykoreans.ROOT_URL+'/'+cate+'/'+eid)
    return [{'label':item['title'],
             'path':plugin.url_for('play_video', url=item['url']),
            } for item in items]

@plugin.route('/play/<url>')
def play_video(url):
    # select first video
    print url
    plugin.log.debug(url)
    quality = plugin.get_setting('qualityPref', int)
    info = getVideoInfo(url, quality=quality)
    if info:
        plugin.log.debug("num of streams: %d" % len(info.streams()))
        # select quality
        from xbmcswift2 import xbmcgui
        stream = info.selectedStream()
        li = xbmcgui.ListItem(stream['title'], iconImage="DefaultVideo.png")
        li.setInfo('video', {"Title": stream['title']})
        xbmc.Player().play(stream['xbmc_url'], li)
    else:
        plugin.log.warning('Fail to extract')
    return plugin.finish(None, succeeded=False)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
