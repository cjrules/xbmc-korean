# -*- coding: utf-8 -*-
"""
    [board.php]
    bo_table:   psd_caption(자막자료실), psd_dramacap(드라마자막)
    sfl:                                field
                wr_subject||wr_subject  제목
                wr_subject||wr_content  제목+내용
                wr_content              내용
                mb_id,1                 회원아이디
                mb_id,0                 회원아이디(코)
                wr_name,1               이름
                wr_name,0               이름 (코)
                wr_5                    제작(stx=1), 수정(stx=2), SUB(stx=3), 기타(stx=4)
                wr_6                    제작년도
                wr_7                    NEW(stx=1)
                100list                 100인LIST(stx=1)
    stx:        키워드                  text
    sop:        and, or                 operator
    page:       <number>
    sca:        한글,영문,통합,기타     category
    mv_no:        
    spt:
    sw:

    [rss.php]
    same parameters, but only wr_* are accepted for sfl
"""
import urllib
import re
from BeautifulSoup import BeautifulSoup
from xml.sax import saxutils
from utilities import log

class CineastWebService:
    root_url = "http://www.cineast.co.kr"

    def __init__(self):
        self.season_ptn = re.compile(u"시즌\s*(\d+)")
        self.episode_ptn = re.compile(u"(\d+)\s*화")
        self.filedown_ptn = re.compile(u"file_download\('(.*?)', *'(.*?)'\);")

    def searchMovieSubtitlesByTitle(self, kw):
        kw2 = urllib.quote(kw.encode('utf-8'), safe='')
        url = self.root_url + "/bbs/board.php?bo_table=psd_caption&sfl=wr_subject||wr_subject&sop=and&stx=%s" %kw2
        log( "CineastWebService", "Search Movie "+url );
        return self.parseMovieResultPage(url)

    def parseMovieResultPage(self, url):
        subtitles = []
        soup = BeautifulSoup( urllib.urlopen(url).read() )
        #tbl = soup.find('td',text=u"번호").find_parent('table')
        tbl = soup.find('td',text=u"번호").parent.parent.parent
        for item in tbl.findAll('tr'):
            if item.has_key('height') and item['height']=='28':
                cols = item.findAll('td')
                relgrp = cols[1].text

                title = ''.join(cols[3].findAll(text=True)).strip()
                title2 = title[:title.rfind("&nbsp;")]
                lang, title3 = title2.split('\n')
                title3 = saxutils.unescape( title3 )
                if lang == u"[영문]":
                    lang2 = "English"
                elif lang == u"[일문]":
                    lang2 = "Japanese"
                else:
                    lang2 = "Korean"

                url = cols[3].find('a')['href']
                if url.startswith("../bbs"):
                    url = self.root_url + url[2:]
                subtitles.append( {"title":title3, "link":url, "language":lang2, "relgrp":relgrp} )
        return subtitles

    def searchTvSubtitlesByTitle(self, kw):
        kw2 = urllib.quote(kw.encode('utf-8'), safe='')
        url = self.root_url + "/bbs/board.php?bo_table=psd_dramacap&sfl=wr_subject&sop=and&stx=%s" %kw2
        log( "CineastWebService", "Search TV "+url );
        return self.parseTvResultPage(url)

    def parseTvResultPage(self, url):
        subtitles = []
        soup = BeautifulSoup( urllib.urlopen(url).read() )
        tbl = soup.find('td',text=u"번호").parent.parent.parent
        for item in tbl.findAll('tr')[2:]:
            if item.has_key('height') and item['height']=='28':
                cols = item.findAll('td')
                try:
                    season = int( self.season_ptn( cols[1].nobr.text ).group(1) )
                except:
                    season = 0

                try:
                    episode = int( self.episode_ptn( cols[2].nobr.text ).group(1) )
                except:
                    episode = 0

                title = ''.join(cols[3].findAll(text=True)).strip()
                title2 = title[:title.rfind("&nbsp;")]
                lang, title3 = title2.split('\n')
                title3 = saxutils.unescape( title3 )
                if lang == u"[영문]":
                    lang2 = "English"
                elif lang == u"[일문]":
                    lang2 = "Japanese"
                else:
                    lang2 = "Korean"

                url = cols[3].find('a')['href']
                if url.startswith("../bbs"):
                    url = self.root_url + url[2:]
                subtitles.append( {"title":title3, "link":url, "language":lang2, "season":season, "episode":episode} )
        return subtitles

    def parseSubtitlesPage(self, url):
        html = urllib.urlopen(url).read()
        return [{"filename":fname, "link":self.root_url+"/bbs"+url[1:]} for url, fname in self.filedown_ptn.findall(html)]

if __name__=="__main__":
    websrv = CineastWebService()
    subtitles = websrv.searchMovieSubtitlesByTitle(u"전쟁")
    print "movie: %d" %len(subtitles)
    subtitles = websrv.searchTvSubtitlesByTitle(u"셜록")
    print "tv: %d" %len(subtitles)
