import urllib,urllib2,re,xbmcplugin,xbmcgui

#TV DASH - by You 2008.

def CATEGORIES():
        req = urllib2.Request('http://tvnews.media.daum.net/')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class="M"><a href="(.+?)" id=".+?">(.+?)</a></li>').findall(link)
        count=1
        for url,name in match:
                url = re.sub('&amp;','&',url)
                addDir("%02d - "%(count) + name,url,3,'')
                count += 1

def NEWS_PROGRAM(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_div=re.compile('<div class="TvBro3">(.+?)</div>', re.DOTALL).findall(link)

        if len( match_div) > 0:
                match=re.compile('<a href="(.+?)">(.+?)</a>').findall(match_div[0])
                count=1
                for url,name in match:
                        url = re.sub('&amp;','&',url)
                        addDir("%02d - "%(count) + name,url,1,'')
                        count += 1
        else:
                INDEX(main_url)

def INDEX(main_url):
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<dl class="TV_RL">\s+<dd class="fl"><a href=".+?"><img src="(.+?)" width="100" height="76" alt="" /></a><br /></dd>\s+<dt class="fl"><a href="(.+?)">(.+?)</a><br /></dt>').findall(link)
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
        print "in videolinks" + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''UI.tvpotSWF\("http://flvs.daum.net/flvPlayer.swf\?vid=(.+?)"\)''').findall(link)
        print match
        for vid in match:
                flv = DaumGetFlvByVid(url,vid)
                addLink(name,flv,thumbnail)

#Python Video Decryption and resolving routines.
#Courtesy of Voinage, Coolblaze.        

def DaumGetFLV(referer, url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.compile('''<MovieLocation movieURL="(.+?)"''').findall(response)
    if len(query_match) > 0:
        return query_match[0]
    return None

def DaumGetFlvByVid(referer, vid):
    req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.compile('''<MovieLocation url="(.+?)"/>''').findall(response)
    if len(query_match) > 0:
        query_match[0] = re.sub('&amp;','&',query_match[0])
        print query_match[0]
        return DaumGetFLV(referer, query_match[0])


                
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
        NEWS_PROGRAM(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
