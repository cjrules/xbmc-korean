import re
import os
from util import getHTML
import xbmcaddon

URLLANG = 'http://www.ted.com/translate/languages'

__settings__ = xbmcaddon.Addon(id='plugin.video.ted.talks.sami')


class Subtitle:

    samiLangMap = {'eng':'ENCC', 'kor':'KRCC'}
    samiFullLangMap = {'eng':'Name:English; lang:en-US;', 'kor':'Name:Korean; lang:ko-KR;'}

    def __init__(self, language=None):
        if language is None:
	    self.genLangAbbr()
	    lang = __settings__.getSetting('subtitleLang')
	    self.language = self.langAbbr[ lang ]
	else:
	    self.language = language

    def genLangAbbr (self):
        self.langAbbr = { 'English':'eng' }
        html = getHTML( URLLANG )
        for full,abbr in re.compile('<a title="(.*?)" href="/translate/languages/(.*?)">').findall(html):
            self.langAbbr[ full ] = abbr

    # Format Time from TED Subtitles format to SRT time Format
    def formatTime ( self, time ) :
        milliseconds = 0
        seconds = ((time / 1000) % 60)
        minutes = ((time / 1000) / 60)
        hours = (((time / 1000) / 60) / 60)
        formatedTime = str ( hours ) + ':' + str (minutes) + ':' + str ( seconds ) + ',' + str ( milliseconds )
        return formatedTime

    # Convert TED Subtitles to SRT Subtitles
    def convertTEDSubtitlesToSRTSubtitles ( self, jsonString , introDuration ) :
        from simplejson import loads
        jsonObject = loads( jsonString )

        srtContent = ''
        captionIndex = 1

        for caption in jsonObject['captions'] :
            startTime = str ( self.formatTime ( introDuration + caption['startTime'] ) )
            endTime = str ( self.formatTime ( introDuration + caption['startTime'] + caption['duration'] ) )

            srtContent += ( str ( captionIndex ) + os.linesep )
            srtContent += ( startTime + ' --> ' + endTime + os.linesep )
            srtContent += ( caption['content'] + os.linesep )
            srtContent += os.linesep

            captionIndex = captionIndex + 1
        return srtContent

    # Convert TED Subtitles to SMI Subtitles
    def convertTEDSubtitlesToSMISubtitles ( self, jsonString , introDuration ) :
        from simplejson import loads
        jsonObject = loads( jsonString )

	smiLang = self.samiLangMap[ self.language ]
        smiContent = '<SAMI>\n<HEAD>\n<STYLE TYPE="text/css">\n<!--\n'
        smiContent += '.%s {%s SAMIType:CC;}\n' % (smiLang, self.samiFullLangMap[ self.language ])
        smiContent += '-->\n</STYLE>\n</HEAD>\n<BODY>\n'
        for caption in jsonObject['captions'] :
            smiContent += "<SYNC Start=" + str(introDuration + caption['startTime']) + ">"
            smiContent += "<P Class=" + smiLang + ">\n"
            smiContent += caption['content'] + "\n"
        smiContent += '</BODY>\n</SAMI>'
        return smiContent

    def getTEDSubtitlesByTalkID ( self, id ) :
        tedSubtitleUrl = 'http://www.ted.com/talks/subtitles/id/' + str(id) + '/lang/' + self.language
        print tedSubtitleUrl
        return getHTML( tedSubtitleUrl )

    def saveTEDSubtitlesByTalkID ( self, id, introDur , savepath ) :
        jsonStr = self.getTEDSubtitlesByTalkID ( id )
        srtStr = self.convertTEDSubtitlesToSRTSubtitles ( jsonStr , introDur )
        f = open(savepath, "w")
        f.write(srtStr.encode('utf-8'))
        f.close()

    def mergeSMI ( self, smiStr1, smiStr2 ) :
	langDef1,smiBody1 = re.compile('\n(\.[^\n]*\n).*?<BODY>\n(.*)</BODY>', re.U|re.S).search(smiStr1).group(1,2)
	langDef2,smiBody2 = re.compile('\n(\.[^\n]*\n).*?<BODY>\n(.*)</BODY>', re.U|re.S).search(smiStr2).group(1,2)
        smiStr = '<SAMI>\n<HEAD>\n<STYLE TYPE="text/css">\n<!--\n'
        smiStr += langDef1
        smiStr += langDef2
        smiStr += '-->\n</STYLE>\n</HEAD>\n<BODY>\n'
        smiStr += smiBody1
        smiStr += smiBody2
        smiStr += '</BODY>\n</SAMI>'
        return smiStr
