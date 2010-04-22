# -*- coding: utf-8 -*-
import sys,urllib2,md5
import string,re

_ = sys.modules[ "__main__" ].__language__

browser_hdr = 'GomPlayer 2, 1, 23, 5007 (KOR)'
gomtv_home  = "http://gom.gomtv.com"

def gomtv_jamak_from_file(f):
    f.seek(0)
    buff = f.read(1024*1024)    # size=1M
    # calculate MD5 key from file
    m = md5.new(); m.update(buff); key = m.hexdigest()

    ###--- Search subtitle in GomTV site
    queryAddr = gomtv_home+"/jmdb/search.html?key=%s"%key
    print "search subtitle at %s"%queryAddr
    req = urllib2.Request(queryAddr)
    req.add_header('User-Agent', browser_hdr)
    try: resp = urllib2.urlopen(req)
    except urllib2.URLError, e:
	print e.reason
	return []
    link = resp.read(); resp.close()

    match = re.match('''<script>location.href = '([^']*)';</script>''',link)
    if match:
	if 'noResult' in match.group(1):
	    print "Unusual result page, "+queryAddr
	    return []
	else:
	    # single search result
	    return [ ('gomtv', _(104), gomtv_home+'/jmdb/'+match.group(1)) ]

    # regular search result page
    url_match  = re.compile('''<div><a href="([^"]*)">\[([^\]]*)\]([^<]*)</a>''',re.U).findall(link)
    date_match = re.compile('''<td>(\d{4}.\d{2}.\d{2})</td>''').findall(link)
    if len(url_match) == 0 or len(url_match) != len(date_match): 
	print "Unusual result page, "+queryAddr
	return []

    ###----- Select a subtitle to download
    title_list = []
    for i in range(0,len(date_match)):
	title = "[%s] %s (%s)"%(url_match[i][1], string.strip(url_match[i][2]), date_match[i])
	title_list.append( ('gomtv', title, gomtv_home+url_match[i][0]) )
    return title_list

def gomtv_jamak_url(url):
    print "parse subtitle page at %s"%url
    req = urllib2.Request(url)
    req.add_header('User-Agent', browser_hdr)
    try: resp = urllib2.urlopen(req)
    except urllib2.URLError, e:
	print e.reason
	return ''
    link = resp.read(); resp.close()
    downid = re.search('''javascript:save[^\(]*\('(\d+)','(\d+)','[^']*'\);''',link).group(1,2)
    return gomtv_home+"/jmdb/save.html?intSeq=%s&capSeq=%s"%downid
