# encoding: utf-8
import urllib,urllib2,re,xbmcplugin,xbmcgui

#TV DASH - by You 2008.

def CATEGORIES():
        addDir("01 - 프로리그","http://tvpot.daum.net/game/sl/LeagueList.do?league=pro&type=list",3,'')
        addDir("02 - 온게임넷 스타리그","http://tvpot.daum.net/game/sl/LeagueList.do?league=osl&type=list",3,'')

def STAR_LEAGUE(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

	minfc=re.compile('''\s*<h5><strong>(\d{4}.\d{2}.\d{2})</strong>.*?</h5>\s*<p>\s*(.*)</p>''')
	setc1=re.compile('''([^<]+)</strong>\s*<dl>\s*<dt[^/]+</dt>\s*<dd class="player">\s*<a class=[^>]+>([^<]+)</a>\s*<em[^/]+</em>\s*</dd>\s*</dl>\s*<span>VS</span>\s*<dl class="right">\s*<dt[^/]+</dt>\s*<dd class="player">\s*<a class=[^>]+>([^<]+)</a>\s*<em[^/]+</em>\s*</dd>\s*</dl>\s*<a href="/clip/ClipView.do\?clipid=(\d+)" class="playBtn on">''')
	setc2=re.compile('''([^<]+)</strong>\s*<dl>\s*<dt[^/]+</dt>\s*<dd class="description">([^<]+)</dd>\s*</dl>\s*<a href="/clip/ClipView.do\?clipid=(\d+)" class="playBtn on"''')

	mgrp=re.split('''<div class="matchGroup">''',link)
	print "#match groups=%d"%(len(mgrp)-1)
	match_cnt=0
	for mgdata in mgrp[1:]:		#skip first chunk
		match_cnt = match_cnt+1

		mset=re.split('''<strong class="set">''',mgdata)
		print "#set in match%d=%d"%(match_cnt, len(mset)-1)

		# match date & title
		mhdr = re.sub('\s+',' ',mset[0])
		mginfo = minfc.match(mhdr)
		if (mginfo is None):
			match_date = ""
			match_title = ""
		else:
			match_date  = mginfo.group(1)
			match_title = re.sub('<br\s*/?>',' ',mginfo.group(2))
			match_title = re.sub('<[^>]*>','',match_title)
			match_title = re.sub('\s*$','',match_title)

		# players in each set
		for setdata in mset[1:]:
			match = setc1.findall(setdata)
			for setname,player1,player2,clipid in match:
				url = "http://tvpot.daum.net/clip/ClipView.do?clipid=%s" % (clipid)
				VIDEOLINKS("%s %s - %s[%s vs %s]" % (match_date,match_title,setname,player1,player2),url,'')
			match=setc2.findall(setdata)
			for setname,descr,clipid in match:
				if clipid == 0:
					continue
				url = "http://tvpot.daum.net/clip/ClipView.do?clipid=%s" % (clipid)
				VIDEOLINKS("%s %s - %s[%s]" % (match_date,match_title,setname,descr),url,'')


def INDEX(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''daumEmbed_.+?\('.+?','(.+?)','.+?'[,\)]''').findall(link)
        count=1
        for thumbnail,url,name in match:
                url = re.sub('&amp;','&',url)
                VIDEOLINKS("%02d - "%(count) + name,main_url+url,thumbnail)
                count += 1
        if count == 1:
                match=re.compile('''<a href="(.+?)"><img src="(.+?)" width="120" height="90" alt="" class="img" /></a>\s+ <div class="R">\s+<h4><a href=".+?" class="tit">(.+?)</a></h4>''').findall(link)
                for url,thumbnail,name in match:
                    url = re.sub('&amp;','&',url)
                    VIDEOLINKS("%02d - "%(count) + name,main_url+url,thumbnail)
                    count += 1


def VIDEOLINKS(name,url,thumbnail):
	#print "in videolink",name,url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	# daumEmbed_jingle2 had 3 arguments, but daumEmbed_standard had 4
        match=re.compile('''daumEmbed_.+?\('.+?','(.+?)','.+?'[,\)]''').findall(link)
        for vid in match:
                flv = DaumGetFlvByVid(url,vid)
                addLink(name,flv,thumbnail)

#Python Video Decryption and resolving routines.
#Courtesy of Voinage, Coolblaze.        

def DaumGetFLV(referer, url):
    print "daum loc=" + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.compile('''<MovieLocation movieURL="(.+?)" />''').findall(response)
    if len(query_match) > 0:
        return query_match[0]
    return None

def DaumGetFlvByVid(referer, vid):
    print "daum vid=" + str(vid)
    req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.compile('''<MovieLocation regdate="\d+" url="(.+?)" storage=".+?"/>''').findall(response)
    if len(query_match) > 0:
        query_match[0] = re.sub('&amp;','&',query_match[0])
        return DaumGetFLV(referer, query_match[0])
    return None


                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        print "get_params", paramstring
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        print "in addLink ", name, url
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        print "-------" + str(u)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==3:
        print ""+url
        STAR_LEAGUE(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
