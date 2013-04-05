# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin
import resources.lib.afreeca as afreeca
import resources.lib.afreecam as afreecam
import resources.lib.afreeca_station as afreeca_station

plugin = Plugin()

UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.9"

@plugin.route('/')
def main_menu():
    items = []
    items.append({'label':u"[B]베스트 BJ[/B]", 'path':plugin.url_for("best_bj")})
    #items.append({'label':u"[B]BJ 랭킹[/B]", 'path':plugin.url_for("bj_ranking")})
    items.append({'label':u"[B]게임 랭킹[/B]", 'path':plugin.url_for("game_ranking")})
    for section in afreeca.getTopItems():
    	items.append({'label':u"[COLOR FF0000FF]%s[/COLOR]" %section['title'], 'path':''})
        for video in section['data']:
            if 'title_no' in video:
                items.append({'label':video['title'], 'label2': video['user_nick'], 'path':plugin.url_for("play_ucc_rtmp", url=video['flv_name']), 'thumbnail':video['thumb']})
            elif 'broad_no' in video:
                if 'url' in video:
                    items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':info['url'], 'thumbnail':video['thumb'], 'is_playable':True})
                else:
                    items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':plugin.url_for("watch_broadcast", userId=video['user_id'], broadNo=video['broad_no']), 'thumbnail':video['thumb']})
            elif 'broad_type' in video and video['broad_type'] == 'vod':
                items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':plugin.url_for("play_ucc_rtmp", url=video['url']), 'thumbnail':video['thumb']})
    return items

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
            items.append({'label':u"[B]방송보기[/B] %s" %info['title'], 'path':plugin.url_for("watch_broadcast", userId=userId, broadNo=broadNo), 'thumbnail':info['thumbnail']})
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
        items.append({'label':video['broad_title'], 'label2': video['user_nick'], 'path':plugin.url_for("watch_broadcast", userId=video['user_id'], broadNo=video['broad_no']), 'thumbnail':video['thumb']})
    return items

@plugin.route('/broadcast/<userId>/<broadNo>')
def watch_broadcast(userId, broadNo):
    from xbmcswift2 import xbmc
    url = afreecam.getStreamUrlByBroadNum( int(broadNo) )
    url += "|User-Agent="+afreecam.IPadAgent
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

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
