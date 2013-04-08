# -*- coding: utf-8 -*-
"""
    GomTV
"""
from xbmcswift2 import Plugin
import urllib
import resources.lib.gomtv as gomtv

plugin = Plugin()
_L = plugin.get_string

m_broad = "plugin://plugin.video.m.gomtv.com/play/contentsid/%d"

tPrevPage = u"[B]<<%s[/B]" % _L(30101)
tNextPage = u"[B]%s>>[/B]" % _L(30102)

#gomtv.setCookieFile( xbmc.translatePath('special://profile/addon_data/%s/cookie.txt' %plugin.id) )

@plugin.route('/')
def main_menu():
    items = [
        {'label':u"무료영화",    'path':plugin.url_for("video_list", cate='8', subcate='30', page='-')},
        {'label':u"무료드라마",  'path':plugin.url_for("video_list", cate='6', subcate='42', page='-')},
        {'label':u"무료연예오락",'path':plugin.url_for("video_list", cate='7', subcate='50', page='-')},
        {'label':u"뮤직",        'path':plugin.url_for("video_list", cate='12', subcate='12', page='-')},
        {'label':u"게임/스포츠", 'path':plugin.url_for("sub_menu", cate='13')},
    ]
    return items

@plugin.route('/<cate>/')
def sub_menu(cate):
    items = gomtv.parseSubCateList(int(cate))
    return [{'label':item['title'], 'path':plugin.url_for('video_list', cate=cate, subcate=str(item['subcate']), page='-')} for item in items]

@plugin.route('/<cate>/<subcate>/<page>')
def video_list(cate, subcate, page):
    page2 = 1 if page=='-' else int(page)
    info = gomtv.parseBoard(int(cate), int(subcate), page2)
    items = [{'label':item['title'], 'path':m_broad %item['contentsid'], 'thumbnail':item['thumbnail']} for item in info['video']]
    # navigation
    if 'prevpage' in info:
        items.append({'label':tPrevPage, 'path':plugin.url_for('video_list', cate=cate, subcate=subcate, page=str(info['prevpage']))})
    if 'nextpage' in info:
        items.append({'label':tNextPage, 'path':plugin.url_for('video_list', cate=cate, subcate=subcate, page=str(info['nextpage']))})
    morepage = False if page=='-' else True
    return plugin.finish(items, update_listing=morepage)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
