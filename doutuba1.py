#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：albert time:2019/1/12

#同步爬取
import os
import re
from urllib import request

import requests
from bs4 import BeautifulSoup
from lxml import etree
def parser_page(url):
    print(url)
    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    req = requests.get(url,headers = headers)
    text = req.text
    soup = BeautifulSoup(text,'lxml')
    imgs = soup.find_all(class_="col-xs-6 col-sm-3")
    for img in imgs:
        img_url = img.contents[1].get('data-original')
        if img_url:
            img_name = img.contents[1].get('alt')
            img_name = re.sub(r'[\?？\.，。！!]',' ',img_name)
            suffix = os.path.splitext(img_url)[-1]
            suffix_name = suffix.split('!')[0]
            file_name = img_name+suffix_name
            print(file_name)
            request.urlretrieve(img_url,'images/'+file_name)
        #break





def main():
    for x in range(1,101):
        url = 'http://www.doutula.com/article/list/?page=%d'% x

        parser_page(url)


if __name__ == '__main__':
    main()
