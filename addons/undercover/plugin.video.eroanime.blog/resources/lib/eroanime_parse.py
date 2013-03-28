# -*- coding: utf-8 *-*
# eroanimedougakan.blog.fc2.com
#   - Directory
#        あかさたなはまやらわ
#   - Index (recent)

import urllib
import re
from BeautifulSoup import BeautifulSoup

home_url = "http://eroanimedougakan.blog.fc2.com/"

def parse_directory(page_url):
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html)
    result = []
    section = None
    for node in soup.find('div',{'class':'entry_text'}).findAll(re.compile('a|span|div')):
        if node.name == 'span':
            if section is not None:
                result.append(section)
            section = {'title':node.text, 'data':[]}
        elif node.name == 'a':
            section['data'].append({'title':node.text[1:], 'path':node['href']})
        elif node.name == 'div' and node.has_key('class') and node['class']=='fc2_footer':
            break
    if section is not None:
        result.append(section)
    return result

def parse_series(page_url):
    html = urllib.urlopen(page_url).read()
    sect_list = re.compile('<div id="more">(.*?)</div>', re.S).search(html).group(1).split('<br /><br />')
    result = []
    for sect in sect_list[:-1]:
        if not "【動画】" in sect:
            continue
        sect2 = re.sub('^\s*<br */>', '', sect).strip()
        soup = BeautifulSoup(sect2, fromEncoding='utf-8')
        episode = {'title':soup.contents[0].string, 'link':[]}
        for a_node in soup.findAll('a'):
            if a_node.text[0] == u'【':
                title = a_node.text[1:-1]
                episode['link'].append({'title':title, 'path':a_node['href']})
        result.append(episode)
    return result

if __name__ == "__main__":
    print parse_directory(home_url+"blog-entry-2.html")
    print parse_series(home_url+"blog-entry-318.html")
