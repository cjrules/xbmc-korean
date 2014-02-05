# -*- coding: utf-8 -*-
"""
    tving Air
"""
from xbmcswift2 import Plugin
import resources.lib.ondemandkorea as scraper

plugin = Plugin()
_L = plugin.get_string

tPrevPage = u"[B]<<%s[/B]" %_L(30100)
tNextPage = u"[B]%s>>[/B]" %_L(30101)

root_url = "http://www.ondemandkorea.com"
resolution2bitrate = [
    '196000',       # 180p
    '396000',       # 240p
    '796000',       # 300p
    '1196000',      # 360p
    '1596000',      # 480p
    '2296000',      # 720p
]

@plugin.route('/')
def main_menu():
    urls = scraper.parseTop()
    items = [
        {'label':u'드라마', 'path':plugin.url_for('genre_view', genre='drama')},
        {'label':u'버라이어티', 'path':plugin.url_for('genre_view', genre='variety')},
        #{'label':u'화제영상', 'path':plugin.url_for('gallery_view', cate='hot')},
        {'label':u'교육', 'path':plugin.url_for('episode_view', url=urls[1])},
        {'label':u'경제', 'path':plugin.url_for('genre_view', genre='economy')},
        {'label':u'종교', 'path':plugin.url_for('genre_view', genre='religion')},
        {'label':u'음악', 'path':plugin.url_for('genre_view', genre='kmuze')},
    ]
    return items

@plugin.route('/genre/<genre>/')
def genre_view(genre):
    url = root_url+'/'+genre
    plugin.log.debug(url)
    info = scraper.parseGenrePage(url)
    items = [{'label':item['title'], 'path':plugin.url_for('episode_view', url=item['url']), 'thumbnail':item['thumbnail']} for item in info]
    return plugin.finish(items, view_mode='thumbnail')

@plugin.route('/episode/<url>')
def episode_view(url):
    plugin.log.debug(url)
    info = scraper.parseEpisodePage(url)
    items = [{'label':item['title'], 'label2':item['broad_date'], 'path':plugin.url_for('play_episode', url=item['url']), 'thumbnail':item['thumbnail']} for item in info['episode']]
    # navigation
    if 'prevpage' in info:
    	items.append({'label':tPrevPage, 'path':plugin.url_for('episode_view', url=info['prevpage'])})
    if 'nextpage' in info:
    	items.append({'label':tNextPage, 'path':plugin.url_for('episode_view', url=info['nextpage'])})
    return plugin.finish(items, update_listing=False)

@plugin.route('/play/<url>')
def play_episode(url):
    flashVer = 'WIN 11,6,602,180'
    swfUrl = 'http://www.ondemandkorea.com/player/jw6.2/jwplayer.flash.swf'
    bitrate = resolution2bitrate[plugin.get_setting('quality', int)]
    plugin.log.debug(url)

    info = scraper.extractStreamUrl(url)
    avail_bitrates = info['bitrate'].keys()
    if not bitrate in avail_bitrates:
    	bitrate = avail_bitrates[0]
    video = info['bitrate'][bitrate]
    from xbmcswift2 import xbmc
    rtmp_url = "%s app=%s swfUrl=%s pageUrl=%s playpath=%s" % (video['tcUrl'], video['app'], swfUrl, url, video['playpath'])
    xbmc.Player().play( rtmp_url )
    return plugin.finish(None, succeeded=False)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
