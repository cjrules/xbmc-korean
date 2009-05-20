import urllib,urllib2,re,xbmcplugin,xbmcgui

#TV DASH - by You 2008.

def CATEGORIES():
        addDir('MOVIES - Daily best','http://movie.daum.net/ranking/movieclip_ranking/bestTrailer.do?datekey=3',1,'')
        addDir('MOVIES - Weekly best','http://movie.daum.net/ranking/movieclip_ranking/bestTrailer.do?datekey=2',1,'')
        addDir('MOVIES - Monthly best','http://movie.daum.net/ranking/movieclip_ranking/bestTrailer.do?datekey=1',1,'')
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<img src="(.+?)" width="73" height="55" alt=".+?" class="poster" /></a>\s*<p style="width:360px;"><a href="(.+?)">(.+?)</a></p>').findall(link)
        count=1
        for thumbnail,url,name in match:
                VIDEOLINKS("%02d - "%(count) + name,url,thumbnail)
                count += 1
        match=re.compile('''<a href="(.+?)">(.+?)</a>\r\n		</td>\r\n		<td class="td5"><a href=".+?"><img src="http://img-contents.daum-img.net/movie/2008_home/ranking/btn_play.gif"''').findall(link)
        for url,name in match:
                VIDEOLINKS("%02d - "%(count) + name,url,'')
                count += 1
        #match=re.compile('<img src="(.+?)" width="73" height="55" alt=".+?" class="poster" /></a>\s*<p style="width:360px;"><a href="(.+?)">(.+?)</a></p>').findall(link)

def VIDEOLINKS(name, url, thumbnail):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''UI.embedSWF\("http://flvs.daum.net/flvPlayer.swf\?vid=(.+?)\&''').findall(link)
        for vid in match:
                flv = DaumMovie(url,vid)
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

def DaumMovie(referer, vid):
    req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.compile('''<MovieLocation url="(.+?)"/>''').findall(response)
    if len(query_match) > 0:
        query_match[0] = re.sub('&amp;','&',query_match[0])
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
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
