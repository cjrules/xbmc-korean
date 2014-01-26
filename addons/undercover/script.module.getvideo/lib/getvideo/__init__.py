from extract_dailymotion import extract_video_from_url as extract_dailymotion
#from extract_sohu import extract_video_from_url as extract_sohu
from extract_tudou import extract_video_from_url as extract_tudou
from extract_youku import extract_video_from_url as extract_youku
from extract_youtube import extract_video_from_url as extract_youtube

from extract_withflvcd import extract_withFLVCD as extract_withFLVCD

def extract_video_from_url(url):
    if "dailymotion.com" in url:
        return extract_dailymotion(url)
    elif "tudou.com" in url:
        return extract_tudou(url)
    elif "youku.com" in url:
        return extract_youku(url)
    elif "youtube.com" in url:
        return extract_youtube(url)
    return extract_withFLVCD(url)
