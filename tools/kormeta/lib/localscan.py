# -*- coding: utf-8 -*-
"""
  Scan folder and extract episode number from files
  by edge @ xbmc-korea.com
"""

import os
import re

class LocalScan:
    def __init__(self): 
        self.EpisodeFound = {};
        self.Season = 1;
        self.KnownExt = ['.avi', '.mkv', '.mp4', '.mpg', '.wmv', '.tp', '.ts']

    # search with title
    def ScanVideo(self,topdir): 
        filelist = []
        for root,dir,files in os.walk(topdir):
            for fi in files:
                ext = os.path.splitext(fi)[1].lower()
                if ext in self.KnownExt:
                    filelist.append( os.path.join(root,fi) )
        return filelist

    # search with title
    def GetEpisodeInfo(self,files): 
        # rule
        rules = []
        rules.append( re.compile('[ \._](?:EP|ep)[ \.]?(?P<ep>\d+)[ \._]') )
        rules.append( re.compile('[ \._][Ee](?P<ep>\d+)[ \._]') )
        # scan
        found = []
        for path in files:
            for rule in rules:
                query = rule.search(path)
                if query:
                    found.append( (int(query.group('ep')), path) )
                    break
        return found

if __name__ == '__main__':
    seriesPath = os.path.join("d:"+os.sep,"Videos",u"드라마",u"지붕 뚫고 하이킥")

    scan = LocalScan()
    avifiles = scan.ScanVideo( seriesPath )
    found = scan.GetEpisodeInfo(avifiles)
    for epnum,epfile in found:
        outpath = os.path.splitext(epfile)
        outfile = outpath[0]+'.nfo'
        f=open(outfile,'w')
        f.close()
