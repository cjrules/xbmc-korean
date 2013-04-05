# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin
import resources.lib.afreecam as afreecam

tPrevPage = u"[B]<<Prev page[/B]"
tNextPage = u"[B]Next page>>[/B]"

plugin = Plugin()

@plugin.route('/')
def main_menu():
    items = [
        {'label':'HOT', 'path':plugin.url_for('hot_list')},
        {'label':'ON-AIR', 'path':plugin.url_for('onair_list_firstpage')}
    ]
    return items

@plugin.route('/hot/')
def hot_list():
    url = afreecam.root_url + "/index.php"
    info = afreecam.parseMobileHot(url)
    items = [{'label':item['title'], 'path':plugin.url_for('watch_broadcast', bno=item['broad_no']), 'thumbnail':item['thumbnail']} for item in info['video']]
    return plugin.finish(items, view_mode='thumbnail')

@plugin.route('/onair/', name='onair_list_firstpage', options={'url':afreecam.root_url+"/onair.php"})
@plugin.route('/onair/<url>')
def onair_list(url):
    info = afreecam.parseMobileOnAir(url)
    items = [{'label':item['title'], 'path':plugin.url_for('watch_broadcast', bno=item['broad_no']), 'thumbnail':item['thumbnail']} for item in info['video']]
    if 'prevpage' in info:
        items.append({'label':tPrevPage, 'path':plugin.url_for('onair_list', url=info['prevpage'])})
    if 'nextpage' in info:
        items.append({'label':tNextPage, 'path':plugin.url_for('onair_list', url=info['nextpage'])})
    morepage = False if url.endswith('php') else True
    return plugin.finish(items, update_listing=morepage)

@plugin.route('/broadcast/<bno>')
def watch_broadcast(bno):
    from xbmcswift2 import xbmc
    url = afreecam.getStreamUrlByBroadNum( int(bno) )
    url += "|User-Agent="+afreecam.IPadAgent
    xbmc.Player().play(url)
    return plugin.finish(None, succeeded=False)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
