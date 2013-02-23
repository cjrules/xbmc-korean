# -*- coding: utf-8 -*-
"""
  UI for subtitle download
"""
import sys
import os
import xbmc, xbmcgui, xbmcvfs

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__settings__ = sys.modules[ "__main__" ].__settings__

import gomtv_service
import cineast_service
from smi2ass import smi2ass

def gui():
  if __settings__.getSetting( "smi2ass" )=='true':
    smiPath = getExsitingSmi()
    if smiPath is None:
      smiPath = subt_down()
    if smiPath is not None:
      subt_conv(smiPath)
      xbmc.executebuiltin("Notification('Subtitles','converted to ASS')")
  else:
    subt_down()

def getExsitingSmi():
  movieFullPath = xbmc.Player().getPlayingFile()
  smiFullPath = movieFullPath[:movieFullPath.rfind('.')]+'.smi'
  return smiFullPath if xbmcvfs.exists(smiFullPath) else None

def subt_down():
  movieFullPath = xbmc.Player().getPlayingFile()
  if not xbmcvfs.exists(movieFullPath):
    xbmc.log("can not open movie file, %s" % movieFullPath, xbmc.LOGERROR)
    xbmcgui.Dialog().ok("can not open movie file", movieFullPath)
    return None
  smiFullPath = movieFullPath[:movieFullPath.rfind('.')]+'.smi'

  ###----- fetch list of available subtitles
  subt_list = []
  dialog = xbmcgui.DialogProgress()
  ignored = dialog.create(__scriptname__ )
  if __settings__.getSetting( "GomTV" )=='true':
    dialog.update( 0, _(100)%_(200) )
    subt_list1, temp, msg = gomtv_service.search_subtitles(movieFullPath, "", False, 0, 0, 0, False, False, "Korean", "English", "", False)
    if len(subt_list1) == 0:
      xbmcgui.Dialog().ok(__scriptname__, _(101)%_(200), _(108) )
    else:
      for i in range(len(subt_list1)):
        subt_list1[i]["service"] = "gomtv"
      subt_list += subt_list1
  if __settings__.getSetting( "Cineast" )=='true':
    dialog.update( 50, _(100)%_(202) )
    infoTag = xbmc.Player().getVideoInfoTag()
    title = infoTag.getTitle()
    year = infoTag.getYear()
    subt_list2, temp, msg = cineast_service.search_subtitles(movieFullPath, title.decode('utf-8'), "", year, 0, 0, False, False, "Korean", "English", "", False)
    if len(subt_list2) == 0:
      xbmcgui.Dialog().ok(__scriptname__, _(101)%_(202), _(108) )
    else:
      for i in range(len(subt_list2)):
        subt_list2[i]["service"] = "cineast"
      subt_list += subt_list2
  dialog.close()

  ###----- select a subtitle to download
  if len(subt_list)==0:
    dialog = xbmcgui.Dialog()
    ignored = dialog.ok(__scriptname__,
                        _(102).encode('utf-8')%os.path.basename(movieFullPath) )
  else:
    title_list = []
    for i in range(0,len(subt_list)):
      if subt_list[i]["service"] == "gomtv":
        title = "[Gom] "+subt_list[i]["filename"]
      elif subt_list[i]["service"] == "cineast":
        title = "[Cin] "+subt_list[i]["filename"]
      else:
        title = subt_list[i]['filename']
      title_list.append( title )
    xbmc.log(str(title_list), xbmc.LOGDEBUG)

    dialog = xbmcgui.Dialog()
    selected = dialog.select( _(103)%len(title_list), title_list )
    if selected < 0:
      return None

    smiTempDir = xbmc.translatePath( "special://temp/" )
    smiTempPath = None
    if subt_list[selected]["service"] == "gomtv":
      succeed, lang, smiTempPath = gomtv_service.download_subtitles(subt_list, selected, False, smiTempDir, None, None)
      if not succeed:
        xbmcgui.Dialog().ok(__scriptname__, _(101)%_(200), _(108) )
    elif subt_list[selected]["link"] == "cineast":
      succeed, lang, smiTempPath = cineast_service.download_subtitles(subt_list, selected, False, smiTempDir, None, None)
      if not succeed:
        xbmcgui.Dialog().ok(__scriptname__, _(101)%_(202), _(108) )
    if not smiTempPath:
      return None
    xbmc.log("subtitle is downloaded to "+smiTempPath, xbmc.LOGNOTICE)

    # try to copy temp file to desired path
    if xbmcvfs.copy(smiTempPath, smiFullPath):
      smiPath = smiFullPath
    else:
      xbmc.log("Fail to write subtitles to "+smiFullPath, xbmc.LOGWARNING)
      xbmcgui.Dialog().ok(__scriptname__, _(110), _(107), smiTempPath )
      smiPath = smiTempPath
    # enable the downloaded subtitle
    xbmc.Player().setSubtitles(smiPath)
    return smiPath

def subt_conv(smiPath=None):
  if smiPath is None:
    videoDir = os.path.dirname(xbmc.Player().getPlayingFile())
    smiPath = os.path.join(videoDir, xbmc.Player().getSubtitles())
  if not xbmcvfs.exists(smiPath):
    return
  if not smiPath.lower().endswith(".smi"):
    return
  assDict = smi2ass(smiPath)
  for lang in assDict:
    ext = lang+'.ass'
    if lang == '':
      ext = 'ass'
    assPath = smiPath[:smiPath.rfind('.')]+'.'+ext
    tempDir = xbmc.translatePath( "special://temp/" )
    tempFile = os.path.basename( smiPath[:smiPath.rfind('.')]+'.'+ext )
    tempPath = os.path.join( tempDir, tempFile )
    if not xbmcvfs.exists(assPath) or __settings__.getSetting( "overwrite_ass" )=='true':
      assfile = open(tempPath, "w")
      assfile.write(assDict[lang])
      assfile.close()
      if not xbmcvfs.copy(tempPath, assPath):
        xbmc.log("Fail to write subtitles to "+assPath, xbmc.LOGWARNING)
        xbmcgui.Dialog().ok(__scriptname__, _(110), _(107), assPath)
        assPath = tempPath
      # enable the downloaded subtitle
      xbmc.Player().setSubtitles(assPath)

# vim: softtabstop=2 shiftwidth=2 expandtab
