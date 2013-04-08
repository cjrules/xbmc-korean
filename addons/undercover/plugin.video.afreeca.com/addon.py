# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin
import resources.lib.afreeca as afreeca
import resources.lib.afreeca_station as afreeca_station
import resources.lib.afreeca_sports as afreeca_sports

plugin = Plugin()

UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.9"
m_broad = "plugin://plugin.video.m.afreeca/broadcast/"

tPrevPage = u"[B]<<%s[/B]" %plugin.get_string(30100)
tNextPage = u"[B]%s>>[/B]" %plugin.get_string(30101)

@plugin.route('/')
def main_menu():
    items = []
    items.append({'label':u"[COLOR FF00FF00]스포츠[/COLOR]", 'path':plugin.url_for("sports_menu")})
    ###
    videos = afreeca.getIssueBroadcast(plugin.get_setting("showMoreIssueBroad", bool))
    if videos:
        items.append({'label':u"[COLOR FF0000FF]이슈 생방송[/COLOR]", 'path':''})
        for video in videos:
            vid_path = m_broad + video['broad_no']
            items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':vid_path, 'thumbnail':video['thumb']})
    ###
    for section in afreeca.getTopBroadcast():
    	items.append({'label':u"[COLOR FF0000FF]%s[/COLOR]" %section['title'], 'path':''})
        for video in section['data']:
            if 'broad_no' in video:
                if 'url' in video:
                    items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':info['url'], 'thumbnail':video['thumb'], 'is_playable':True})
                else:
                    #vid_path = plugin.url_for("watch_broadcast", userId=video['user_id'], broadNo=video['broad_no'])
                    vid_path = m_broad + video['broad_no']
                    items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':vid_path, 'thumbnail':video['thumb']})
            else:
            	plugin.log.warning("unknown broadcast info")
            	print video
    ###
    for section in afreeca.getTopClips():
    	items.append({'label':u"[COLOR FF0000FF]%s[/COLOR]" %section['title'], 'path':''})
        for video in section['data']:
            if 'title_no' in video:
                items.append({'label':video['title'], 'label2': video['user_nick'], 'path':plugin.url_for("play_ucc_rtmp", url=video['flv_name']), 'thumbnail':video['thumb']})
            elif 'broad_type' in video and video['broad_type'] == 'vod':
                items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':plugin.url_for("play_ucc_rtmp", url=video['url']), 'thumbnail':video['thumb']})
    ###
    items.append({'label':u"[COLOR FF00FF00]실시간 시청인원 급상승 방송[/COLOR]", 'path':plugin.url_for("rapid_growing")})
    items.append({'label':u"[COLOR FF00FF00]베스트 BJ[/COLOR]", 'path':plugin.url_for("best_bj")})
    items.append({'label':u"[COLOR FF00FF00]BJ 랭킹[/COLOR]", 'path':plugin.url_for("bj_ranking")})
    items.append({'label':u"[COLOR FF00FF00]게임 랭킹[/COLOR]", 'path':plugin.url_for("game_ranking")})
    return items

@plugin.route('/rapid_growing/')
def rapid_growing():
    items = []
    for video in afreeca.getRapidGrowingBroadcast():
        vid_path = m_broad + video['broad_no']
        items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':vid_path, 'thumbnail':video['thumb']})
    return plugin.finish(items, view_mode='thumbnail')

@plugin.route('/best_bj/')
def best_bj():
    items = [{'label':item['user_nick'], 'label2':item['intro_title'], 'path':plugin.url_for("user_station", userId=item['user_id']), 'thumbnail':item['img_path']} for item in afreeca.getBestBj()]
    return plugin.finish(items, view_mode='thumbnail')

@plugin.route('/bj_ranking/')
def bj_ranking():
    return [{'label':item['bj_nick'], 'path':plugin.url_for("user_station", userId=item['bj_id'])} for item in afreeca.getBjRanking()]

@plugin.route('/station/<userId>')
def user_station(userId):
    items = []
    info = afreeca_station.is_broadcasting(userId)
    if info:
    	if 'broad_no' in info:
    	    broadNo = info['broad_no']
        else:
            tbl = afreeca.searchBroadById(userId)
            broadNo = tbl[userId][0] if userId in tbl else None
        if broadNo:
            #vid_path = plugin.url_for("watch_broadcast", userId=userId, broadNo=broadNo)
            vid_path = m_broad + broadNo
            items.append({'label':u"[B]방송보기[/B] %s" %info['title'], 'path':vid_path, 'thumbnail':info['thumbnail']})
    items.append({'label':u"[COLOR FF0000FF]동영상[/COLOR]", 'path':''})
    result = afreeca_station.parse_ucc(userId, '')
    for item in result['video']:
    	items.append({'label':item['title'], 'path':plugin.url_for("play_ucc", userId=userId, titleNo=item['ucc_id']), 'thumbnail':item['thumbnail']})
    return items

@plugin.route('/game_ranking/')
def game_ranking():
    return [{'label':item['game_name'], 'path':plugin.url_for("game_broadcast", gameNo=item['game_no'])} for item in afreeca.getGameRanking()]

@plugin.route('/game/<gameNo>')
def game_broadcast(gameNo):
    items = []
    for video in afreeca.getGameBroadcast(gameNo):
        #vid_path = plugin.url_for("watch_broadcast", userId=video['user_id'], broadNo=video['broad_no'])
        vid_path = m_broad + video['broad_no']
        items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':vid_path, 'thumbnail':video['thumb']})
    return items

@plugin.route('/broadcast/<userId>/<broadNo>')
def watch_broadcast(userId, broadNo):
    from xbmcswift2 import xbmc
    url = afreeca.extractBroadUrl(userId, broadNo)
    xbmc.Player().play(url)
    return plugin.finish(None, succeeded=False)

@plugin.route('/ucc_url/<url>')
def play_ucc_rtmp(url):
    from xbmcswift2 import xbmc
    info = afreeca_station.extractRtmpUrl( url )
    rtmp_url = "%s app=%s playpath=%s" % (info['tcUrl'], info['app'], info['playpath'])
    xbmc.Player().play( rtmp_url )
    return plugin.finish(None, succeeded=False)

@plugin.route('/ucc/<userId>/<titleNo>')
def play_ucc(userId, titleNo):
    from xbmcswift2 import xbmc
    info = afreeca_station.extractUccUrl( userId, titleNo )
    rtmp_url = "%s app=%s swfUrl=%s pageUrl=%s playpath=%s" % (info['tcUrl'], info['app'], info['swfUrl'], info['pageUrl'], info['playpath'])
    xbmc.Player().play( rtmp_url )
    return plugin.finish(None, succeeded=False)

@plugin.route('/sports/')
def sports_menu():
    items = []
    items.append({'label':u"[COLOR FF00FF00]e스포츠[/COLOR]", 'path':plugin.url_for("esports_menu")})
    items.append({'label':u"[COLOR FF0000FF]스포츠 베스트[/COLOR]", 'path':''})
    for item in afreeca_sports.getSportsBest():
        items.append({'label':item['b_subject'], 'path':plugin.url_for("watch_sports_url", url=item['link_url']), 'thumbnail':item['img']})
    items.append({'label':u"[COLOR FF0000FF]e스포츠 베스트[/COLOR]", 'path':''})
    for item in afreeca_sports.getEsportsBest():
        items.append({'label':item['b_subject'], 'path':plugin.url_for("watch_sports_url", url=item['link_url']), 'thumbnail':item['img']})
    return items

@plugin.route('/esports/')
def esports_menu():
    items = [
        {'label':'GSL',  'path':plugin.url_for("sports_highlight", cid='esports_highlight', btype='GSL', page='-')},
        {'label':'GSTL', 'path':plugin.url_for("sports_highlight", cid='esports_highlight', btype='GSTL', page='-')},
        {'label':'LOL',  'path':plugin.url_for("sports_highlight", cid='esports_highlight', btype='LOL', page='-')},
    ]
    return items
    #return plugin.finish(items, view_mode='thumbnail')

@plugin.route('/sports_highlight/<cid>/<btype>/<page>/')
def sports_highlight(cid, btype, page):
    if page == '-':
    	page = ''
    result = afreeca_sports.parseBoard(cid, btype, page)
    items = [{'label':item['title'], 'path':plugin.url_for("watch_sports", cid=cid, bno=item['b_no'], btype=btype), 'thumbnail':item['thumbnail']} for item in result['video']]
    if 'prev_pgno' in result:
        items.append({'label':tPrevPage, 'path':plugin.url_for("sports_highlight", cid=cid, btype=btype, page=result['prev_pgno'])})
    if 'next_pgno' in result:
        items.append({'label':tNextPage, 'path':plugin.url_for("sports_highlight", cid=cid, btype=btype, page=result['next_pgno'])})
    morepage = True if page else False
    return plugin.finish(items, update_listing=morepage)

@plugin.route('/watch/sports/<cid>/<bno>/<btype>/')
def watch_sports(cid, bno, btype):
    proxy = plugin.get_setting('proxyServer', unicode) if plugin.get_setting('useProxy', bool) else None
    info = afreeca_sports.getInfoById(cid, bno, btype, proxy=proxy)
    print info
    return play_sports_stream(info['c_id'], info['b_no'], info['sub_btype'], info['idx'])

@plugin.route('/watch/sports/url/<url>')
def watch_sports_url(url):
    proxy = plugin.get_setting('proxyServer', unicode) if plugin.get_setting('useProxy', bool) else None
    info = afreeca_sports.parseVideoPage( url, proxy=proxy )
    print info
    return play_sports_stream(info['c_id'], info['b_no'], info['sub_btype'], info['idx'])

def play_sports_stream(c_id, b_no, sub_btype, idx):
    video = afreeca_sports.extractStreamUrl(c_id, b_no, sub_btype, idx)
    print video
    #return plugin.play_video({'label':video['title'], 'path':video['url'], 'thumbnail':video['thumbnail']})
    from xbmcswift2 import xbmc, xbmcgui
    import re
    tcUrl, app, playpath = re.search("(rtmp://[^/]+)/([^/]+)/(.*)", video['url']).group(1,2,3)
    vid_url = "%s app=%s playpath=%s" %(tcUrl, app, playpath)
    li = xbmcgui.ListItem(video['title'], iconImage=video['thumbnail'])
    li.setInfo('video', {"Title": video['title']})
    xbmc.Player().play(vid_url, li)
    return plugin.finish(None, succeeded=False)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
