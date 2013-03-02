# -*- coding: utf-8 -*- 

import sys
import os
import re
from utilities import log, languageTranslate
from cineast import CineastWebService

_ = sys.modules[ "__main__" ].__language__   

def search_subtitles( file_original_path, title, tvshow, year, season, episode, set_temp, rar, lang1, lang2, lang3, stack ): #standard input
    msg = ""
    subtitles_list = []
    websvc = CineastWebService()
    title = title.strip()
    if tvshow:  # TvShow
        log(__name__, "search TVshow with "+tvshow)
        for result in websvc.searchTvSubtitlesByTitle(tvshow):
            subtitle = {"format": "smi", "sync": True}
            subtitle['link'] = result['link']
            subtitle['filename'] = result['title']
            rating = 0
            if season == result['season']:
                rating += 3
            if episode == result['episode']:
                rating += 3
            subtitle['rating'] = str(rating)
            subtitle['language_name'] = result['language']
            subtitle['language_flag'] = "flags/%s.gif" %languageTranslate(result['language'],0,2)
            subtitles_list.append( subtitle )
    elif title:   # Movie
        srch_title = title
        query = re.match("^(.*)\(([^\)]*)\)$", title)
        if query:
            srch_title = query.group(2).strip() # English title
        log(__name__, "search Movie with "+srch_title)
        for result in websvc.searchMovieSubtitlesByTitle(srch_title):
            subtitle = {"format": "smi", "sync": True}
            subtitle['link'] = result['link']
            subtitle['filename'] = result['title']
            subtitle['rating'] = "6" if file_original_path.find(result['relgrp']) > 0 else "0"
            subtitle['language_name'] = result['language']
            subtitle['language_flag'] = "flags/%s.gif" %result['language'][:2].lower()
            subtitles_list.append( subtitle )
    else:
        msg = _(800)
    return subtitles_list, "", msg #standard output

def download_subtitles (subtitles_list, pos, zip_subs, tmp_sub_dir, sub_folder, session_id): #standard input
    language = subtitles_list[pos][ "language_name" ]
    websvc = CineastWebService()
    subtitle = websvc.parseSubtitlesPage( subtitles_list[pos]["link"] )[0]
    log(__name__,  u"download subtitle from %s" %subtitle["link"])
    try:
        tmp_fname = os.path.join(tmp_sub_dir, subtitle["filename"])
        resp = urllib2.urlopen(url)
        f = open(tmp_fname, "w")
        f.write(resp.read())
        f.close()
    except:
        return False, language, ""
    return True, language, tmp_fname #standard output
