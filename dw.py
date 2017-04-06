#!/usr/bin/python
#coding:utf-8

import requests
import codecs
import os
import sys

src_url = 'http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=198&filter=author&orderby=dateline&sortid=192'
log_home = '~/1point3/'
keyword = '我这里要招人'

def fetch(code='utf-8', url = src_url):
    r = requests.get(url)
    return r.text.encode(code)

def save(pth = log_home + 'tmp.html'):
    f = codecs.open(pth, 'w+', 'UTF-8')
    f.write(get())

def flite(key=keyword, src=log_home + 'tmp.html'):
    rst = []
    with codecs.open(src, 'r','UTF-8') as f:
        for line in f:
            line = line.encode('UTF-8')
            if key in line:
                rst.append(line)
    return rst


#em>[<a href="http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=198&amp;filter=typeid&amp;typeid=653">我这里要招人</a>]</em> <a href="http://www.1point3acres.com/bbs/forum.php?mod=viewthread&amp;tid=259530&amp;extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26sortid%3D192%26sortid%3D192%26orderby%3Ddateline" onclick="atarget(this)" class="s xst">网络安全startup 招数据科学家</a>

def parse(text):
    arr = text.split('<a href=')
    if len(arr) != 3:
        return None
    text = arr[2]
    arr = text.split('onclick="atarget(this)" class="s xst"')
    if len(arr) != 2:
        return None
    url = arr[0][1:-2].replace('&amp;','&')
    title = arr[1][1:-5]
    return {'url':url, 'title':title}

def init():
    if not os.path.exists(log_home):
        os.mkdir(log_home)

def main():
    init()
    page = fetch()
    if page == None:
         sys.exit('Error: failed to download html.')   
    #TODO: save page with date as name
    flited = flite() 
    for text in flited:
        parsed =  parse(text)
        if parsed != None:
            print parsed['title']
            print parsed['url']
            print '=' * 80

main()
