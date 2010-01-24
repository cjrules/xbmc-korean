import urllib,urllib2,re,xbmcplugin,xbmcgui

#TV DASH - by You 2008.

def CATEGORIES():
        addDir('BEST - Daily','http://tvpot.daum.net/best/BestToday.do?svctab=best&range=0',1,'')
        addDir('BEST - Weekly','http://tvpot.daum.net/best/BestToday.do?svctab=best&range=1',1,'')
        addDir('BEST - Monthly','http://tvpot.daum.net/best/BestToday.do?svctab=best&range=2',1,'')
        addDir('BEST - 100k','http://tvpot.daum.net/best/BestToday.do?svctab=10m',1,'')
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''<img src="([^"]+)" width="110" height="84" alt="[^"]+"\s+title="([^"]+)" /></a></dd>\s*<dt><a href="([^"]+)">''').findall(link)
        count=1
        for thumbnail,name,url in match:
                name = re.sub('\n',' ',name)
                name = re.sub('&lt;','<',name)
                name = re.sub('&gt;','>',name)
                name = re.sub('&quot;','"',name)
                name = re.sub('&#39;','\'',name)
                if url[0] == '/':
                        url = 'http://tvpot.daum.net' + url
                url = re.sub('&amp;','&',url)
                url = re.sub(' ','',url)
                VIDEOLINKS("%02d - "%(count) + name,url,thumbnail)
                count += 1
	print "matched item %d"%count

def VIDEOLINKS(name,url,thumbnail):
	#print "in videolink",name,url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''daumEmbed_.+?\('.+?','(.+?)','.+?','.+?'\)''').findall(link)
        for vid in match:
                flv = DaumGetFlvByVid(url,vid)
                addLink(name,flv,thumbnail)

#Python Video Decryption and resolving routines.
#Courtesy of Voinage, Coolblaze.        

def DaumGetFLV(referer, url):
    print "daum loc="+url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.compile('''<MovieLocation movieURL="(.+?)"''').findall(response)
    if len(query_match) > 0:
        return query_match[0]
    return None

def DaumGetFlvByVid(referer, vid):
    print "daum vid="+str(vid)
    req = urllib2.Request("http://flvs.daum.net/viewer/MovieLocation.do?vid="+vid)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', referer)
    page = urllib2.urlopen(req);response=page.read();page.close()
    query_match = re.compile('''<MovieLocation regdate="\d+" url="(.+?)" storage=".+?"/>''').findall(response)
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


xbmcplugin.endOfDirectory(int(sys.argv[1]))
