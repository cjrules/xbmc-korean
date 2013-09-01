# -*- coding: utf-8 -*-
"""
    GomTV Mobile
"""
from xbmcswift2 import Plugin, xbmc, xbmcgui
import urllib
import resources.lib.gomm as gomm

plugin = Plugin()
_L = plugin.get_string

root_url = "http://m.gomtv.com"
tPrevPage = u"[B]<<%s[/B]" % _L(30101)
tNextPage = u"[B]%s>>[/B]" % _L(30102)

gomm.setCookieFile( xbmc.translatePath('special://profile/addon_data/%s/cookie.txt' %plugin.id) )

@plugin.route('/')
def main_menu():
    info = gomm.parseMenu(root_url)
    return [{'label':item['title'], 'path':plugin.url_for('section_list', url=item['url'])} for item in info['tab']]

@plugin.route('/section/<url>')
def section_list(url):
    info = gomm.parseMenu(url)
    # check login
    if info is None:
    	if not gomtv_login():
    	    return
        info = gomm.parseMenu(url)
    if info is None:
        xbmcgui.Dialog().ok(_L(30010), _L(30013))
    	return
    return [{'label':item['title'], 'path':plugin.url_for('program_list', service=item['service'], cate=item['cate'], offset='-')} for item in info['subtab']]

@plugin.route('/program/<service>/<cate>/<offset>')
def program_list(service, cate, offset):
    offset2 = 0 if offset=='-' else int(offset)
    plistStep = plugin.get_setting('plistStep', int)
    vlist = gomm.parseList(service, cate, offset2, plistStep)
    items = [{'label':item['title'], 'path':plugin.url_for('video_url', url=item['url']), 'thumbnail':item['thumbnail']} for item in vlist]
    # navigation
    if offset2 > 0:
        new_offset = (offset2-plistStep) if offset2 >= plistStep else 0
        items.append({'label':tPrevPage, 'path':plugin.url_for('program_list', service=service, cate=cate, offset=str(new_offset))})
    if len(vlist) == plistStep:
        new_offset = offset2 + plistStep
        items.append({'label':tNextPage, 'path':plugin.url_for('program_list', service=service, cate=cate, offset=str(new_offset))})
    morepage = False if offset=='-' else True
    return plugin.finish(items, update_listing=morepage)

@plugin.route('/play/url/<url>')
def video_url(url):
    proxy = None
    if plugin.get_setting('useProxy', bool):
    	proxy = plugin.get_setting('proxyServer', unicode)
    	print "Proxy="+proxy
    info = gomm.parseProg(url, proxy=proxy)
    if info is None:
    	if not gomtv_login():
    	    return
        info = gomm.parseProg(url, proxy=proxy)
    if info is None:
        xbmcgui.Dialog().ok(_L(30010), _L(30013))
        return
    if len(info['link']) == 1:
    	video = info['link'][0]
        url = video['url'] + "|Referer="+url
        li = xbmcgui.ListItem(video['title'], iconImage="DefaultVideo.png")
        li.setInfo('video', {"Title": video['title']})
        xbmc.Player().play(url, li)
    elif plugin.get_setting('plistDir', bool):
        items = [{'label':item['title'], 'path':item['url']+"|Referer="+url, 'thumbnail':"DefaultVideo.png", 'is_playable':True} for item in info['link']]
        return plugin.finish(items)
    else:
        pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        pl.clear()
        for item in info['link']:
            li = xbmcgui.ListItem(item['title'], iconImage="DefaultVideo.png")
            li.setInfo( 'video', { "Title": item['title'] } )
            pl.add(item['url']+"|Referer="+url, li)
        xbmc.Player().play(pl)
    return plugin.finish(None, succeeded=False)

@plugin.route('/play/contentsid/<contentsid>')
def play_contentsid(contentsid):
    return plugin.redirect(plugin.url_for("video_url", url=root_url+"/view.gom?contentsid="+contentsid))

def gomtv_login():
    userid = plugin.get_setting('account', unicode)
    password = plugin.get_setting('password', unicode)
    if not userid or not password:
        xbmcgui.Dialog().ok(_L(30010), _L(30011))
        return False
    if not gomm.login(userid, password):
        xbmcgui.Dialog().ok(_L(30010), _L(30012))
        return False
    plugin.notify(_L(30014), title=plugin.name)
    return True

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
