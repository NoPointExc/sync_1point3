#!/usr/bin/python
#coding:utf-8

import requests
import codecs
import os
import sys
import time
from datetime import date
import config

src_url = config.src_url
log_home = config.log_home
keyword = '我这里要招人'

def catch(url = src_url, pth = log_home):
    fname = date.today().strftime('%y-%m-%d') + '.html'
    fpth = os.path.join(pth, fname)
    if not os.path.exists(fpth):
        r = requests.get(url)
        if r.status_code != 200:
            sys.exit("Error: failed to download page, error status "+ r.status_code)
        f = codecs.open(fpth, 'w+', 'UTF-8')
        f.write(r.text)
    return fpth

def flite(src=log_home + '/tmp.html', key = keyword):
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

def main():
    if not os.path.exists(log_home):
        os.mkdir(log_home)
    fpth = catch() 
    flited = flite(fpth) 
    for text in flited:
        parsed =  parse(text)
        if parsed != None:
            print parsed['title']
            print parsed['url']
            print '=' * 80

main()
