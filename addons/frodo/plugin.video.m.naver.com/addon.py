# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin
import resources.lib.jrnaverm as jrnaverm
import urllib

tPrevPage = u"[B]<<이전[/B]"
tNextPage = u"[B]다음>>[/B]"

dispPerPage = 10

plugin = Plugin()

@plugin.route('/')
def main_menu():
    items = [
        {'label':u"쥬니어 네이버", 'path':plugin.url_for('jrnaver_list')}
    ]
    return items

@plugin.route('/jr/')
def jrnaver_list():
    results = jrnaverm.parseMenu("tv")
    return [{'label':item['name'],
             'path':plugin.url_for('jrvideo_list', serviceId=item['serviceId']),
             'thumbnail':item['thumb']
            } for item in results]

@plugin.route('/jr/service/<serviceId>/')
def jrvideo_list(serviceId):
    totalCnt = jrnaverm.getContentsCount("tv", serviceId)
    plugin.redirect(plugin.url_for('jrvideo_list_page', serviceId=serviceId, totalCnt=totalCnt, pageNum='-'))

@plugin.route('/jr/list/<serviceId>/<totalCnt>/<pageNum>')
def jrvideo_list_page(serviceId, totalCnt, pageNum):
    pageNum2 = 0 if pageNum == '-' else int(pageNum)
    totalCnt2 = int(totalCnt)
    dispCount = totalCnt2 if totalCnt2 < dispPerPage else dispPerPage
    result = jrnaverm.parseVideoList("tv", serviceId, pageNum2*dispPerPage, dispCount)
    items = []
    for item in result:
        items.append( { 'label':item['title'],
                        'path':plugin.url_for('jrplay_url', url=jrnaverm.root_url+item['link']),
                        'thumbnail':item['thumb'] } )
    # page navigation
    if pageNum2 > 0:
        prevPageNum = pageNum2-1
        items.append({'label':tPrevPage, 'path':plugin.url_for("jrvideo_list_page", serviceId=serviceId, totalCnt=totalCnt, pageNum=prevPageNum)})
    if totalCnt2 > ((pageNum2+1)*dispPerPage):
        nextPageNum = pageNum2+1
        items.append({'label':tNextPage, 'path':plugin.url_for("jrvideo_list_page", serviceId=serviceId, totalCnt=totalCnt, pageNum=nextPageNum)})
    morepage = False if pageNum == '-' else True
    return plugin.finish(items, update_listing=morepage)

@plugin.route('/play/<url>')
def jrplay_url(url):
    result = jrnaverm.parseVideoPage( url )
    nurl = result['path']+"|User-Agent="+jrnaverm.BrowserAgent
    from xbmcswift2 import xbmc, xbmcgui
    li = xbmcgui.ListItem(result['title'], iconImage="defaultVideo.png")
    li.setInfo('video', {"Title": result['title']})
    xbmc.Player().play(nurl, li)
    return plugin.finish(None, succeeded=False)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
