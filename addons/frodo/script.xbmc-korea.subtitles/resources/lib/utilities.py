# -*- coding: utf-8 -*-
"""
  dummy file to run a service file from 'XBMC Subtitles'
"""
import xbmc, xbmcvfs
import hashlib

def log(name, text):
    xbmc.log("%s - %s" %(name, text), xbmc.LOGINFO)

LANGABBR = {
    "English":"en",
    "Korean":"ko",
}
def languageTranslate(lang, fromlang, tolang):
    return LANGABBR[lang]

def hashFileMD5(file_path, buff_size=1048576):
    # calculate MD5 key from file
    f = xbmcvfs.File(file_path)
    if f.size() < buff_size:
        return None
    f.seek(0,0)
    buff = f.read(buff_size)    # size=1M
    f.close()
    # calculate MD5 key from file
    m = hashlib.md5();
    m.update(buff);
    return m.hexdigest()
