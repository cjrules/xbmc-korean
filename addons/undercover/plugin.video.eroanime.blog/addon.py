# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin
import resources.lib.eroanime_parse as eroanime_parse
import urllib

UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.9"

plugin = Plugin()

@plugin.route('/')
def main_menu():
    items = [
        {'label':'Directory', 'path':plugin.url_for('directory_list')}
    ]
    return items

@plugin.route('/directory/')
def directory_list():
    items = [
        {'label':u'あ', 'path':plugin.url_for('directory_page', page='blog-entry-2.html')},
        {'label':u'か', 'path':plugin.url_for('directory_page', page='blog-entry-3.html')},
        {'label':u'さ', 'path':plugin.url_for('directory_page', page='blog-entry-4.html')},
        {'label':u'た', 'path':plugin.url_for('directory_page', page='blog-entry-5.html')},
        {'label':u'な', 'path':plugin.url_for('directory_page', page='blog-entry-6.html')},
        {'label':u'は', 'path':plugin.url_for('directory_page', page='blog-entry-7.html')},
        {'label':u'ま', 'path':plugin.url_for('directory_page', page='blog-entry-8.html')},
        {'label':u'や', 'path':plugin.url_for('directory_page', page='blog-entry-9.html')},
        {'label':u'ら', 'path':plugin.url_for('directory_page', page='blog-entry-10.html')},
        {'label':u'わ', 'path':plugin.url_for('directory_page', page='blog-entry-11.html')}
    ]
    return items

@plugin.route('/dirpage/<page>')
def directory_page(page):
    url = eroanime_parse.home_url + page
    items = []
    for section in eroanime_parse.parse_directory(url):
        items.append({'label':u"[COLOR FFFF0000]%s[/COLOR]" %section['title'], 'path':''})
        for item in section['data']:
            items.append({'label':item['title'], 'path':plugin.url_for('series_page', url=item['path'])})
    return items

@plugin.route('/series/<url>')
def series_page(url):
    items = []
    for episode in eroanime_parse.parse_series(url):
        items.append({'label':u"[COLOR FFFF0000]%s[/COLOR]" %episode['title'], 'path':''})
        for item in episode['link']:
            if 'toukoucity.to' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('toukoucity_play', url=item['path'])})
            elif '2anime.net' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('_2anime_list', url=item['path'])})
            elif 'fc2.com' in item['path']:
                items.append({'label':'FC2', 'path':plugin.url_for('fc2_list', url=item['path'])})
            elif 'xvideos.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('xvideos_play', url=item['path'])})
            elif 'slutload.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('slutload_play', url=item['path'])})
            elif 'hardsextube.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('hardsextube_play', url=item['path'])})
            elif 'sunporno.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('sunporno_play', url=item['path'])})
            elif 'redtube.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('redtube_play', url=item['path'])})
            elif 'pornhub.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('pornhub_play', url=item['path'])})
            elif 'cliphunter.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('cliphunter_play', url=item['path'])})
            elif 'videobam.com' in item['path']:
                items.append({'label':item['title'], 'path':plugin.url_for('videobam_play', url=item['path'])})
            elif 'hentaicrunch.com' in item['path']:
                items.append({'label':'Hentaicrunch', 'path':plugin.url_for('hentaicrunch_list', url=item['path'])})
            elif 'watchhentaionline.net' in item['path']:
                items.append({'label':'Watchhentaionline', 'path':plugin.url_for('hentaicrunch_play', url=item['path'])})
            elif 'animestigma.com' in item['path']:
                items.append({'label':'Hentaistigma', 'path':plugin.url_for('hentaistigma_list', url=item['path'])})
            elif 'hentaistream.com' in item['path']:
                items.append({'label':'Hentaistream', 'path':plugin.url_for('hentaistream_list', url=item['path'])})
            elif 'tubehentai.me' in item['path']:
                items.append({'label':'Tubehentai', 'path':plugin.url_for('tubehentai_play', url=item['path'])})
            elif 'nuvid.com' in item['path']:
                items.append({'label':'Nuvid', 'path':plugin.url_for('nuvid_play', url=item['path'])})
            elif 'spankwire.com' in item['path']:
                items.append({'label':'Spankwire', 'path':plugin.url_for('spankwire_play', url=item['path'])})
            else:
                items.append({'label':u"[I]%s[/I]" %item['title'], 'path':''})
    return items

#################################################################
@plugin.route('/toukoucity_play/<url>')
def toukoucity_play(url):
    from resources.lib.toukoucity_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

#-----------------------------------------
@plugin.route('/_2anime_list/<url>')
def _2anime_list(url):
    from resources.lib._2anime_download import parse_search_result
    items = []
    for item in parse_search_result(url):
        items.append({'label':item['title'], 'path':plugin.url_for('_2anime_play', url=item['path']), 'thumbnail':item['thumbnail']})
    return items

@plugin.route('/_2anime_play/<url>')
def _2anime_play(url):
    from resources.lib._2anime_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

#-----------------------------------------
@plugin.route('/fc2_list/<url>')
def fc2_list(url):
    from resources.lib.fc2_download import parse_search_result
    items = []
    for item in parse_search_result(url):
        items.append({'label':item['title'], 'path':plugin.url_for('fc2_play', url=item['path']), 'thumbnail':item['thumbnail']})
    return items

@plugin.route('/fc2_play/<url>')
def fc2_play(url):
    from resources.lib.fc2_download import extract_from_url, UserAgent
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    url = '{0:s}|User-Agent={1:s}&Cookie={2:s}'.format(info['url'], UserAgent, info['cookie'])
    xbmc.Player().play(url, li)
    return plugin.finish(None, succeeded=False)

#-----------------------------------------
@plugin.route('/hentaicrunch_list/<url>')
def hentaicrunch_list(url):
    from resources.lib.hentaicrunch_download import parse_series_page
    items = []
    info = parse_series_page(url)
    for item in info['episode']:
        items.append({'label':item['title'], 'path':plugin.url_for('hentaicrunch_play', url=item['path'])})
    return items

@plugin.route('/hentaicrunch_play/<url>')
def hentaicrunch_play(url):
    from resources.lib.hentaicrunch_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

#-----------------------------------------
@plugin.route('/hentaistigma_list/<url>')
def hentaistigma_list(url):
    from resources.lib.hentaistigma_download import parse_search_result
    items = []
    for item in parse_search_result(url):
        items.append({'label':item['title'], 'path':plugin.url_for('hentaistigma_play', url=item['path'])})
    return items

@plugin.route('/hentaistigma_play/<url>')
def hentaistigma_play(url):
    from resources.lib.hentaistigma_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    if info['type'] == 'rtmp':
        vid_url = "%s app=%s swfUrl=%s pageUrl=%s playpath=%s" % (info['tcUrl'], info['app'], info['swfUrl'], info['pageUrl'], info['play'])
    else:
        vid_url = info['path']
    xbmc.Player().play(vid_url, li)
    return plugin.finish(None, succeeded=False)

#-----------------------------------------
@plugin.route('/hentaistream_list/<url>')
def hentaistream_list(url):
    from resources.lib.hentaistream_download import parse_search_result
    items = []
    for item in parse_search_result(url):
        items.append({'label':item['title'], 'path':plugin.url_for('hentaistream_play', url=item['path'])})
    return items

@plugin.route('/hentaistream_play/<url>')
def hentaistream_play(url):
    from resources.lib.hentaistream_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    pl.clear()
    for info in extract_from_url( url ):
        li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
        li.setInfo( 'video', { "Title": info['title'] } )
        pl.add(info['path'], li)
    xbmc.Player().play(pl)
    return plugin.finish(None, succeeded=False)

#-----------------------------------------
@plugin.route('/xvideos_play/<url>')
def xvideos_play(url):
    from resources.lib.xvideos_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/slutload_play/<url>')
def slutload_play(url):
    from resources.lib.slutload_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/hardsextube_play/<url>')
def hardsextube_play(url):
    from resources.lib.hardsextube_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/sunporno_play/<url>')
def sunporno_play(url):
    from resources.lib.sunporno_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/redtube_play/<url>')
def redtube_play(url):
    from resources.lib.redtube_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/pornhub_play/<url>')
def pornhub_play(url):
    from resources.lib.pornhub_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/cliphunter_play/<url>')
def cliphunter_play(url):
    from resources.lib.cliphunter_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/videobam_play/<url>')
def videobam_play(url):
    from resources.lib.videobam_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/tubehentai_play/<url>')
def tubehentai_play(url):
    from resources.lib.tubehentai_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage=info['thumbnail'])
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/nuvid_play/<url>')
def nuvid_play(url):
    from resources.lib.nuvid_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

@plugin.route('/spankwire_play/<url>')
def spankwire_play(url):
    from resources.lib.spankwire_download import extract_from_url
    from xbmcswift2 import xbmc, xbmcgui
    info = extract_from_url( url )
    li = xbmcgui.ListItem(info['title'], iconImage="DefaultVideo.png")
    li.setInfo( 'video', { "Title": info['title'] } )
    xbmc.Player().play(info['url'], li)
    return plugin.finish(None, succeeded=False)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
