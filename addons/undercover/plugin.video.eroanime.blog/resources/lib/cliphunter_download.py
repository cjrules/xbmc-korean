import urllib
import re

def extract_from_url(page_url):
    return extract_from_mobile(page_url.replace("//www.","//m."))

# from http://s.gexo.me/ch3/126//js/mobile/player,favorites.js
def mobile_decrypt(ss):
    atbl = "mbcidgsaztuynlfvjxrqpewhko"
    ctbl = {'$':':', '=':'/', '&':'.', '^':'&', '(':'='} 
    out = []
    for c in ss:
    	if c.isalpha():
    	    out.append(chr(ord('a')+atbl.find(c)))
    	elif c in ctbl:
    	    out.append(ctbl[c])
    	else:
    	    out.append(c)
    return ''.join(out)

def extract_from_mobile(page_url):
    html = urllib.urlopen(page_url).read()
    vid_title = re.search('<h3>(.*?)</h3>', html).group(1)
    vtbl = dict()
    for key, val in re.compile("^var (\w+) = '([^']*)'", re.M).findall(html):
    	vtbl[key] = val
    encstr = vtbl['pl_fiji_p']
    vid_url = mobile_decrypt(encstr)
    vid_thumb = vtbl['mov_thumb'];
    return {'title':vid_title, 'url':vid_url, 'thumbnail':vid_thumb}

def extract_from_flash(page_url):
    import base64
    iid = re.search('/(\d+)/', page_url).group(1)
    new_url = "http://www.cliphunter.com/embed/"+iid
    html = urllib.urlopen(new_url).read()
    encstr = re.compile('{d:\s*"(.*?)"}').search(html).group(1)
    jstr = base64.b64decode(encstr)
    return None

# Read command line arguments.
if __name__ == "__main__":
    print extract_from_url('http://www.cliphunter.com/w/985521/Inyouchuu_Ep_1')
