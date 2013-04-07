# -*- coding: utf-8 -*-
"""
  m.gomtv.com
"""
import urllib2, re
from BeautifulSoup import BeautifulSoup
import simplejson

BrowserAgent = "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) Mobile"

root_url = "http://m.gomtv.com"

def parseList(main_url):
    vid_info = {}
    vid_info['tab'] = []
    vid_info['subtab'] = []
    vid_info['list'] = []

    req = urllib2.Request(main_url)
    req.add_header("User-Agent", BrowserAgent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)

    # tab menu
    for node in soup.find("nav", {"class":re.compile("^top_menu")}).findAll('a'):
        vid_info['tab'].append( {'title':node.string, 'url':root_url+node['href']} )
    # subtab menu
    for node in soup.find("ul", {"class":"list_tab"}).findAll('a'):
        sorttype = re.compile("'listsort'\s*:\s*'(\d+)'").search(node['href']).group(1)
        vid_info['subtab'].append( {'title':node.string, 'url':main_url+"&listsort="+sorttype} )
    # programs
    sect = soup.find("div", {"id":"contentsList"})
    if sect:
        for node in sect.findAll('a'):
            title = ' '.join(node.find('dt').findAll(text=True))
            vid_info['list'].append( {'title':title, 'url':root_url+node['href'], 'thumb':node.find('img')['src']} )
    return vid_info

def parseProg(main_url):
    vid_info = {}
    req = urllib2.Request(main_url)
    req.add_header("User-Agent", BrowserAgent)
    html = urllib2.urlopen(req).read()

    # program info
    match = re.search('&chnum=(\d+)&', html)
    if not match:
    	return None
    vid_info['chnum'] = match.group(1)
    for vname,vval in re.compile(r"^\s*var (\w+)\s*=\s*'(\d+)';",re.M).findall(html):
    	if vname == "systype" or vname[:2] == "id" or vname == "contentsid" or vname == "seriesid":
    	    vid_info[vname] = vval

    # video base
    down_url = root_url+"/ajax/getPlayUrl.gom"
    req = urllib2.Request(down_url)
    req.add_header("User-Agent", BrowserAgent)
    req.add_header("Referer", main_url)
    paras = '&authmodel=ipad&systemversion=4.3'
    jsonstr = urllib2.urlopen(req, paras).read()
    markup = simplejson.loads(jsonstr)
    vid_info['video_base'] = markup['param']

    # video link
    vid_info['link'] = []
    btndiv = re.compile('<dd class="btn">(.*?)</dd>', re.S).findall(html)
    match = re.compile(r"""setPlayVideo\('(.*?)'\);">(.*?)</a>""").findall(btndiv[-1])
    for item in match:
        url = vid_info['video_base'] + item[0]
        vid_info['link'].append( {'title':item[1].decode('utf-8'), 'url':url} )
    if len(match) == 0:
        vid_info['titles'] = [nn.decode('utf-8') for nn in re.compile(r';">(.*?)</a>').findall(btndiv[-1])]

    return vid_info

def parseProg2(main_url):
    info = parseProg(main_url)
    if len(info['link']) == 0:
        # trick to guess 1st/2nd node id
        req = urllib2.Request(main_url)
        req.add_header("User-Agent", BrowserAgent)
        html = urllib2.urlopen(req).read()
        nid = re.search('nid=(\d*)', html).group(1)
        nid1 = str(int(nid)-1)
        nid2 = str(int(nid1)+6)
        info['link'].append({'title':info['titles'][0],'url':info['video_base']+getRequestQuery(info['contentsid'], info['seriesid'], nid1)})
        info['link'].append({'title':info['titles'][1],'url':info['video_base']+getRequestQuery(info['contentsid'], info['seriesid'], nid2)})
    return info

def getRequestQuery(contentsid, seriesid, nodeid):
    ss  = "&attr1=10002"
    ss += "&contentsid=" + contentsid
    ss += "&seriesid=" + seriesid
    ss += "&userno="
    ss += "&nodeid=" + nodeid
    ss += "&level_flag=4"
    ss += "&service_flag=1"
    ss += "&isfree=1"
    ss += "&platform_flag=2"
    ss += "&etc0="
    return ss

if __name__ == "__main__":
    #info = parseProg(root_url+"/view.gom?contentsid=552606&service=musicvideo")
    info = parseProg(root_url+"/view.gom?contentsid=453618&service=game")
    print "%s %s" % (info['contentsid'], info['seriesid'])
    print "%s %s %s %s" % (info['chnum'], info['id0s'], info['id1s'], info['id2s'])
    if len(info['link']):
        for item in info['link']:
            print item['title'] + " : " + item['url']
    else:
    	print "http://ch.gomtv.com/%s/%s/%s" % (info['chnum'],info['id1s'],info['id2s'])
    	print getRequestQuery(info['contentsid'],info['seriesid'],'?')

# vim:sts=4:et
