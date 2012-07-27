# -*- coding: utf-8 -*-
"""
  gomtv.com
"""

import urllib2, re

root_url = "http://ch.gomtv.com"

def parseProg(main_url):
    vid_info = {}
    html = urllib2.urlopen(main_url).read()
    """
    hgstr = re.search(r"this\.arrHighBjoinv\s*=\s*\[(.*?)\];", html).group(1)
    lwstr = re.search(r"this\.arrLowBjoinv\s*=\s*\[(.*?)\];", html).group(1).split(',')
    if len(hgstr):
        pidlist = hgstr.split(',')
    elif len(lwstr):
        pidlist = lwstr.split(',')
    else:
        pidlist = []
    """

    # node id
    match = re.search(r"this\.arrCommonMid\s*=\s*\[(.*?)\];", html)
    if match is None:
    	return None
    ndstr = match.group(1)
    if len(ndstr):
        nodelist = ndstr.split(',')
    else:
        nodelist = []

    # title
    titlist = re.compile('<li class="pbtn">.*?<span>(.*?)</span></a></li>',re.S).findall(html)
    if len(nodelist) == 1 and len(titlist) == 0:
    	titlist = [ re.compile('<h1[^>]*><a[^>]*>(.*?)</a>',re.U).search(html).group(1) ]

    # output combine
    vid_info['playlist'] = []
    if len(nodelist) <= len(titlist):
        for i in range(len(nodelist)):
            vid_info['playlist'].append( {'title':titlist[i].decode('euc-kr'), 'nodeid':nodelist[i]} )
    else:
    	print "ERROR: #node(%d) > #title(%d)" % (len(nodelist), len(titlist))

    return vid_info

if __name__ == "__main__":
    info = parseProg(root_url+"/427/28099/393618")
    for item in info['playlist']:
        print item['title'] + " : " + item['nodeid']

# vim:sts=4:et
